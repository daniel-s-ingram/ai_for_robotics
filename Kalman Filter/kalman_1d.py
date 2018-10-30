from __future__ import print_function, division
from random import gauss
from math import sqrt, exp, pi
import matplotlib.pyplot as plt

def f(mean, var, x):
    return exp(-0.5*(x-mean)**2/var)/sqrt(2*pi*var)

def update(mean1, var1, mean2, var2):
    new_mean = (var2*mean1 + var1*mean2)/(var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    return new_mean, new_var

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return new_mean, new_var

measurement_var = 0.4
motion_var = 0.5
measurements = [gauss(i, measurement_var) for i in range(100)]
motion = [gauss(1, motion_var) for i in range(100)]
mean = 0
var = 10000
x_pts = [i/10 for i in range(1000)]

plt.ion()
fig, ax = plt.subplots()

for meas, move in zip(measurements, motion):
    mean, var = predict(mean, var, move, motion_var)
    y1 = [f(mean, var, x) for x in x_pts]
    mean, var = update(mean, var, meas, measurement_var)
    y2 = [f(mean, var, x) for x in x_pts]
    ax.cla()
    ax.plot(x_pts, y1, 'r-')
    ax.plot(x_pts, y2, 'g-')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1)
    ax.legend(("Prediction", "Update"))
    plt.pause(1e-3)