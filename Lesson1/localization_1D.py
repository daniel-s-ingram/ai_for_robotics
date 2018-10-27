from __future__ import print_function, division
import random
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors

#Number of grid cells
n_cells = 100

p_hit = 0.6
p_miss = 0.2
p_exact = 0.8
p_undershoot = 0.1
p_overshoot = 0.1

#Start with uniform probability distribution i.e. the robot could be anywhere
p = [1/n_cells for _ in range(n_cells)]

#Or we know where we start
#p = [0 for _ in range(n_cells)]
#p[0] = 1

world = [1 if random.random() > 0.8 else 0 for _ in range(n_cells)]

colors = ["green", "red"]
levels = [0, 1, 2]
cmap, norm = from_levels_and_colors(levels, colors)

def sense(p, Z):
    q = []
    for i in range(n_cells):
        hit = (world[i] == Z)
        q.append(p[i]*(hit*p_hit + (1 - hit)*p_miss))
    norm = sum(q)
    q = [q[i]/norm for i in range(n_cells)]
    return q

def move(p, U):
    q = []
    for i in range(n_cells):
        s = p_exact*p[(i-U)%len(p)]
        s += p_overshoot*p[(i-U-1)%len(p)]
        s += p_undershoot*p[(i-U+1)%len(p)]
        q.append(s)
    return q

fig, (prob_ax, world_ax) = plt.subplots(
    nrows=2,
    ncols=1,
    gridspec_kw={'height_ratios' : [10, 1]})
plt.ion()
world_ax.imshow([world], cmap=cmap, norm=norm, interpolation=None)
world_ax.axis("off")
for i in range(n_cells):
    p = sense(p, world[i])
    p = move(p, 1)
    prob_ax.cla()
    prob_ax.plot(p)
    prob_ax.set_xlim(0, n_cells)
    prob_ax.set_ylim(0, 1)
    plt.pause(1e-3)