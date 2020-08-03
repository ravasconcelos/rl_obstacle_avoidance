import math
import random
import json

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


import json

appDict = {
  'name': 'messenger',
  'playstore': True,
  'company': 'Facebook',
  'price': 100
}
app_json = json.dumps(appDict)
print(app_json)


f = open("episodes_test.py", "w")
f.write("EPISODES = [
    {
        "robot_pos" : [10, 10],
        "goal_pos" : [450,450],
        "full_obstacle_list" : [(50, 100), (300, 210), (410, 300), (400, 310)]
    },
    {
        "robot_pos" : [10, 10],
        "goal_pos" : [450,450],
        "full_obstacle_list" : [(50, 100), (300, 210), (410, 300), (400, 310)]
    },
]")
f.close()

