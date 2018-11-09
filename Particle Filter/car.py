from __future__ import print_function, division
from math import sqrt, pi, cos, sin, tan, exp, atan2
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

L = 10          #Car length
W = 5           #Car width
R = 1           #Tire radius

N_PARTICLES = 1000
MAX_STEERING_ANGLE = pi/4
WORLD_SIZE = 100
LANDMARKS = [[20*i, 90] for i in range(6)]
LANDMARKS += [[20*i, 10] for i in range(6)]
LANDMARKS += [[20*i+10, 5] for i in range(5)]
LANDMARKS += [[20*i+10, 95] for i in range(5)]

class Car:
    def __init__(self, L=L, W=W, R=R):
        self.x = WORLD_SIZE*random.random()
        self.y = WORLD_SIZE*random.random()
        self.theta = 2*pi*random.random()
        self.alpha = 0
        self.bearing_noise = 0.1
        self.steering_noise = 1
        self.distance_noise = 1
        self.L = L
        self.W = W
        self.left_side = np.array([[-L/2, L/2],
                                   [W/2, W/2],
                                   [1, 1]])
        self.right_side = np.array([[-L/2, L/2],
                                   [-W/2, -W/2],
                                   [1, 1]])
        self.front_side = np.array([[L/2, L/2],
                                   [W/2, -W/2],
                                   [1, 1]])
        self.back_side = np.array([[-L/2, -L/2],
                                   [W/2, -W/2],
                                   [1, 1]])
        self.wheel = np.array([[-R, R],
                               [0, 0],
                               [1, 1]])

    def set_pose(self, new_x, new_y, new_theta, new_alpha):
        self.x = new_x
        self.y = new_y
        self.theta = new_theta%(2*pi)
        self.alpha = new_alpha

    def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
        self.bearing_noise = new_b_noise
        self.steering_noise = new_s_noise
        self.distance_noise = new_d_noise

    """
    def sense(self, add_noise=True):
        Z = []
        for lm in LANDMARKS:
            dx = lm[0] - self.x
            dy = lm[1] - self.y
            bearing = atan2(dy, dx) - self.theta
            if add_noise:
                bearing += random.gauss(0, self.bearing_noise)
            bearing = bearing%(2*pi)
            Z.append(bearing)
        return Z

    def Gaussian(self, bearing_error):
        return exp(-(bearing_error)**2/(2*self.bearing_noise**2))/sqrt(2*pi*self.bearing_noise**2)

    def measurement_prob(self, measurements):
        prob = 1.0
        predicted = self.sense(False)
        for pred, meas in zip(predicted, measurements):
            bearing_error = abs(pred - meas)
            bearing_error = (bearing_error + pi)%(2*pi) - pi
            prob *= self.Gaussian(bearing_error)
        return prob
    """
    def sense(self):
        Z = []
        for lm in LANDMARKS:
            dist = sqrt((self.x - lm[0])**2 + (self.y - lm[1])**2)
            dist += random.gauss(0, self.distance_noise)
            Z.append(dist)
        return Z

    def Gaussian(self, mean, var, x):
        return exp(-(mean - x)**2/(2*var**2))/sqrt(2*pi*var**2)

    def measurement_prob(self, measurements):
        prob = 1.0
        for lm, meas in zip(LANDMARKS, measurements):
            dist = sqrt((self.x - lm[0])**2 + (self.y - lm[1])**2)
            prob *= self.Gaussian(dist, self.distance_noise, meas)
        return prob

    def move(self, alpha, d):
        if alpha > MAX_STEERING_ANGLE:
            alpha = MAX_STEERING_ANGLE
        elif alpha < -MAX_STEERING_ANGLE:
            alpha = -MAX_STEERING_ANGLE
        d = d + random.gauss(0, self.distance_noise)
        alpha = alpha + random.gauss(0, self.steering_noise)
        beta = d*tan(alpha)/self.L
        if abs(beta) > 1e-6:
            R = d/beta
            x = self.x + R*(sin(self.theta + beta) - sin(self.theta))
            y = self.y + R*(cos(self.theta) - cos(self.theta + beta))
            theta = self.theta + beta
        else:
            x = self.x + d*cos(self.theta)
            y = self.y + d*sin(self.theta)
            theta = self.theta
        theta = theta%(2*pi)
        car = Car()
        car.set_pose(x, y, theta, alpha)
        car.set_noise(self.bearing_noise, self.steering_noise, self.distance_noise)
        return car

    def transform(self, x, y, theta):
        return np.array(
            [[cos(theta), -sin(theta), x],
             [sin(theta), cos(theta), y],
             [0, 0, 1]])

    def draw(self, lines):
        T = self.transform(self.x, self.y, self.theta)
        left_side = T.dot(self.left_side)
        right_side = T.dot(self.right_side)
        front_side = T.dot(self.front_side)
        back_side = T.dot(self.back_side)
        d = sqrt((L/2 - R)**2 + (W/2)**2)
        theta = atan2(W/2, -L/2 + R)
        x = self.x + d*cos(theta + self.theta)
        y = self.y + d*sin(theta + self.theta)
        T = self.transform(x, y, self.theta)
        back_left_tire = T.dot(self.wheel)
        theta = atan2(-W/2, -L/2 + R)
        x = self.x + d*cos(theta + self.theta)
        y = self.y + d*sin(theta + self.theta)
        T = self.transform(x, y, self.theta)
        back_right_tire = T.dot(self.wheel)
        theta = atan2(W/2, L/2 - R)
        x = self.x + d*cos(theta + self.theta)
        y = self.y + d*sin(theta + self.theta)
        T = self.transform(x, y, self.theta + self.alpha)
        front_left_tire = T.dot(self.wheel)
        theta = atan2(-W/2, L/2 - R)
        x = self.x + d*cos(theta + self.theta)
        y = self.y + d*sin(theta + self.theta)
        T = self.transform(x, y, self.theta + self.alpha)
        front_right_tire = T.dot(self.wheel)
        lines[0][0].set_data(left_side[0, :], left_side[1, :])
        lines[1][0].set_data(right_side[0, :], right_side[1, :])
        lines[2][0].set_data(front_side[0, :], front_side[1, :])
        lines[3][0].set_data(back_side[0, :], back_side[1, :])
        lines[4][0].set_data(back_left_tire[0, :], back_left_tire[1, :])
        lines[5][0].set_data(back_right_tire[0, :], back_right_tire[1, :])
        lines[6][0].set_data(front_left_tire[0, :], front_left_tire[1, :])
        lines[7][0].set_data(front_right_tire[0, :], front_right_tire[1, :])
        return lines
        
    def __repr__(self):
        return "[x = %.6f y = %.6f yaw = %.6f]" % (self.x, self.y, self.theta) 

def resample(p, w):
    new_p = []
    index = int(N_PARTICLES*random.random())
    beta = 0.0
    mw = max(w)
    for _ in range(N_PARTICLES):
        beta += 2*mw*random.random()
        while beta > w[index]:
            beta -= w[index]
            index = (index + 1)%N_PARTICLES
        new_p.append(p[index])
    return new_p

particles = [Car() for _ in range(N_PARTICLES)]
weights = [0 for _ in range(N_PARTICLES)]
fig, ax = plt.subplots()
lines = [ax.plot([0, 0], [0, 0], 'k-') for _ in range(8)]
lines[4][0].set_linewidth(5)
lines[5][0].set_linewidth(5)
lines[6][0].set_linewidth(5)
lines[7][0].set_linewidth(5)
sense_lines = [ax.plot([0, 0], [0, 0], 'b--', alpha=0.3) for _ in LANDMARKS]
particle_dots = [ax.plot(0, 0, '.') for _ in range(N_PARTICLES)]
car = Car()
car.set_noise(0, 0, 0)
car.set_pose(0, 50, 0, 0)
def animate(frame):
    global car, lines, particle_dots, particles, weights
    turn = 0.75*cos(2*pi*frame/75)
    forward = 0.5
    car = car.move(turn, forward)
    Z = car.sense()
    lines = car.draw(lines)
    for j in range(N_PARTICLES):
        p = particles[j].move(turn, forward)
        particles[j] = p
        weights[j] = p.measurement_prob(Z)
        particle_dots[j][0].set_data(p.x, p.y)
    norm = sum(weights)
    #weights = [w/norm for w in weights]
    particles = resample(particles, weights)
    for j in range(len(LANDMARKS)):
        sense_lines[j][0].set_data([car.x, LANDMARKS[j][0]], [car.y, LANDMARKS[j][1]])
    return lines, particle_dots, sense_lines,

def init():
    ax.set_xlim(0, WORLD_SIZE)
    ax.set_ylim(0, WORLD_SIZE)
    for lm in LANDMARKS:
        ax.plot(lm[0], lm[1], 'g*')
    return lines, particle_dots, sense_lines,

anim = animation.FuncAnimation(fig, animate, 200, interval=50, init_func=init)
#plt.show()
anim.save("car.gif", writer="imagemagick")