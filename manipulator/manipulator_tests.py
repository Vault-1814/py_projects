from math import pi
from fik import Kinematics
import plot_2d
import numpy

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


# DH parameters
l = 10  # length of link
angle = pi / 2
d = [l, 0, 0, 2 * l, 0, 2 * l]
a = [0, l, 0, 0, 0, 0]
alpha = [angle, 0, angle, -angle, angle, 0]
theta = [0, 0, angle, 0, 0, 0]

ks = Kinematics(l, a, alpha, d, theta)

in_q = [0, 10, 10, 10, 10, 10]
#print("sets angles: ", in_q)
print("sets angles: ", deg2rad(in_q))
print("returns angles: ")

H06 = ks.forward(in_q)

out_q = ks.inverse(H06)

d6 = d[5]
r06 = H06[:3, :3]
# points minus height of first link
o = H06[:3, 3]
oc = o - numpy.dot(d6 * r06, [0, 0, 1]) - (0, 0, 10)
o = o - (0, 0, 10)
print(oc)

plot_2d.draw1d(ks.get_dh_d(), ks.get_dh_theta(), in_q, iq=(1, 2, 4), point=oc, point_gripper=o)
plot_2d.draw2d(ks.get_dh_d(), ks.get_dh_theta(), out_q, iq=(1, 2, 4), point=oc, point_gripper=o)
H06 = ks.forward(in_q)

out_q = ks.inverse(H06)
print(rad2deg(out_q))
plot_2d.commit()


