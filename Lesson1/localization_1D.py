from __future__ import print_function, division
import matplotlib.pyplot as plt

#Number of grid cells
n_cells = 5
n_measurements = 2

#Start with uniform probability distribution i.e. the robot could be anywhere
#p = [1/n_cells for _ in range(n_cells)]

#Or we know where we start
p = [0 for _ in range(n_cells)]
p[0] = 1

world = ["green", "red", "red", "green", "green"]
measurements = world
p_hit = 0.6
p_miss = 0.2
p_exact = 0.8
p_undershoot = 0.1
p_overshoot = 0.1

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

#for k in range(n_measurements):
    #p = sense(p, measurements[k])

fig, ax = plt.subplots()
#plt.ion()

for i in range(1000):
    ax.cla()
    ax.plot(p)
    ax.set_ylim(0, 1)
    plt.pause(1e-3)
    p = move(p, 1)

#ax.plot(p)
#plt.show()