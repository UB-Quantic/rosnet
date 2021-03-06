import numpy as np
from rosnet.core import log
from rosnet.tuning.task import autotune


@autotune(returns=1)
@log.trace
def full(shape, value, dtype, order="F"):
    return np.full(shape, value, dtype, order)


@autotune(returns=1)
@log.trace
def rand(shape, order="F"):
    return np.asarray(np.random.random_sample(shape), order=order)


@autotune(returns=1)
@log.trace
def identity(block_shape, n, i, j, dtype):
    block = np.zeros(block_shape, dtype)

    diag = np.intersect1d(*[np.arange(idx * bs, min(n, (idx + 1) * bs)) for idx, bs in zip([i, j], block_shape)])

    i_ones, j_ones = [diag - idx * bs for idx, bs in zip([i, j], block_shape)]

    block[i_ones, j_ones] = 1

    return block
