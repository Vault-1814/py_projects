import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos

m = 60
plt.xlim(-m, m)
plt.ylim(-m, m)
plt.hlines(0, -m, m)
plt.vlines(0, -m, m)
plt.grid(True)


def f(l, angle, x0, y0):
    # d**2 = (x - x0)**2 + (y - y0)**2
    if l == 0:
        l = 10
    oy = l * sin(angle) + y0
    ox = l * cos(angle) + x0
    return ox, oy


def draw2d(l, q, iq=(1, 2, 4), point=[0, 0, 0], point_gripper=[0, 0, 0]):
    subplot = 221
    qty_points = len(iq) + 1
    for k in range(0, len(q)):
        x = np.zeros(qty_points)
        y = np.zeros(qty_points)
        sum_angles = 0
        for i in range(1, qty_points):
            sum_angles += q[k, iq[i - 1]]
            x[i], y[i] = f(l[iq[i - 1] + 1], sum_angles, x[i - 1], y[i - 1])
        plt.figure(2)
        plt.subplot(subplot)
        plt.xlim(-m, m)
        plt.ylim(-m, m)
        plt.hlines(0, -m, m)
        plt.vlines(0, -m, m)
        plt.grid(True)
        subplot = subplot + 1
        plt.plot((0, 0), (0, -10), 'g', (0, 0), (0, -10), 'bo', linewidth=3.0)
        plt.plot(x, y, 'g', x, y, 'bo', linewidth=3.0)
        title = "Configuration %d" % (k+1)
        plt.title(title)
        if k % 2 == 0:
            plt.plot(point[0], point[2], 'ro')
            plt.plot(point_gripper[0], point_gripper[2], 'mo')
        else:
            plt.plot(-point[0], point[2], 'ro')
            plt.plot(-point_gripper[0], point_gripper[2], 'mo')


def draw1d(l, q, iq=(1, 2, 4), point=[0, 0, 0], point_gripper=[0, 0, 0]):
    qty_points = len(iq) + 1
    x = np.zeros(qty_points)
    y = np.zeros(qty_points)
    # i am indian *_+
    sum_angles = 0
    for i in range(1, qty_points):
        sum_angles += q[iq[i-1]]
        x[i], y[i] = f(l[iq[i-1]+1], sum_angles, x[i-1], y[i-1])
        # print(q[iq[i-1]], theta[iq[i-1]])
    plt.figure(1)
    # plt.subplot(subplot)
    plt.plot((0, 0), (0, -10), 'g', (0, 0), (0, -10), 'bo', linewidth=3.0)
    plt.plot(x, y, 'g', x, y, 'bo', linewidth=3.0)
    plt.title("Sets angles")
    plt.plot(point[0], point[2], 'ro')
    plt.plot(point_gripper[0], point_gripper[2], 'mo')


def commit():
    plt.show()
