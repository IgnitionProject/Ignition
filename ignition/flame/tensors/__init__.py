"""Symbolic tensor library

Provides a small symbolic tensor library for use with flame algorithms.
"""

# Cyclic dependencies require this order.
from tensor_expr import (
    ConformityError, TensorExpr, is_zero, is_outer,
    is_inner, mul_rank, expr_shape, expr_rank)
from tensor import (Tensor)
from basic_operators import (NotInvertibleError, Inner, Inverse, Transpose, T)
from solvers import (all_back_sub, solve_vec_eqn)
from printers import (numpy_print)
