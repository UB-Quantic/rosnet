from typing import Union
import numpy as np
from rosnet.tuning.task import autotune
from rosnet.core.interface import Array


@autotune(a=IN, returns=1)
def count_nonzero(a: Array, axis, keepdims) -> Union[int, np.ndarray]:
    return np.count_nonzero(a, axis=axis, keepdims=keepdims)
