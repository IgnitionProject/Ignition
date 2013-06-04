from ignition.utils.code_obj import CodeObj, Statement, Variable, FunctionNode, LoopNode


def create_sum_squares():
    """Returns a code dag for sum of squares."""
    num_squares = Variable('N', var_type="int")
    sum_var = Variable('sum_var', var_type="int")

    sum_squares = FunctionNode('sum_squares', ret_type="int", inputs=[num_squares], output=sum_var)
    sum_squares.add_object(sum_var)
    sum_squares.add_statement("=", sum_var, 0)
    floop = LoopNode(kind='for', init=1, test=num_squares + 1, inc=1)
    s1 = Statement("*", floop.idx, floop.idx)
    floop.add_statement("+=", sum_var, s1)
    sum_squares.add_object(floop)
    code_dag = CodeObj().add_object(sum_squares)
    return code_dag


def test_for_loop_sum_squares():
    """Test for creating \sum_{i=1}^N i*i"""
    create_sum_squares()  # Should raise exception if fails.


def create_double_sum():
    """Returns dag for double sum"""
    N = Variable('N', var_type='int')
    tmp = Variable('tmp', var_type='int')
    sum_var = Variable('sum_var', var_type='int')

    double_sum = FunctionNode('double_sum', ret_type='int', inputs=[N], output=sum_var)
    double_sum.add_object(sum_var)
    double_sum.add_statement('=', sum_var, 0)
    outer_loop = LoopNode(kind='for', init=1, test=N+1, inc=1)
    outer_loop.add_object(tmp)
    outer_loop.add_statement('=', tmp, 0)
    inner_loop = LoopNode(kind='for', init=1, test=outer_loop.idx+1, inc=1)
    inner_loop.add_statement('+=', tmp, Statement('*', inner_loop.idx, inner_loop.idx))
    outer_loop.add_object(inner_loop)
    outer_loop.add_statement('+=', sum_var, tmp)
    double_sum.add_object(outer_loop)
    return CodeObj().add_object(double_sum)

def test_double_for_loop():
    """Test for creating a double sum"""
    create_double_sum() # Should raise exception if fails.
