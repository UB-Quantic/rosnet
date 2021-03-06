import functools
import itertools
import operator as op
from typing import Sequence

import numpy as np
from multimethod import multimethod
from rosnet.core.interface import Array


def isunique(l: Sequence) -> bool:
    """Checks whether all the elements in `l` are unique in `l`"""
    return len(set(l)) == len(l)


def space(s: list):
    """Generates an iterator through the Cartesian space of dimensionality `s`"""
    return itertools.product(*[range(i) for i in s])


def result_shape(a, b, axes):
    "Returns the blockshape of the resulting array after `tensordot`."
    outer_axes = [tuple(set(range(len(bs))) - set(ax)) for ax, bs in zip(axes, (a, b))]
    return functools.reduce(op.add, (tuple(i[ax] for ax in outer_ax) for outer_ax, i in zip(outer_axes, (a, b))))


def join_idx(outer, inner, axes):
    n = len(outer) + len(inner)
    outer_axes = filter(lambda i: i not in axes, set(range(n)))

    res = [0] * n

    for axe, v in zip(axes, inner):
        res[axe] = v

    for axe, v in zip(outer_axes, outer):
        res[axe] = v

    return tuple(res)


@multimethod
def __recurse(x):
    yield None


@__recurse.register
def __recurse(x: list):
    yield x
    yield from recurse(x[0])


@__recurse.register
def __recurse(x: np.ndarray):
    if isinstance(x.flat[0], np.ndarray):
        yield x
        yield from recurse(x.flat[0])
    # NOTE NumPy's scalar types fulfill the ArrayConvertable interface, and we don't want that
    elif isinstance(x.flat[0], Array):
        yield x


def recurse(x):
    yield from filter(lambda x: x is not None, __recurse(x))


def nest_level(x):
    return sum(1 for _ in recurse(x))


def measure_shape(x):
    return tuple(len(i) for i in recurse(x))
