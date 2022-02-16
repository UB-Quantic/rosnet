from typing import Callable, Dict
import functools
from math import ceil
from rosnet.helper.typing import Future


class TunableTask:
    def __init__(self, **kwargs):
        self.task_info = kwargs
        self.__fn = None

    @property
    def fn(self):
        return self.__fn

    @functools.lru_cache
    def generate_variant(self, **kwargs):
        from pycompss.api.task import task
        from pycompss.api.constraint import constraint

        return constraint(**kwargs)(task(**self.task_info)(self.fn))

    def __getitem__(self, **kwargs):
        return self.generate_variant(**kwargs)

    def __call__(self, *args, **kwargs):
        if self.fn is None:
            self.fn = args[0]
            return self

        constraints = tune(self.fn, *args, **kwargs)

        # automatic unpacking of wrapper objects
        args = [arg.ref if isinstance(arg, Future) else arg for arg in args]

        return self.generate_variant(**constraints)(*args, **kwargs)


def tune(fn: Callable, *args, **kwargs) -> Dict[str, int]:
    from rosnet.tuning.compss import core_count

    # dispatch cost function
    try:
        mem_usage = do(fn.__name__, *args, **kwargs, like="rosnet.tuning.cost.mem")
    except:
        mem_usage = 1

    # TODO get memory space from COMPSs
    available_memory_per_node = 92 * 1024 ** 3

    # conservative parallelization: with uniform mem/core, min #cores that fulfill the task
    par = min(int(ceil(core_count() * mem_usage / available_memory_per_node)), 1)

    return {"computing_units": str(par)}
