from typing import Tuple

import numpy as np
from pycompss.api.parameter import IN
from rosnet.core import log
from rosnet.core.interface import Array
from rosnet.tuning.task import autotune


@autotune(a=IN, returns=3)
@log.trace
def svd(a: Array, full_matrices=False, hermitian=False) -> Tuple[Array, Array, Array]:
    return np.linalg.svd(a, full_matrices=full_matrices, compute_uv=True, hermitian=hermitian)


@autotune(a=IN, returns=1)
@log.trace
def svd_vals(a: Array, hermitian=False) -> Array:
    return np.linalg.svd(a, full_matrices=False, compute_uv=False, hermitian=hermitian)


@autotune(a=IN, returns=2)
@log.trace
def svd_matrix(a: Array, full_matrices=False, hermitian=False) -> Tuple[Array, Array]:
    U, s, Vt = np.linalg.svd(a, full_matrices=full_matrices, compute_uv=True, hermitian=hermitian)
    U = U @ np.diag(s)
    return (U, Vt)
