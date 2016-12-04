from _dbus_bindings import Array
from math import pi, factorial
from fik import Kinematics
import plot_2d
from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
import math


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


def poly(order, k, t, derivative=0):
    h = 0
    for i in range(derivative, order + 1):
        h += (factorial(i) / factorial(i - derivative)) * k[i] * t ** (i - derivative)
    return h


def show_manipulation_clouds():
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    t1 = numpy.arange(45, 205, 1)
    t2 = numpy.arange(-60, 60, 5)
    x = []
    y = []
    z = []
    for i in t1:
        #for j in t2:
        in_q = [i*pi/180, math.sin(i), 0, 0, 0, 0]
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
    #ax.plot(x, y, z, "bo")
    #ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
    plt.show()


def test_forward_to_inverse():
    #in_q = [45, 90, 45, 13, 42, 210]
    # print("sets angles: ", in_q)

    H06 = ks.get_orientation_matrix(7 * pi/13, 0 * pi/180, 5 * pi / 3)
    print(7 * pi/13, 0 * pi/180, 5 * pi / 3)
    R06 = H06[:3, :3]
    o = (0, -1, 20)
    out_q = ks.inverse(o, R06)
    print(out_q)
    hh = ks.forward(out_q[0])

    print(round_rad(R06))
    print(round_rad(hh))

    #print(out_q)
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

    t1 = 1
    t2 = 1
    tn = 1

    v_0 = 0
    a_0 = 0
    v_1 = 1
    a_1 = 1
    v_2 = 1
    a_2 = 1
    v_n = 0
    q_0 = deg2rad([10, 0, 0, 0, 0, 0])
    q_1 = deg2rad([30, 20, 1, 0, 1, 0])
    q_2 = deg2rad([40, 70, 5, 0, 5, 0])
    q_n = deg2rad([45, 90, 10, 0, 10, 0])

    h0 = ks.forward(q_0)
    h1 = ks.forward(q_1)
    h2 = ks.forward(q_2)
    hn = ks.forward(q_n)

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    x = [h0[0,3], h1[0,3], h2[0,3], hn[0,3]]
    y = [h0[1,3], h1[1,3], h2[1,3], hn[1,3]]
    z = [h0[2,3], h1[2,3], h2[2,3], hn[2,3]]
    ax.plot(x, y, z, "kx")


#    q_0 = ks.inverse(h0)[0]
#    q_1 = ks.inverse(h1)[0]
#    q_2 = ks.inverse(h2)[0]
#    q_n = ks.inverse(hn)[0]


    SO = []

    for i in range(0, 6):
        a0 = q_0[i]
        a1 = v_0 * t1
        a2 = a_0 * t1**2 / 2
        a3 = 4 * q_1[i] - v_1 * t1 - 2 * a2 - 3 * a1 - 4 * a0
        a4 = -3 * q_1[i] + v_1 * t1 + a2 + 2 * a1 + 3 * a0

        b0 = q_1[i]
        b1 = v_1 * t2
        b2 = a_1 * t2**2 / 2
        b3 = q_2[i] - b0 - b1 - b2

        c0 = q_2[i]
        c1 = v_2 * tn
        c2 = a_2 * tn**2 / 2
        c3 = 4 * q_n[i] - v_n * tn - 2 * c2 - 3 * c1 - 4 * c0
        c4 = -3 * q_n[i] + v_n * tn + c2 + 2 * c1 + 3 * c0

        a = [a0, a1, a2, a3, a4]
        b = [b0, b1, b2, b3]
        c = [c0, c1, c2, c3, c4]

        curve0_1 = []
        curve1_2 = []
        curve2_n = []
        t = numpy.arange(0, 0.1, 0.001)
        for j in t:
            q1 = poly(4, a, j)
            q2 = poly(3, b, j+0.1)
            qn = poly(4, c, j+0.2)
            curve0_1.append(q1)
            curve1_2.append(q2)
            curve2_n.append(qn)
        curve_i = curve0_1 + curve1_2 + curve2_n
        SO.append(curve_i)
        print(SO)

    x = []
    y = []
    z = []
    for i in range(0, 300):
        q = []
        for j in range(0, 6):
            q.append(SO[j][i])
        h = ks.forward(q)
        x.append(h[0, 3])
        y.append(h[1, 3])
        z.append(h[2, 3])
    ax.plot(x, y, z, "g")
    #ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
    plt.show()



# DH parameters
l = 10  # length of link
angle = pi / 2
d = [l, 0, 0, 2 * l, 0, 2 * l]
a = [0, l, 0, 0, 0, 0]
alpha = [angle, 0, angle, -angle, angle, 0]
theta = [0, 0, angle, 0, 0, 0]

ks = Kinematics(l, a, alpha, d, theta)

#trajectory_planning()
test_forward_to_inverse()
#show_manipulation_clouds()

