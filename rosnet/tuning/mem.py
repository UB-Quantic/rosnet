from math import prod
import numpy as np
from rosnet.helper.macros import implements
from rosnet.helper.typing import Array
from rosnet.helper.math import result_shape


@implements("tensordot", ext="tuning.mem")
def tensordot(a: Array, b: Array, axes) -> int:
    assert all(a.shape[i] == b.shape[j] for i, j in zip(*axes))

    shape = result_shape(a.shape, b.shape, axes)
    dtype = np.result_type(a.dtype, b.dtype)
    return a.nbytes + b.nbytes + prod(shape) * dtype.itemsize


@implements("full", ext="tuning.mem")
def full(shape, fill_value, dtype=None, **kwargs) -> int:
    dtype = dtype or np.dtype(type(fill_value))
    return prod(shape) * dtype.itemsize


@implements("reshape", ext="tuning.mem")
def reshape(a: Array, shape, **kwargs) -> int:
    return a.nbytes


@implements("transpose", ext="tuning.mem")
def transpose(a: Array, axes=None, **kwargs) -> int:
    """Current implementation does not change it inplace, so we need an auxiliar array.
    Maybe we could dampen this cost in the future?
    """
    return 2 * a.nbytes