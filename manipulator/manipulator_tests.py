from math import pi
from fik import Kinematics


def deg2rad(ang):
    for i in range(0, len(ang)):
        ang[i] = ang[i] * pi / 180
    return ang


def rad2deg(ang):
    for i in range(0, len(ang)):
        for j in range(0, len(ang[i])):
            ang[i, j] = round((ang[i, j] * 180 / pi), 5)
    return ang

# DH parameters
l = 10  # length of link
angle = pi / 2
d = [l, 0, 0, 2 * l, 0, 2 * l]
a = [0, l, 0, 0, 0, 0]
alpha = [angle, 0, angle, -angle, angle, 0]
theta = [0, 0, angle, 0, 0, 0]

ks = Kinematics(l, a, alpha, d, theta)

in_q = [0, 0, 90, 45, 1, 33]
print("sets angles: ", in_q)
print("returns angles: ")
H06 = ks.forward(deg2rad(in_q))
out_q = ks.inverse(H06)

print(rad2deg(out_q))
