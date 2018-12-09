from __future__ import print_function, division
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

M = 50        #Rows
N = 50        #Columns
GOAL_NODE = (M-1, N-1)
OBSTACLE_PROBABILITY = 0.15
GRID = np.int8(np.random.random((M, N)) > OBSTACLE_PROBABILITY)
IMAGE = 255*np.dstack((GRID, GRID, GRID))
IMAGE[GOAL_NODE] = [0, 255, 0]
DELTAS = [[-1, 0],
          [0, -1],
          [1, 0],
          [0, 1]]

cost = 1

fig, ax = plt.subplots()
fig.set_size_inches(19.2, 9.43, True)
ax.imshow(IMAGE)
kwargs = {"width" : 0.01,
          "head_width" : 0.4,
          "length_includes_head" : True}
value = 1000*np.ones((M, N))
change = True
def animate(_):
    change = False
    for x in range(M):
        for y in range(N):
            if (x, y) == GOAL_NODE:
                if value[x, y] > 0:
                    value[x, y] = 0
                    change = True
            elif GRID[x, y] == 1:
                for a in range(len(DELTAS)):
                    x2 = x + DELTAS[a][0]
                    y2 = y + DELTAS[a][1]
                    if x2 >= 0 and x2 < M and y2 >= 0 and y2 < N and GRID[x2, y2] == 1:
                        v2 = value[x2, y2] + cost
                        if v2 < value[x, y]:
                            change = True
                            value[x, y] = v2
                            ax.arrow(y, x, DELTAS[a][1], DELTAS[a][0], **kwargs)

anim = animation.FuncAnimation(fig, animate, 100, interval=50)
#plt.show()
anim.save("dstar_grid.gif", writer="imagemagick")
