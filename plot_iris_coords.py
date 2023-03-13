'''plot x,y,z data from a list using a matplotlib 3D plot'''


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

data = [
[0,468,0.513432,0.4056498,0.004029],
[0,469,0.5226817,0.4060153,0.004029],
[0,470,0.5134187,0.3921469,0.004029],
[0,471,0.5040786,0.4053049,0.004029],
[0,472,0.5133595,0.4190525,0.004029],
[0,473,0.5981546,0.4063564,0.0048743],
[0,474,0.6068251,0.4069338,0.0048743],
[0,475,0.5981172,0.3926875,0.0048743],
[0,476,0.5894306,0.4056647,0.0048743],
[0,477,0.5981624,0.4199503,0.0048743]
]

x = [] # x,y,z data
y = []
z = []
pointlabels = [] # labels for each point

for i in data:
    x.append(i[2]) 
    y.append(i[3])
    z.append(i[4])
    pointlabels.append(i[1])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#make the scale of the x and y axes go from zero to 1, and the z axis from -0.1 to +0.1
ax.set_xlim3d(0, 1)
ax.set_ylim3d(0, 1)
ax.set_zlim3d(-0.1, 0.1)

#label the points

for i in range(len(x)):
#make the labels centered above each datapoint
    ax.text(x[i], y[i], z[i], pointlabels[i], horizontalalignment='center', verticalalignment='top')

#make the first five points blue
ax.scatter(x, y, z, c='b', marker='o')
#make the rest of the points red
x = x[5:]
y = y[5:]
z = z[5:]
ax.scatter(x, y, z, c='r', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
