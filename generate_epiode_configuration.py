import math
import random
import constants

EPISODE_FILE_NAME = "episodes.py"

def create_random_escalar():
    return random.randint(0,constants.FRAME_SIZE)

def create_random_position():
    return [create_random_escalar(), create_random_escalar()]

def create_random_setup():
    robot_pos = create_random_position()
    goal_pos = create_random_position()
    full_obstacle_list = []
    for _ in range(constants.N_OBSTACLES):
        full_obstacle_list.append((create_random_escalar(),create_random_escalar()))
    return robot_pos, goal_pos, full_obstacle_list

def printEpisodeSetup(f):
    print("  {", file=f)
    print(f"    \"robot_pos\" : {create_random_position()},", file=f) 
    print(f"    \"goal_pos\" : {create_random_position()},", file=f) 
    full_obstacle_list = []
    for _ in range(constants.N_OBSTACLES):
        full_obstacle_list.append((create_random_escalar(),create_random_escalar()))
    print(f"    \"full_obstacle_list\" : {full_obstacle_list}", file=f) 
    print("  },", file=f)

f = open(EPISODE_FILE_NAME, "w")
print("EPISODES = [", file=f) 
for _ in range(constants.N_EPISODES*5):
    printEpisodeSetup(f)
print("]", file=f)
f.close()

