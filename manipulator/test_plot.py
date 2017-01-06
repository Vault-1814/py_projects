import matplotlib.pyplot as plt
from kinematics import *
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')
centerx = 0
centery = 0
in_q = [0,-pi/2,0,0,0,0]
X = np.zeros(6)
Y = np.zeros(6)
Z = np.zeros(6)
X[0] = centerx
Y[0] = centery
Z[0] = 0
for j in range(1, 6):
    H = forward(in_q, j)
    o = H[:3, 3]
    x, y, z = o
    X[j] = x + centerx
    Y[j] = y + centery
    Z[j] = z
ax.plot(X, Y, Z)
ax.set_xlim(-70, 70)
ax.set_ylim(-70, 70)
ax.set_zlim(-70, 70)
plt.show()
