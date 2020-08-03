import math
import random
import sys

sys.path.insert(0,'./dynamic_policy')
sys.path.insert(0,'./bayesian')
sys.path.insert(0,'./extended_dynamic_policy')

import sonar
import sonar_array
import constants
import utils
import edp_robot
import dp_robot
import b_robot
import matplotlib.pyplot as plt
from matplotlib import gridspec

# define constants


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

def play_episode():
    robot_co = 1

    robot_pos, goal_pos, full_obstacle_list = create_random_setup()
    start_pos = robot_pos.copy()
    print (f"start_pos={start_pos}")
    print (f"robot_pos={robot_pos}")
    print (f"goal_pos={goal_pos}")
    print (f"full_obstacle_list={full_obstacle_list}")

    #create a sonar array
    r1 = dp_robot.Robot(robot_pos.copy(), robot_co, constants.N_SENSOR, goal_pos)
    r2 = b_robot.Robot(robot_pos.copy(), robot_co, constants.N_SENSOR, goal_pos)
    r3 = edp_robot.Robot(robot_pos.copy(), robot_co, constants.N_SENSOR, goal_pos)

    print("000000000000000000000000000000000000000000")
    print("000000000000000000000000000000000000000000")
    print("Playing episode for Reinforcement Learning Robot")
    print("000000000000000000000000000000000000000000")
    print("000000000000000000000000000000000000000000")

    step_number1 = 1
    hit_obstcle1, reach_goal1 = False, False
    # Experiment 1
    while (hit_obstcle1 == False and reach_goal1 == False):
        print("")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("")
        print(f"step_number={step_number1}")
        hit_obstcle1, reach_goal1 = r1.update(full_obstacle_list, goal_pos) 
        step_number1 += 1
        if step_number1 > 200:
            hit_obstcle1 = True
            reach_goal1 = False
            print(f"Too many steps, it will probably take too long to end")
            break
    print(f"Completed in {step_number1} steps")
    
    print("000000000000000000000000000000000000000000")
    print("000000000000000000000000000000000000000000")
    print("Playing episode for Bayesian Robot")
    print("000000000000000000000000000000000000000000")
    print("000000000000000000000000000000000000000000")
    
    print (f"start_pos={start_pos}")
    print (f"robot_pos={robot_pos}")
    print (f"goal_pos={goal_pos}")
    print (f"full_obstacle_list={full_obstacle_list}")

    step_number2 = 1
    hit_obstcle2, reach_goal2 = False, False
    # Experiment 2
    while (hit_obstcle2 == False and reach_goal2 == False):
        print("")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("")
        print(f"step_number={step_number2}")
        hit_obstcle2, reach_goal2 = r2.update(full_obstacle_list, goal_pos) 
        step_number2 += 1    
        if step_number2 > 200:
            hit_obstcle2 = True
            reach_goal2 = False
            print(f"Too many steps, it will probably take too long to end")
            break
    print(f"Completed in {step_number2} steps")

    print("000000000000000000000000000000000000000000")
    print("000000000000000000000000000000000000000000")
    print("Playing episode for Reiforcement 5x5")
    print("000000000000000000000000000000000000000000")
    print("000000000000000000000000000000000000000000")
    
    print (f"start_pos={start_pos}")
    print (f"robot_pos={robot_pos}")
    print (f"goal_pos={goal_pos}")
    print (f"full_obstacle_list={full_obstacle_list}")

    step_number3 = 1
    hit_obstcle3, reach_goal3 = False, False
    # Experiment 3
    while (hit_obstcle3 == False and reach_goal3 == False):
        print("")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("")
        print(f"step_number={step_number3}")
        hit_obstcle3, reach_goal3 = r3.update(full_obstacle_list, goal_pos) 
        step_number3 += 1    
        if step_number3 > 200:
            hit_obstcle3 = True
            reach_goal3 = False
            print(f"Too many steps, it will probably take too long to end")
            break
    print(f"Completed in {step_number3} steps")


    print (f"start_pos={start_pos}")
    print (f"robot_pos={robot_pos}")
    print (f"goal_pos={goal_pos}")
    print (f"full_obstacle_list={full_obstacle_list}")
    return step_number1, hit_obstcle1, reach_goal1, step_number2, hit_obstcle2, reach_goal2, step_number3, hit_obstcle3, reach_goal3

episodes_data = {    
    "episode" : [],
    "steps1" : [],
    "success1" : [],
    "steps2" : [],
    "success2" : [],
    "steps3" : [],
    "success3" : []
}

for i in range(constants.N_EPISODES):
    step_number1, hit_obstcle1, reach_goal1,step_number2, hit_obstcle2, reach_goal2, step_number3, hit_obstcle3, reach_goal3  = play_episode()
    episodes_data["episode"].append(i)
    episodes_data["steps1"].append(step_number1)
    episodes_data["success1"].append(reach_goal1)
    episodes_data["steps2"].append(step_number2)
    episodes_data["success2"].append(reach_goal2)
    episodes_data["steps3"].append(step_number3)
    episodes_data["success3"].append(reach_goal3)

print("Final result")
print("------------")
print("Episode: ", episodes_data["episode"])
print("Steps1: ", episodes_data["steps1"])
print("Success1: ", episodes_data["success1"])
print("Steps2: ", episodes_data["steps2"])
print("Success2: ", episodes_data["success2"])
print("Steps3: ", episodes_data["steps3"])
print("Success3: ", episodes_data["success3"])

passed_episodes = {
    "x" : [],
    "y" : [],
    "rl" : 0,
    "bayesian" : 0,
    "r3" : 0
}
failed_episodes = {
    "x" : [],
    "y" : []
}

for episode_index in range(constants.N_EPISODES):
    if episodes_data["success1"][episode_index]:
        passed_episodes["x"].append(episode_index)
        passed_episodes["y"].append(episodes_data["steps1"][episode_index])
        passed_episodes["rl"] += 1
    if episodes_data["success2"][episode_index]:
        passed_episodes["x"].append(episode_index)
        passed_episodes["y"].append(episodes_data["steps2"][episode_index])
        passed_episodes["bayesian"] += 1
    if episodes_data["success3"][episode_index]:
        passed_episodes["x"].append(episode_index)
        passed_episodes["y"].append(episodes_data["steps3"][episode_index])
        passed_episodes["r3"] += 1

for episode_index in range(constants.N_EPISODES):
    if episodes_data["success1"][episode_index] == False:
        failed_episodes["x"].append(episode_index)
        failed_episodes["y"].append(episodes_data["steps1"][episode_index])
    if episodes_data["success2"][episode_index] == False:
        failed_episodes["x"].append(episode_index)
        failed_episodes["y"].append(episodes_data["steps2"][episode_index])
    if episodes_data["success3"][episode_index] == False:
        failed_episodes["x"].append(episode_index)
        failed_episodes["y"].append(episodes_data["steps3"][episode_index])


fig, axes = plt.subplots(2)
fig.suptitle('Obstacle Avoidance')
episode_steps_plot = axes[0]
episode_steps_plot.set_title("Episode Steps") 

episode_steps_plot.plot(episodes_data["steps1"], "Blue", label = "Dynamic Policy")
episode_steps_plot.plot(episodes_data["steps2"], "Orange", label = "Baysian")
episode_steps_plot.plot(episodes_data["steps3"], "Red", label = "Extended Dynamic Policy")
episode_steps_plot.scatter(passed_episodes["x"], passed_episodes["y"], label= "Reached the Goal", color= "green",  
            marker= "*", s=30) 
episode_steps_plot.scatter(failed_episodes["x"], failed_episodes["y"], label= "Hit an Obstacle", color= "red",  
            marker= "s", s=30) 

episode_steps_plot.set(xlabel='Episodes', ylabel='Steps')
episode_steps_plot.legend()

print("Accuracy:")
rl_accuracy = passed_episodes["rl"]/constants.N_EPISODES*100
print(f"Dynamic Policy: {rl_accuracy}%")
bayesian_accuracy = passed_episodes["bayesian"]/constants.N_EPISODES*100
print(f"Baysian: {bayesian_accuracy}%")
mc_5x5_accuracy = passed_episodes["r3"]/constants.N_EPISODES*100
print(f"Extended Dynamic Policy: {mc_5x5_accuracy}%")

accuracy_plot = axes[1]
accuracy_plot.set_title("Accuracy") 
accuracy_plot.set(xlabel='Algorithms', ylabel='Percentage')
accuracy_plot.bar(["Dynamic Policy","Bayesian","Extended Dynamic Policy"], [rl_accuracy, bayesian_accuracy, mc_5x5_accuracy], width=0.4)

plt.tight_layout()
plt.show()


