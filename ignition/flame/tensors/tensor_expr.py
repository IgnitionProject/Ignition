from sympy import Add, Expr, Number, Mul, Pow, Symbol

# from tensor import Tensor /* cyclic */
# from functions import Inner, Inverse, Transpose /* cyclic */

class ConformityError (Exception):
    pass

class TensorExpr (Expr):
    """Base object for things with Tensor properties such as:
    * rank
    * shape
    * has_inverse
    * algebraic ops ( + - * / **)
    """
    _op_priority = 20
    rank = -1
    name = None
    has_inverse = False
    shape = None
    is_symmetric = True

    def __mul__ (self, other):
        if is_zero(self) or is_zero(other):
            return Tensor('0', rank=mul_rank(self, other))
        if is_inner(self, other):
            return Inner(self, other)
        return super(TensorExpr, self).__mul__(other)

    def __rmul__ (self, other):
        if is_zero(self) or is_zero(other):
            return Tensor('0', rank=mul_rank(other, self))
        if is_inner(self, other):
            return Inner(self, other)
        return super(TensorExpr, self).__rmul__(other)

    def __add__ (self, other):
        if expr_rank(self) != expr_rank(other):
            raise TypeError("Tensor addition only defined for same rank")
        if is_zero(self):
            return other
        if is_zero(other):
            return self
        return super(TensorExpr, self).__add__(other)

    def __radd__ (self, other):
        if expr_rank(self) != expr_rank(other):
            raise TypeError("Tensor addition only defined for same rank")
        if self.name and self.name.startswith('0'):
            return other
        return super(TensorExpr, self).__radd__(other)

    def __div__ (self, other):
        if is_zero(self):
            raise ZeroDivisionError()
        if isinstance(other, TensorExpr):
            return Mul(self, Inverse(other))
        return super(TensorExpr, self).__div__(other)

    def __rdiv__ (self, other):
        if is_zero(self):
            raise ZeroDivisionError()
        return Mul(other, Inverse(self))

    def __pow__ (self, other):
        if is_zero(self):
            return self
        elif isinstance(other, int) and other < 0:
            return Inverse(self) ** (-other)
        else:
            return Pow(self, other)

    def __rpow__ (self, other):
        raise RuntimeError("Can't raise to the tensor power.")

def is_zero (expr):
    """Returns True, False, or None"""
    if isinstance(expr, Tensor):
        return expr.name.startswith('0')
    if isinstance(expr, Transpose):
        return expr.args[0].is_zero

def is_outer (a, b):
    esa = expr_shape(a)
    esb = expr_shape(b)
    return expr_rank(a) == expr_rank(b) == 1 and \
           esa[0] == esb[1] == 1 and esa[1] == esa[0]

def is_inner (a, b):
    esa = expr_shape(a)
    esb = expr_shape(b)
    return expr_rank(a) == expr_rank(b) == 1 and \
           esa[1] == esb[0] == 1 and esa[0] == esa[1]

def mul_rank (a, b):
    if is_outer(a, b):
        return 2
    era = expr_rank(a)
    erb = expr_rank(b)
    if era == 0 or erb == 0:
        return max(era, erb)
    return era + erb - 2

def expr_shape(expr):
    """Returns the shape of a given expression

    Will raise ConformityError if expression does not conform.
    
    >>> A = Tensor('A', rank=2)
    >>> B = Tensor('B', rank=2)
    >>> x = Tensor('x', rank=1)
    >>> expr_shape(A+B)
    (n, n)
    >>> expr_shape((A+B)*x)
    (n, 1)
    >>> expr_shape(A*T(x))
    ---------------------------------------------------------------------------
    ConformityError                           Traceback (most recent call last)
    """
    if isinstance(expr, TensorExpr):
        return expr.shape
    if isinstance(expr, (Number, Symbol)):
        return (1, 1)
    if isinstance(expr, Add):
        #TODO: Check consistency
        return expr_shape(expr.args[0])
    if isinstance(expr, Mul):
        arg_shapes = map(expr_shape, expr.args)
        arg_shapes = filter(lambda x: x != (1, 1), arg_shapes)
        if len(arg_shapes) == 0:
            return (1, 1)
        for n in xrange(len(arg_shapes) - 1):
            if arg_shapes[n][1] != arg_shapes[n + 1][0]:
                raise ConformityError()
        return (arg_shapes[0][0], arg_shapes[-1][1])
    if isinstance(expr, Pow):
        if expr_rank(expr.args[0]) == 1:
            raise ConformityError()
        return expr_shape(expr.args[0])
    raise NotImplementedError("expr_shape can't handle: %s of type: %s" % \
                              (str(expr), type(expr)))

def expr_rank(expr):
    """Returns the rank of a given expression

    Will raise ConformityError if expression does not conform.
    
    >>> A = Tensor('A', rank=2)
    >>> B = Tensor('B', rank=2)
    >>> x = Tensor('x', rank=1)
    >>> expr_rank(A+B)
    2
    >>> expr_rank((A+B)*x)
    1
    >>> expr_rank(A*T(x))
    ---------------------------------------------------------------------------
    ConformityError                           Traceback (most recent call last)
    """

    if isinstance(expr, TensorExpr):
        return expr.rank
    if isinstance(expr, (Number, int, float)):
        return 0
    if isinstance(expr, Add):
        #TODO: Check consistency
        return expr_rank(expr.args[0])
    if isinstance(expr, Mul):
        arg_shape = expr_shape(expr)
        return sum(map(lambda x: x != 1, arg_shape))
    if isinstance(expr, Pow):
        if isinstance(expr.args[1], (Number, int)):
            base_rank = expr_rank(expr.args[0])
            if expr.args[1] == -1:
                return base_rank
            if base_rank == 0 or base_rank == 2:
                return base_rank
            if base_rank == 1 and expr.args[1] % 2 == 0:
                return 0
            if base_rank == 1:
                return 1
    raise NotImplementedError("expr_rank can't handle: %s of type: %s" % \
                              (str(expr), type(expr)))


from tensor import Tensor #/* cyclic */
from basic_operators import Inner, Inverse, Transpose