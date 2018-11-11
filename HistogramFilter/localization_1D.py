from __future__ import print_function, division
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
#world = [0, 1, 1, 0, 0]
colors = ["white", "black"]
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
    gridspec_kw={'height_ratios' : [10, 1]},
    sharex=True)
world_ax.imshow([world, world], cmap=cmap, norm=norm, interpolation=None)
world_ax.get_yaxis().set_ticks([])
x = [i for i in range(n_cells)]
rects = prob_ax.bar(x, p)
line, = world_ax.plot(0, 1, 'r.')
def update(i):
    global p
    p = sense(p, world[i%100])
    print(p)
    p = move(p, 1)
    print(p)
    for rect, h in zip(rects, p):
        rect.set_height(h)
    line.set_xdata((i+1)%n_cells)
    input()
    return rects, line,

def init():
    prob_ax.set_xlim(0, n_cells-1)
    prob_ax.set_ylim(0, 1)
    world_ax.set_xlabel("Position")
    prob_ax.set_ylabel("Probability")
    prob_ax.set_title("Histogram Localization With Measurements")
    return rects, line,

anim = animation.FuncAnimation(fig, update, n_cells, interval=50, init_func=init)
plt.show()
#anim.save("only_move.gif", writer="imagemagick")
