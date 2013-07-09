import os

from mako.lookup import TemplateLookup

from ignition.flame.printing import LatexWorksheetPrinter


def test_flatex_template ():
    cg = {}
    cg["outputs"] = r"""$X,R,P,D,U$"""
    cg["sizes"] = r"""$m\times n$"""
    cg["operation"] = r"""$A\underbar {PD}=R(I-J)$, $\underbar{PD}=X(I-J)$,
  $P(I-U)=M\inv R, R^tM\inv R=\Omega$,
  $D,\Omega$~diagonal and $U$~strictly upper triangular, and $R
  e_0=Ax_0-b$"""
    cg["precondition"] = r"""$ R e_0 = Ax_0-b$"""
    cg["postcondition"] = r"""$A\underbar {PD}=R(I-J) \wedge
  P(I-U)=M\inv R \wedge R^tM\inv R=\Omega 
  \wedge K e_0=b$ with $D,\Omega$ diagonal
  and $U$~strictly upper triangular"""
    cg["partition"] = r"""
  $ 
  R \rightarrow \FLAOneByThreeII RrR,\quad\mbox{$P$ similarly;}\quad
  J \rightarrow \FLAThreeByThreeII {J_{TL}}00 {\er^t}00 0{e_0}{J_{BR}},
  \quad\mbox{$U,D$ similarly}
  $
"""
    cg["partition_sizes"] = r"""$n(r_M) = n(p_M)=n(d_{MM})=1$"""
    cg["repartition"] = r"""
  $
  \begin{array}{l}
    \FLAOneByThreeII RrR \rightarrow \\[4pt]
     \FLAOneByFourIIi RrrR\\ \mbox{$P$ similar}
  \end{array}
  $,\kern1em\penalty0 
  $ 
  \FLAThreeByThreeII{J_{TL}}00 {j_{ML}^t}00 0{j_{MR}}{J_{BR}}\rightarrow
  \left( \begin{array}{ c I c I c | c}
  {J_{00}} & 0 & 0 & 0 \\ \whline
  {\er^t} & 0 & 0 & 0  \\ \whline
  0 & 1 & 0 & 0 \\ \hline
  0 & 0 & {e_0} & {J_{33}}
  \end{array}
  \right),\quad\mbox{$U,D$ similar}
  $
"""
    cg["repartition_sizes"] = r"""$n(r_2)=n(p_2)=n(d_{22})=1$"""
    cg["fuse"] = r"""
  $
  \begin{array}{l}
    \FLAOneByThreeII RrR \leftarrow \\[4pt]
    \FLAOneByFouriII RrrR\\ \mbox{$P$ similar}
  \end{array}
  $,\kern1em\penalty0 
  $ 
  \FLAThreeByThreeII{J_{TL}}00 {j_{ML}^t}00 0{j_{MR}}{J_{BR}}\leftarrow
  \left( \begin{array}{ c | c I c I c}
  {J_{00}} & 0 & 0 & 0 \\ \hline
  {\er^t} & 0 & 0 & 0  \\ \whline
  0 & 1 & 0 & 0 \\ \whline
  0 & 0 & {e_0} & {J_{33}}
  \end{array}
  \right),\quad\mbox{$U,D$ similar}
  $
"""
    cg["guard"] = r"""$ n(R_R) > 0 $"""
    cg["invariant"] = r"""
  $
  AP_LD_{LL}=R_LJ_{TL}+r_M \er^t 
    \wedge \FLAOneByTwoo{P_L}{p_M}=\FLAOneByTwoo{R_L}{r_M}
           \FLATwoByTwoo{I-U_{TL}}{-u_{TM}} 01
    \wedge \FLAOneByTwoo{ R_L }{ r_M } e_0 = b 
  $
"""
    cg["before_update"] = r"""
  $
  AP_0D_0=R_0J_{00}-r_1 e_r^t 
  \wedge P_0U_{00}=R_0 \wedge P_0u_{01}+p_1=r_1
  \wedge R_0^tR_0=\Omega_0 \wedge R_0^tr_1=0 \wedge r_1^tr_1=\omega_1
  \wedge R_0 e_0 = b 
  $
"""
    cg["after_update"] = r"""
  $
  \begin{array}{l}
    A
    \begin{pmatrix}  P_0&p_1\end{pmatrix}
    \begin{pmatrix}  D_0\\&d_1\end{pmatrix}
    =
    \begin{pmatrix}  R_0& r_1&r_2\end{pmatrix}
    \begin{pmatrix}  J_{00}\\ j_{10}^t&1\\ 0&-1\end{pmatrix}
    \\ [4pt]
    \wedge
    \FLAOneByThreeood Ppp \FLAThreeByThreeood Uuu 01u 001 =
    \FLAOneByThreeood Rrr
    \\ [4pt]
    \wedge
    \begin{pmatrix}  R_0^t\\ r_1^t\\ r_2^t\end{pmatrix}
    \begin{pmatrix}  R_0&r_1&r_2\end{pmatrix} =
    \begin{pmatrix}\Omega_0&0&0\\ 0&\omega_1&0\\ 0&0&\omega_2  \end{pmatrix}
    \wedge
    \begin{pmatrix}
      P_0^tAP_0&P_0^tAp_1&P_0^tAp_2\\ p_1^tAP_0&p_1^tAp_1&p_1^tAp_2 \\
      p_2^tAP_0&p_2^tAp_1&p_2^tAp_2 \end{pmatrix}=
    \begin{pmatrix}
    P_0^tAP_0&0&0\\ p_1^tAP_0&p_1^tAp_1&0 \\
    p_2^tAP_0&p_2^tAp_1&p_2^tAp_2 \end{pmatrix}
  \end{array}
  $
"""
    cg["update"] = r"""
  $d_1\leftarrow r_1^tr_1/r_1^tAp_1$, 
  $r_2\leftarrow r_1-Ap_1d_1$, 
  $u_{12}=r_2^tr_2/r_1^tr_1$,
  $p_2\leftarrow r_2-p_1u_{12}$
"""
    cg["caption"] = r"""Worksheet for the Conjugate Gradient method"""
    cg["label"] = r"""cg-worksheet"""

    my_dir = os.path.dirname(__file__)
    template_dir = os.path.join(my_dir, "..", "templates")
    mylookup = TemplateLookup(template_dir)
    t = mylookup.get_template("flatex.mako")
    gold = open(os.path.join(my_dir, "cg_gold.tex")).read()
    assert(t.render(**cg) == gold)
