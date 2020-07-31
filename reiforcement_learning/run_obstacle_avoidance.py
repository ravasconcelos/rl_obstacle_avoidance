import math
import random
import sonar
import sonar_array
import constants
import utils
import robot

# define constants
FRAME_SIZE = 500
N_SENSOR = 16 
N_OBSTACLES = 16
N_EPISODES = 10

def create_random_escalar():
    return random.randint(0,FRAME_SIZE)

def create_random_position():
    return [create_random_escalar(), create_random_escalar()]

def create_random_setup():
    robot_pos = create_random_position()
    goal_pos = create_random_position()
    full_obstacle_list = []
    for _ in range(N_OBSTACLES):
        full_obstacle_list.append((create_random_escalar(),create_random_escalar()))
    return robot_pos, goal_pos, full_obstacle_list

def play_episode():

    robot_co = 1

    robot_pos, goal_pos, full_obstacle_list = create_random_setup()
    print (f"robot_pos={robot_pos}")
    print (f"goal_pos={goal_pos}")
    print (f"full_obstacle_list={full_obstacle_list}")

    #create a sonar array
    r1 = robot.Robot(robot_pos, robot_co, N_SENSOR, goal_pos)

    step_number = 1
    hit_obstcle, reach_goal = False, False
    while (hit_obstcle == False and reach_goal == False):
        print("")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("")
        print(f"step_number={step_number}")
        hit_obstcle, reach_goal = r1.update(full_obstacle_list, goal_pos)
        step_number += 1
    print(f"Completed in {step_number} steps")
    return step_number, hit_obstcle, reach_goal

episodes_data = {
    "steps" : [],
    "success" : []
}

for _ in range(N_EPISODES):
    step_number, hit_obstcle, reach_goal = play_episode()
    episodes_data["steps"].append(step_number)
    episodes_data["success"].append(reach_goal)

print("Final result")
print("------------")
print("Steps: ", episodes_data["steps"])
print("Success: ", episodes_data["success"])
