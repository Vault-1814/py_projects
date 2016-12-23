import numpy
from numpy import pi, transpose, dot, eye, zeros, cross
from fik import Kinematics
from ht import *
import fik

n = 2
g = zeros((3, n))
g[1, :] = 9.81
# LINKS
#   mass
m1 = 1
m2 = 1
m = [m1, m2]
#   length
l1 = 1
l2 = 1
l = [l1, l2]
#   height = width = diameter
diameter1 = 0.05
diameter2 = 0.05
diameter = [diameter1, diameter2]
#   centers of mass
r1 = l1 / 2
r2 = l2 / 2
r = [r1, r2]
# DH parameters
a = [l1, l2]
alpha = [0, 0]
d = [0, 0]
theta = [0, 0]

# vectors for links
vec_r = zeros((3, n))
vec_rc = zeros((3, n))
vec_r[0, :] = l
vec_rc[0, :] = r

# axis of rotation
z = zeros((3, 3))
z[2, :] = 1


# returns tensor of inertia for center of mass of the link
def I(m, l, r):
    Icf = zeros((3, 3))
    Icf[0, 0] = m * r**2 / 2
    Icf[1, 1] = m * (3 * r**2 + l**2) / 12
    Icf[2, 2] = Icf[1, 1]
    return Icf


# returns tensor of inertia for offset d
def J(Icf, m, d):
    kronecker = lambda x, y: 1 if x == y else 0
    Jff = zeros((3, 3))
    for i in range(0, 3):
        for j in range(0, 3):
            Jff[i, j] = Icf[i, j] + m * (dot(a, a) * kronecker(i, j) + a[i] * a[j])
    return Jff


# !!! the i must be less then j
# ^iH_j
def H(ks, q, i, j):
    H0i = ks.forward(q, i)
    H0j = ks.forward(q, j)
    Hij = transpose(H0i).dot(H0j)
    return Hij


# !!! the i must be less then j
# ^iR_j
def R(ks, q, i, j):
    return H(ks, q, i, j)[:3, :3]


def NE(q, dq, ddq, ks):
    omega = zeros((3, n+1))
    dOmega = zeros((3, n + 1))
    a = zeros((3, n + 1))
    ac = zeros((3, n + 1))
    f = zeros((3, n + 2))
    tau = zeros((3, n + 2))
    u = zeros((3, n + 2))

    for i in range(1, n+1):
        transposedR = transpose(R(ks, q[i], i-1, i))
        omega[:, i] = transposedR.dot(omega[:, i-1] + dq[i] * z[:, i-1])
        dOmega[:, i] = transposedR.dot(dOmega[:, i-1] + ddq[i] * z[:, i-1] + cross(dq[i] * omega[:, i-1], z[:, i-1]))
        # vec_r[:, i-1] because len(vec_r) == 2 and index of first element is equals to 0 and i start from 1
        a[:, i] = transposedR.dot(a[:, i-1] + cross(dOmega[:, i], vec_r[:, i-1]) +
                                  cross(omega[:, i], cross(omega[i], vec_r[:, i-1])))
        ac[:, i] = a[:, i] + cross(dOmega[i], vec_rc[:, i-1]) + cross(omega[i], cross(omega[i], vec_rc[:, i-1]))
    for i in range(n, 0):
        Icf = I(m[i], l[i], diameter[i] / 2)
        # vector for tensor inertia in fixed frame
        vec_offset = [-r[i], 0, 0]
        Jff = J(Icf, m[i], vec_offset)
        f[i] = f[i-1] + m[i-1] * (ac[:, i] - g[i-1])
        tau[i] = tau[i+1] - cross(f[i], (vec_r[:, i-1] + vec_rc[:, i-1])) + cross(f[i+1], vec_rc[:, i-1]) + \
                 Jff.dot(dOmega[i]) + cross(omega[i], (Jff.dot(omega[i])))
        u[i] = transpose(tau[i]) * z[:, i-1]
    return omega, dOmega, a, ac, f, tau, u

