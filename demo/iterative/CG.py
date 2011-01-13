"""Implements the complete conjugant gradient examples."""

from numpy import matrix

from ignition.flame import *
from ignition.utils import flatten_list

# Define the operation
def CG_Op (A, X, P, I, U, J, D, R, O):
    return [X * (I + U) - P * D,
            A * P * D - R * (I + U),
            P * (I - J) - R,
            T(R) * R - O]

# Define the loop invariant
def CG_Inv (A, X, P, I, U, J, D, R, O):
    [A] = A
    [X_l, x_m, X_r] = X
    [P_l, p_m, P_r] = P
    [[I_tl, _, _],
     [_, o, _],
     [_, _, I_br]] = I
    [[U_tl, u_tm, U_tr],
     [_, u_mm, t_u_mr],
     [_, _, U_br]] = U
    [[J_tl, _, _],
     [T_m_j_ml, _, _],
     [_, j_bm, J_br]] = J
    [[D_l, _, _],
     [_, d_m, _],
     [_, _, D_r]] = D
    [R_l, r_m, R_t] = R
    eqns = [A * P_l * D_l - R_l * (I_tl - J_tl) - r_m * T_m_j_ml,
            P_l * D_l - X_l * (I_tl - J_tl) - x_m * T_m_j_ml,
            P_l * (I_tl + U_tl) - R_l,
            P_l * u_tm + p_m - r_m,
            T(R_l) * r_m,
            T(r_m) * R_l,
            T(P_l) * A * p_m]

    known = [one,
            Zero,
            I_tl,
            U_tr,
            u_mm]

    print "U_tr:", U_tr
#    print "P_l:", P_l
#    print "I_U_tl:", I_tl
#    print "R_l:", R_l
#    print  "P_l * I_U_tl - R_l", pprint.pformat(P_l * I_tl - R_l)
    def unroll_mats(acc, eqn):
        if isinstance(eqn, matrix):
            return acc + flatten_list(eqn.tolist())
        else:
            return acc + [eqn]

    eqns = reduce(unroll_mats, eqns, [])
    return eqns, reduce(unroll_mats, known, [])

# Define the Partition Objs
A = PObj(Tensor("A", rank=2),
         part_fun=Part_1x1(),
         repart_fun=Repart_1x1(),
         fuse_fun=Fuse_1x1(),
         arg_src=PObj.ARG_SRC.Input)
X = PObj(Tensor("X", rank=2),
         part_fun=Part_1x3(),
         repart_fun=Repart_1x3(),
         fuse_fun=Fuse_1x3(),
         arg_src=PObj.ARG_SRC.Overwrite)
P = PObj(Tensor("P", rank=2),
         part_fun=Part_1x3(),
         repart_fun=Repart_1x3(),
         fuse_fun=Fuse_1x3(),
         arg_src=PObj.ARG_SRC.Computed)
I = PObj(Tensor("I", rank=2),
         part_fun=Part_I_3x3(),
         repart_fun=Repart_I_3x3(),
         fuse_fun=Fuse_I_3x3(),
         arg_src=PObj.ARG_SRC.Computed)
U = PObj(Tensor("U", rank=2),
         part_fun=Part_Upper_3x3(),
         repart_fun=Repart_Upper_3x3(),
         fuse_fun=Fuse_Upper_3x3(),
         arg_src=PObj.ARG_SRC.Computed)
J = PObj(Tensor("J", rank=2),
         part_fun=Part_J_3x3(),
         repart_fun=Repart_J_3x3(),
         fuse_fun=Fuse_J_3x3(),
         arg_src=PObj.ARG_SRC.Computed)
D = PObj(Tensor("D", rank=2),
         part_fun=Part_Diag_3x3(),
         repart_fun=Repart_Diag_3x3(),
         fuse_fun=Fuse_Diag_3x3(),
         arg_src=PObj.ARG_SRC.Computed)
R = PObj(Tensor("R", rank=2),
         part_fun=Part_1x3(),
         repart_fun=Repart_1x3(),
         fuse_fun=Fuse_1x3(),
         arg_src=PObj.ARG_SRC.Computed)
O = PObj(Tensor("O", rank=2),
         part_fun=Part_1x3(),
         repart_fun=Repart_1x3(),
         fuse_fun=Fuse_1x3(),
         arg_src=PObj.ARG_SRC.Computed)

# Generate the algorithm
generate(op=CG_Op, loop_inv=CG_Inv,
         inv_args=[A, X, P, I, U, J, D, R, O],
         updater=tensor_updater, filetype="text")
