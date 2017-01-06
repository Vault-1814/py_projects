
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import plot_2d
from _dbus_bindings import Array
from math import pi, factorial
from kinematics import Kinematics
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


# my body is lazzzzy, because its there
def deg2rad(ang):
    for i in range(0, len(ang)):
        ang[i] = ang[i] * pi / 180
    return ang


def rad2deg(ang):
    for i in range(0, len(ang)):
        for j in range(0, len(ang[i])):
            ang[i, j] = round((ang[i, j] * 180 / pi), 5)
    return ang


def rad2deg1d(ang):
    for i in range(0, len(ang)):
        ang[i] = round((ang[i] * 180 / pi), 5)
    return ang


def round_rad(ang):
    for i in range(0, len(ang)):
        for j in range(0, len(ang[i])):
            ang[i, j] = round((ang[i, j]), 3)
    return ang


# Calculation value of polynomial h(t) for itself order,
#   derivative, coefficients (k = (a0, a1, a2 etc.) ) and time
def poly(order, k, t, derivative=0):
    h = 0
    for i in range(derivative, order + 1):
        h += (factorial(i) / factorial(i - derivative)) * k[i] * t ** (i - derivative)
    return h


def show_manipulation_clouds():
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    t1 = numpy.arange(45, 205, 3)
    t2 = numpy.arange(-60, 60, 5)
    x = []
    y = []
    z = []
    for i in t1:
        for j in t2:
            in_q = [i*pi/180, j*pi/180, 0, 0, 0, 0]
            h = ks.forward(in_q)
            x.append(h[0, 3])
            y.append(h[1, 3])
            z.append(h[2, 3])
        print(round(i*100/360), "%")
    ax.plot(x, y, z, "go")
    x = []
    y = []
    z = []
    for i in t1:
        for j in t2:
            in_q = [i*pi/180, 180, j*pi/180-180, 0, 0, 0]
            h = ks.forward(in_q, n=4)
            x.append(h[0, 3])
            y.append(h[1, 3])
            z.append(h[2, 3])
        print(round(i*100/360), "%")
    ax.plot(x, y, z, "bo")
    #ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
    plt.show()


def test_forward_to_inverse():
    ph, th, ps = (7 * pi/13, 0 * pi/180, 5 * pi / 3)
    R06 = ks.get_orientation_matrix(ph, th, ps)
    print(ph, th, ps)
    o = (10, 0, 10)
    out_q = ks.inverse(o, R06)
    print(out_q)
    hh = ks.forward(out_q[0])
    print(round_rad(R06))
    print(round_rad(hh))

    #for y = 0
    #d6 = d[5]
    #r06 = H06[:3, :3]
    #o = H06[:3, 3]
    # points minus height of first link,
    # because it's a flat case of motion manipulator
    #oc = o - numpy.dot(d6 * r06, [0, 0, 1]) - (0, 0, 10)
    #o = o - (0, 0, 10)
    #plot_2d.draw1d(ks.get_dh_d(), in_q, iq=(1, 2, 4), point=oc, point_gripper=o)
    #plot_2d.draw2d(ks.get_dh_d(), out_q, iq=(1, 2, 4), point=oc, point_gripper=o)
    #print(rad2deg(out_q))
    #print("point oc: ", oc)
    #print("point o: ", o)
    #plot_2d.commit()


def trajectory_planning():
    # magic matrix for 4-3-4 trajectory
    C = [
        [1, 1, 0,    0, 0, 0,    0, 0, 0],
        [-3,-4, 1,    0, 0, 0,    0, 0, 0],
        [-3,-6, 0,    1, 0, 0,    0, 0, 0],

        [0, 0, 1,    1, 1, 0,    0, 0, 0],
        [0, 0,-1,   -2,-3, 1,    0, 0, 0],
        [0, 0, 0,   -1,-3, 0,    1, 0, 0],

        [0, 0, 0,    0, 0, 1,    1, 1, 1],
        [0, 0, 0,    0, 0, 1,    2, 2, 4],
        [0, 0, 0,    0, 0, 0,    2, 6, 12],
    ]
    # i, d, a and f points
    o1 = (10, 10, 10)
    o2 = (10, 10, 15)
    o3 = (-10, -10, 15)
    o4 = (-10, -10, 0)
    # Kinematics.get_orientation_matrix(0, 0, 0)
    R06 = ks.get_orientation_matrix(0, 0, 0)
    q_i = ks.inverse(o1, R06)[0]
    q_d = ks.inverse(o2, R06)[0]
    q_a = ks.inverse(o3, R06)[0]
    q_f = ks.inverse(o4, R06)[0]
    hi = ks.forward(q_i)
    hd = ks.forward(q_d)
    ha = ks.forward(q_a)
    hf = ks.forward(q_f)
    # plot points on a diagram
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    x = [hi[0, 3], hd[0, 3], ha[0, 3], hf[0, 3]]
    y = [hi[1, 3], hd[1, 3], ha[1, 3], hf[1, 3]]
    z = [hi[2, 3], hd[2, 3], ha[2, 3], hf[2, 3]]
    ax.plot(x, y, z, "kx")
    SO = []
    for i in range(0, 6):
        b = [q_d[i] - q_i[i], 0, 0, q_a[i] - q_d[i], 0, 0, q_f[i] - q_a[i], 0, 0]
        x = numpy.linalg.solve(C, b)
        # known
        a0 = q_i[i]
        a1 = 0
        a2 = 0
        b0 = q_d[i]
        c0 = q_a[i]
        a = [a0, a1, a2, x[0], x[1]]
        b = [b0, x[2], x[3], x[4]]
        c = [c0, x[5], x[6], x[7], x[8]]
        coefs_poly = [a, b, c]
        exps_poly = [4, 3, 4]
        n = 4
        step = 0.1
        tau = (0, 5, 10, 15)

        # relative time from absolutly
        def get_t(j, i):
            return (j - tau[i-1]) / (tau[i] - tau[i-1])

        time = numpy.arange(tau[0], tau[n-1]+1, step)
        curve = []
        for j in time:
            if tau[0] <= j <= tau[1]:
                i = 0
            elif tau[1] < j <= tau[2]:
                i = 1
            elif tau[2] < j <= tau[3]:
                i = 2
            q = poly(exps_poly[i], coefs_poly[i], get_t(j, i + 1))
            curve.append(q)
        plt.figure(2)
        plt.plot(time, curve, "b")
        plt.grid(True)
        SO.append(curve)
    x = []
    y = []
    z = []
    for i in range(0, 151):
        q = []
        for j in range(0, 6):
            q.append(SO[j][i])
        h = ks.forward(q)
        x.append(h[0, 3])
        y.append(h[1, 3])
        z.append(h[2, 3])
    ax.plot(x, y, z, "g")
    # ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
    plt.show()

# DH parameters
l = 10  # length of link
angle = pi / 2
d = [l, 0, 0, 2 * l, 0, 2 * l]
a = [0, l, 0, 0, 0, 0]
alpha = [angle, 0, angle, -angle, angle, 0]
theta = [0, 0, angle, 0, 0, 0]

ks = Kinematics(a, alpha, d, theta)

#show_manipulation_clouds()
#test_forward_to_inverse()
trajectory_planning()
