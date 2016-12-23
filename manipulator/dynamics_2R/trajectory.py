import numpy
import matplotlib.pyplot as plt
from math import pi, factorial

# s -- start point
# e -- end point
# position, velocity, acceleration for q_1
Q1s = 0
dotQ1s = 0
ddotQ1s = 0
Q1e = 45
dotQ1e = 0
ddotQ1e = 0
# position, velocity, acceleration for q_2
Q2s = 0
dotQ2s = 0
ddotQ2s = 0
Q2e = 90
dotQ2e = 0
ddotQ2e = 0
# the time interval
ts = 0
te = 42
step = 0.1

initQ = [
    [Q1s, Q1e],
    [Q2s, Q2e]
]
initDotQ = [
    [dotQ1s, dotQ1e],
    [dotQ2s, dotQ2e]
]
initDDotQ = [
    [ddotQ1s, ddotQ1e],
    [ddotQ2s, ddotQ2e]
]
interval = [ts, te, step]


# Calculation value of polynomial h(t) for itself order,
#   coefficients = (a0, a1, a2 etc.)
def calculatePolynom(order, coefficients, time, derivative=0):
    h = 0
    for i in range(derivative, order + 1):
        h += (factorial(i) / factorial(i - derivative)) * coefficients[i] * time ** (i - derivative)
    return h


def getCoefficients(qs, dqs, ddqs, qe, dqe, ddqe):
    # x = A^(-1) b
    # x = transpose([a3, a4, a5])
    A = [
        [1, 1, 1],
        [3, 4, 5],
        [6, 12, 20]
    ]
    b = [
        [qe - qs - dqs - ddqs / 2],
        [dqe - qs - ddqs],
        [ddqe - ddqs]
    ]
    x = numpy.linalg.solve(A, b)
    # a0, a1, a2, a3, a4, a5
    coefficients = [qs, dqs, ddqs, x[0], x[1], x[2]]
    return coefficients


# relative time from absolut
# tau \in [real_time1, real_time2]; j -- real time;
# i -- number of part trajectory (for multypolynomal traj.)
def get_t(tau, j, i):
    return (j - tau[i - 1]) / (tau[i] - tau[i - 1])


def getTrajectory(iq, idq, iddq, tau, step=0.1, i=1):
    q = []
    dq = []
    ddq = []
    time = numpy.arange(tau[0], tau[1], step)
    coefficients = getCoefficients(iq[0], idq[0], iddq[0],
                                   iq[1], idq[1], iddq[1])
    for j in time:
        q.append(calculatePolynom(5, coefficients, get_t(tau, j, i)))
        dq.append(calculatePolynom(5, coefficients, get_t(tau, j, i), 1))
        ddq.append(calculatePolynom(5, coefficients, get_t(tau, j, i), 2))
    return q, dq, ddq


def getTrajectories(initQ, initDotQ, initDDotQ, interval):
    Q = []
    dQ = []
    ddQ = []
    for i in range(0, len(initQ)):
        qi, dqi, ddqi = getTrajectory(initQ[i], initDotQ[i], initDDotQ[i], (interval[0], interval[1]), interval[2])
        Q.append(qi)
        dQ.append(dqi)
        ddQ.append(ddqi)
    return Q, dQ, ddQ


# must call plt.show() after call it function
def plotTrajectory(q, dq, ddq, time, num_figure=0, color="r"):
    title = "Coordinate q%s" % (num_figure)
    plt.figure(title)
    plt.subplot(311)
    plt.plot(time, q, color)
    plt.subplot(312)
    plt.plot(time, dq, color)
    plt.subplot(313)
    plt.plot(time, ddq, color)


def plotTrajectories(Q, dQ, ddQ, interval):
    time = numpy.arange(interval[0], interval[1], interval[2])
    for i in range(0, len(q)):
        plotTrajectory(Q[i], dQ[i], ddQ[i], time, i+1)
    plt.show()

# q, q2, q3 = getTrajectory((0,45),(0,0),(0,0),(0,42))
q, q2, q3 = getTrajectories(initQ, initDotQ, initDDotQ, interval)

plotTrajectories(q, q2, q3, interval)
