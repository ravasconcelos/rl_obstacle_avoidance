import baysian_obs_avoid
import time

start_pos = [10,10]
robot_pos = [10, 10]
robot_co = 1
goal_pos = [450,450]
n_sensor = 16 


r1 = baysian_obs_avoid.Robot(robot_pos, robot_co, n_sensor, goal_pos)

i = 0
obstacle_flag, goal_flag = 0, 0
while (goal_flag == False and obstacle_flag == False):
    i+=1
    obstacle_flag, goal_flag = r1.update()
    print ("Total number of steps:{}".format(i))
    time.sleep(0.001)
