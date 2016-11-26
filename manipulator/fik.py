#!/bin/env python
"""
    solving forward and inverse kinematics problems
"""
from numpy import identity, dot, sign, transpose
import numpy
from math import pi, cos, sin, atan2, sqrt
from ht import translation_matrix, rotation_matrix, concatenate_matrices


class Kinematics:

    def __init__(self, l, a, alpha, d, theta):
        self.l = l
        self.a = a
        self.alpha = alpha
        self.d = d
        self.theta = theta

    def set_length_link(self, l):
        self.l = l

    def set_dh_parameters(self, a, alpha, d, theta):
        self.a = a
        self.alpha = alpha
        self.d = d
        self.theta = theta

    # forward kinematics
    def forward(self, q, n=6):
        h = identity(4)
        for i in range(0, n):
            rz = rotation_matrix(q[i] + self.theta[i], (0, 0, 1))
            tz = translation_matrix((0, 0, self.d[i]))
            tx = translation_matrix((self.a[i], 0, 0))
            rx = rotation_matrix(self.alpha[i], (1, 0, 0))
            a = concatenate_matrices(rz, tz, tx, rx)
            h = concatenate_matrices(h, a)
        return h

    # inverse kinematics
    def inverse(self, h):
        q = numpy.zeros(24)
        q.shape = (4, 6)
        d6 = self.d[5]
        a2 = self.a[1]
        a3 = 2 * self.a[1]
        r06 = h[:3, :3]
        o = h[:3, 3]
        oc = o - dot(d6 * r06, [0, 0, 1])
        xc, yc, zc = oc
        # position problem
        s = zc - self.d[0]
        r = sqrt(xc**2 + yc**2)
        d = (s**2 + r**2 - a2**2 - a3**2) / (2 * a2 * a3)
        q[0, 0] = q[1, 0] = atan2(yc, xc)
        q[2, 0] = q[3, 0] = pi + atan2(yc, xc)

        q[0, 2] = q[1, 2] = atan2(sqrt(abs(1 - d**2)), d)
        q[2, 2] = q[3, 2] = atan2(-sqrt(abs(1 - d**2)), d)

        q[0, 1] = atan2(s, r) - atan2(2 * a2 * sin(q[0, 2]), a2 + a3 * cos(q[0, 2]))
        q[1, 1] = pi - atan2(s, r) + atan2(2 * a2 * sin(q[0, 2]), a2 + a3 * cos(q[0, 2]))
        q[2, 1] = atan2(s, r) - atan2(2 * a2 * sin(q[1, 2]), a2 + a3 * cos(q[1, 2]))
        q[3, 1] = pi - atan2(s, r) + atan2(2 * a2 * sin(q[1, 2]), a2 + a3 * cos(q[1, 2]))

        # orientation problem
        def solve_orientation(r36, i=0):
            eps = numpy.finfo(numpy.float).eps
            if abs(r36[0, 2]) > 10 * eps and r36[0, 2] != r36[1, 2]:
                q[i, 4] = atan2(sqrt(abs(1 - r36[2, 2])), r36[2, 2])
                q[i, 3] = atan2(r36[1, 2], r36[0, 2])
                q[i, 5] = atan2(r36[2, 1], -r36[2, 0])
                q[i+1, 4] = atan2(-sqrt(abs(1 - r36[2, 2])), r36[2, 2])
                q[i+1, 3] = atan2(-r36[1, 2], -r36[0, 2])
                q[i+1, 5] = atan2(-r36[2, 1], r36[2, 0])
            else:
                print("!psi + phi!")
                if r36[2, 2] > eps:
                    q[i, 4] = 0
                    q[i+1, 4] = 0
                    # any
                    q[i, 3] = 0
                    q[i, 5] = pi
                    q[i+1, 5] = 0
                    q[i+1, 3] = pi
                else:
                    q[i, 4] = pi
                    q[i+1, 4] = pi
                    # any
                    q[i, 3] = 0
                    q[i, 5] = pi
                    q[i+1, 5] = 0
                    q[i+1, 3] = pi

        h03 = self.forward(q[0], n=3)
        r03 = h03[:3, :3]
        r36 = dot(transpose(r03), r06)
        solve_orientation(r36, 0)
        solve_orientation(r36, 2)
        return q

