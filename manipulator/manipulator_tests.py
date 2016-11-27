from math import pi
from fik import Kinematics
import plot_2d
from mpl_toolkits.mplot3d import Axes3D
import numpy
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm


def deg2rad(ang):
    for i in range(0, len(ang)):
        ang[i] = ang[i] * pi / 180
    return ang


def rad2deg(ang):
    for i in range(0, len(ang)):
        for j in range(0, len(ang[i])):
            ang[i, j] = round((ang[i, j] * 180 / pi), 5)
    return ang


def round_rad(ang):
    for i in range(0, len(ang)):
        for j in range(0, len(ang[i])):
            ang[i, j] = round((ang[i, j]), 5)
    return ang


def show_manipulation_clouds():
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure(1)
    ax = fig.gca(projection='3d')
    t1 = numpy.arange(45, 205, 5)
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
    in_q = [0, 90, 45, 13, 42, 201]
    # print("sets angles: ", in_q)
    print("sets angles: ", deg2rad(in_q))
    print("returns angles: ")

    H06 = ks.forward(in_q)
    out_q = ks.inverse(H06)

    d6 = d[5]
    r06 = H06[:3, :3]
    o = H06[:3, 3]
    # points minus height of first link,
    # because it's a flat case of motion manipulator
    oc = o - numpy.dot(d6 * r06, [0, 0, 1]) - (0, 0, 10)
    o = o - (0, 0, 10)

    plot_2d.draw1d(ks.get_dh_d(), in_q, iq=(1, 2, 4), point=oc, point_gripper=o)
    plot_2d.draw2d(ks.get_dh_d(), out_q, iq=(1, 2, 4), point=oc, point_gripper=o)

    print(rad2deg(out_q))
    print("point oc: ", oc)
    print("point o: ", o)
    plot_2d.commit()

# DH parameters
l = 10  # length of link
angle = pi / 2
d = [l, 0, 0, 2 * l, 0, 2 * l]
a = [0, l, 0, 0, 0, 0]
alpha = [angle, 0, angle, -angle, angle, 0]
theta = [0, 0, angle, 0, 0, 0]

ks = Kinematics(l, a, alpha, d, theta)

test_forward_to_inverse()
#show_manipulation_clouds()