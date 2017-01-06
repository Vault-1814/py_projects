from __future__ import division
from IPython.display import display

from sympy import Matrix
from sympy.interactive import printing

printing.init_printing(use_latex='mathjax')

import sympy as sym
from sympy import *

q1, q2 = symbols("q1 q2")
dq1, dq2 = symbols("\dot{q}_1 \dot{q}_2")
ddq1, ddq2 = symbols("\ddot{q}_1 \ddot{q}_2")
w0, w1, w2 = symbols("\omega_0 \omega_1 \omega_2")
dw0, dw1, dw2 = symbols("\dot\omega_0 \dot\omega_1 \dot\omega_2")
z0, z1, z2 = symbols("z0 z1 z2")
a0, a1, a2, ac1, ac2 = symbols("a0 a1 a2 a_{c1} a_{c2}")
f1, f2, f3 = symbols("f1 f2 f3")
tau1, tau2, tau3 = symbols("\tau_1 \tau_2 \tau_3")
J1, J2 = symbols("J1 J2")
l1, l2, r1, r2 = symbols("l1 l2 r1 r2")
g = symbols("g")
m1, m2 = symbols("m1 m2")
r01 = Matrix([[l1], [0], [0]])
r12 = Matrix([[l2], [0], [0]])
r1c1 = Matrix([[-(l1 - r1)], [0], [0]])
r2c2 = Matrix([[-(l2 - r2)], [0], [0]])
z0 = z1 = z2 = Matrix([[0], [0], [1]])
rl1, rl2 = symbols("r_1^l r_2^l")
J1 = Matrix([[m1 * rl1 ** 2 / 2, 0, 0],
             [0, m1(3 * rl1 ** 2 + l1 ** 2) / 12 + m1 * rl1 ** 2, 0],
             [0, 0, m1(3 * rl1 ** 2 + l1 ** 2) / 12 + m1 * rl1 ** 2]])
J2 = Matrix([[m2 * rl2 ** 2 / 2, 0, 0],
             [0, m2(3 * rl2 ** 2 + l2 * 2) / 12 + m2 * rl2 ** 2, 0],
             [0, 0, m2(3 * rl2 ** 2 + l2 * 2) / 12 + m2 * rl2 ** 2]])
R01 = Matrix([[cos(q1), -sin(q1), 0], [sin(q1), cos(q1), 0], [0, 0, 1]])
R12 = Matrix([[cos(q2), -sin(q2), 0], [sin(q2), cos(q2), 0], [0, 0, 1]])

w0 = Matrix([[0], [0], [0]])
dw0 = Matrix([[0], [0], [0]])
a0 = Matrix([[0], [g], [0]])
w1 = R01.T * (w0 + dq1 * z0)
dw1 = R01.T * (dw0 + ddq1 * z0 - dq1 * w0.cross(z0))
a1 = R01.T * a0 + dw1.cross(r01) + w1.cross(w1.cross(r01))
ac1 = a1 + dw1.cross(r1c1) + w1.cross(w1.cross(r1c1))

w2 = R12.T * (w1 + dq2 * z1)
dw2 = R12.T * (dw1 + ddq2 * z1 - dq2 * w1.cross(z1))
a2 = R12.T * a1 + dw2.cross(r12) + w2.cross(w2.cross(r12))
ac2 = a2 + dw2.cross(r2c2) + w2.cross(w2.cross(r2c2))
f3 = Matrix([[0], [0], [0]])
tau3 = Matrix([[0], [0], [0]])
f2 = f3 + m2 * ac2
tau2 = tau3 - f2.cross(r12 + r2c2) + f3.cross(r2c2) + J2 * dw2 + w2.cross(J2 * w2)
f1 = f2 + m1 * ac1
tau1 = tau2 - f1.cross(r01 + r1c1) + f2.cross(r1c1) + J1 * dw1 + w1.cross(J1 * w1)
