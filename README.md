# Artificial Intelligence for Robotics by Sebastian Thrun

## Lesson 1
### Histogram Localization in a Cylic 1D World
Using only dead reckoning, the robot's position quickly becomes uncertain even when it starts with 100% certainty of where it is. Dead reckoning uses only information about how the robot tries to move to estimate its position, but there is a possibility that the robot will move by some amount less than or more than it tried to move. Eventually, the robot's belief of where it is approaches a state of maximum uncertainty, known as the limit distribution, in which the robot believes it could be _anywhere_.
![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/HistogramFilter/only_move.gif)

The only way to overcome this uncertainty is to use the known positions of landmarks to get a better estimate of the robot's position. Landmarks even help to localize when we start with _no_ idea of where we are. 
![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/HistogramFilter/sense_and_move.gif)

### Histogram Localization in a Cyclic 2D World
![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/HistogramFilter/localization_2d.gif)

## Lesson 2
### 1D Kalman Filter
![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/KalmanFilter/kalman_1d.gif)

### 2D Kalman Filter
![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/KalmanFilter/kalman_2d.gif)

## Lesson 3
### Particle Filter
![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/ParticleFilter/particle_filter.gif)

![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/ParticleFilter/car.gif)

## Lesson 4
### A*

![](https://github.com/daniel-s-ingram/ai_for_robotics/blob/master/Search/astar_grid.gif)
