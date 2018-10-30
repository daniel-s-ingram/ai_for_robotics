# Artificial Intelligence for Robots by Sebastian Thrun

## 1D Histogram Localization
Using only dead reckoning, the robot's position quickly becomes uncertain even when it starts with 100% certainty of where it is. Dead reckoning uses only information about how the robot tries to move to estimate its position, but there is a possibility that the robot will move by some amount less than or more than it tried to move. Eventually, the robot's belief of where it is approaches a state of maximum uncertainty, known as the limit distribution, in which the robot believes it could be _anywhere_.
![](https://github.com/daniel-s-ingram/ai_for_robots/blob/master/Histogram%20Localization/only_move.gif)

The only way to overcome this uncertainty is to use the known positions of landmarks e.g. red blocks in a sea of green to get a better estimate of the robot's position. Landmarks even help to localize when we start with _no_ idea of where we are. 
![](https://github.com/daniel-s-ingram/ai_for_robots/blob/master/Histogram%20Localization/sense_and_move.gif)

## 2D Histogram Localization
![](https://github.com/daniel-s-ingram/ai_for_robots/blob/master/Histogram%20Localization/localization_2d.gif)