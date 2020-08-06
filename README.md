# School of Continuing Studies, University of Toronto

# 3547 TERM PROJECT
# Intelligent Systems and Reinforcement Learning

### Title: Robot obstacle avoidance with reinforcement learning

#### Group Members:
    1. Alexandre Dietrich
    2. Ankur Tyagi
    3. Haitham Alamri
    4. Rodolfo Vasconcelos


Date: August, 4 2020

The report in Jupyter Notebook format is stored at https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/Term%20Project%20V2.ipynb

The presentation is in the same folder at https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/project_ppt_v1.pdf

# Table of Contents

* [Introduction](#Introduction)
* [Problem](#Problem)
* [Solution](#Solution)
    * [Algorithm 1 - Static Policy](#Alternative_1)
        * [Training Phase](#Training_Phase)
        * [Playing Phase](#Playing_Phase)
    * [Algorithm 2 - Dynamic Policy](#Alternative_2)
        * [Description](#Description_1)
    * [Algorithm 3 - Extended Dynamic Policy](#Alternative_3)
        * [Description](#Description_2)
* [Evaluation](#Evaluation)
* [Conclusion](#Conclusion)
* [Appendix A - Code and Documentation](#Appendix_A)
* [Appendix B - Instructions to Run the Code](#Appendix_B)

<a id='Introduction'></a>
# Introduction

After ten weeks of learning additional Artificial Intelligence techniques, which cover more traditional branches of AI, such as research, planning, knowledge, logic and reinforcement learning, we had the opportunity to put what we learned into practice. After interesting brainstorming and group discussions, we decided to go ahead with a project using reinforcement learning. We found a challenging project and the right size to carry out a solution in a reasonable time and resources. We then put our efforts into defining the problem, defining workarounds, coding and testing our algorithms, evaluating the results and preparing for the conclusion. Here's what we did.

<a id='Problem'></a>
# Problem

### Problem statement: Find the path for a robot to reach an end point (goal state) while avoiding randomly generated obstacles in a 2D space, using reinforcement learning methods.

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/Problem Identification.jpg" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 1. Problem Statement</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div> 
 

We found an implementation of this challenge that uses other techniques, instead of reinforcement learning. Here is the link to the article that inspired us on this project. 

https://bayesianadventures.wordpress.com/2015/08/31/obstacle-avoidance-for-clever-robots/

For this project, the environment created by the original simulator is called "Robot World".

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/bayesian_giphy.gif" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 2. Original Bayesian algorithm simulation</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div> 

In this Robot World, you can move around by clicking on the step button. After a new step, the robot will be in a new state. You can add new obstacles during the journey dynamically. The objective is to reach the goal point (G) without colliding with an obstacle. You can also define the starting and goal points. 

The original code implemented three important classes: Robot, Sonar and Sonar_Array. The first one controls the robot, its position, its movements, etc. The other two implement the controls to obtain information from all the sensors and allows the robot to uderstantd if there are obstacles in close range, define the alerts and define the actions that control whether the robot should continue on its path or need to make a turn to avoid an obstacle. This part of the code is where our main problem lies. 

- Can we use reinforcement learning to define an optimal policy to guide the robot's actions to avoid the obstacles and reach the goal? 
- Can we replace the original algorithm by a more efficient RL algorithm or RL is not the best solution for this problem? 
- Can we extrapolate this problem to a drone or to a more dynamic environment ? 

These were some questions that guided our project. 

The original code and simultador can be see and run in this link: <br>
http://www.codeskulptor.org/#user40_EEIxkOtKog_1.py

     
To effectively use the original code and simulator, we made some changes and adapted the Robot World. Our goal was to focus more on reinforcement learning algorithms than on other parts of the code. 
<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/new_simulator.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 3. New Robot World Simulator</b></center>
<center><i>Source: New Robot World from Term Project</i></center>
<center><i>.</i></center>
</div> 

# Solution

We tried different alternatives to solve the problem. To effectively use the original code and simulator, we made some changes and adapted the Robot World. Our main goal was to focus more on reinforcement learning algorithms than on other parts of the code, but we also adapted the original code to better compare the results of our alternatives. Below you can see our solution alternatives. 

<a id='Alternative_1'></a>
## Algorithm 1 - Static Policy

In our first approach, we redefined the Robot World like this:

New Robot World Assumptions: <br>
500 x 500 pixels <br>
Start point at the top left corner <br>
End point at the bottom right corner <br>


Following is the definition of the Markov Decision Process (MDP): 

States: all possible states within a 4 x 4 grid with 0, 1 or 2 obstacles<br>
Start State: top left corner<br>
Actions(s): Up, Down, Right and left<br>
T(s'|s; a): probability of reaching s' if action a is taken in state s = 1 (No uncertainty)<br>
Reward(s; a; s0): -1 without obsctacle, -5 when there is an obstacle<br>
End State: bottom right corner <br>
Discount factor = 0.6<br>
_   

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/Small Grid.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 4. Small Grid approach</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div>

<a id='Training_Phase'></a>
### Training Phase


To find an optimal policy to help our robot reach its goal without hitting obstacles, we made an operational decision and divided the New Robot World (500 x 500) in 100 4 x 4 position grids. With that, we created a strategy to find the best policy in a smaller grid, considering that we could have 15 different positions for one or two obstacles. We ran the Monte Carlo method to simulate thousands of episodes and value iteration to find optimal q-value for every state in 4 x 4 grid and determine the action based on epsilon soft policy algorithm. The generated master policy is a dictionary of states and actions for all 100 grids. 

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/Training Phase.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 5. Static Policy Algorithm - Training Phase</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div>


After that initial phase to define master policy, we just copied the print of policy to the code that implement the playing stage which was adapted to run the New Robot World. Below you can find some parts of the code which we use to build our Master Policy. 


```python
## Parts of the code extracted from the python master-policy.py program


def standard_grid(starting_position,k1,k2,x1,x2):
  # define a grid that describes the reward for arriving at each state
  # and possible actions at each state
  g = Grid(4, 4, starting_position)
  rewards = {
    (3, 3): 0,
    (k1,k2):-5,
    (x1,x2):-5,
  }
  actions = {
    (0, 0): ('L', 'D', 'R','U'),
    (0, 1): ('L', 'D', 'R','U'),
    (0, 2): ('L', 'D', 'R','U'),
    (0, 3): ('L', 'D', 'R','U'),
    (1, 0): ('L', 'D', 'R','U'),
    (1, 1): ('L', 'D', 'R','U'),
    (1, 2): ('L', 'D', 'R','U'),
    (1, 3): ('L', 'D', 'R','U'),
    (2, 0): ('L', 'D', 'R','U'),
    (2, 1): ('L', 'D', 'R','U'),
    (2, 2): ('L', 'D', 'R','U'),
    (2, 3): ('L', 'D', 'R','U'),
    (3, 0): ('L', 'D', 'R','U'),
    (3, 1): ('L', 'D', 'R','U'),
    (3, 2): ('L', 'D', 'R','U'),
    (3, 3): ('L', 'D', 'R','U'),
  }
  g.set(rewards, actions)
  return g


def play_game(grid, policy):
  # returns a list of states and corresponding returns
  # use an epsilon-soft policy
  # Random start position
  states = [(i, j) for i in range(4) for j in range(4)]
  initState = random.choice(states[1:-1])
  g = standard_grid(initState,k1,k2,x1,x2)
  s = initState
  grid.set_state(s)
  a = random_action(policy[s])

  # each triple is s(t), a(t), r(t)
  # but r(t) results from taking action a(t-1) from s(t-1) and landing in s(t)
  states_actions_rewards = [(s, a, 0)]
  while True:
    r = grid.move(a)
    s = grid.current_state()
    if grid.game_over():
      states_actions_rewards.append((s, None, r))
      break
    else:
      a = random_action(policy[s]) # the next state is stochastic
      states_actions_rewards.append((s, a, r))

  # calculate the returns by working backwards from the terminal state
  G = 0
  states_actions_returns = []
  first = True
  for s, a, r in reversed(states_actions_rewards):
    # the value of the terminal state is 0 
    # we should ignore the first state we encounter
    # and ignore the last G, which is meaningless since it doesn't correspond to any move
    if first:
      first = False
    else:
      states_actions_returns.append((s, a, G))
    G = r + GAMMA*G
  states_actions_returns.reverse() # we want it to be in order of state visited
  return states_actions_returns

```

<a id='Playing_Phase'></a>
### Playing Phase

With the Master Policy trained, we adapted the original code of the Robot World to create our New Robot World. We included the Master Policy as a dictionary considering States and Actions. We also created two functions: find_location_onMap and policy_finder, which are use to obtain information of the robot and obstacles within a specific grid and define the optimal action according the these positions. 

Within the code where the original program understands what action the robot should take when it discovers an obstacle, we changed the code to call our policy_finder fuction, which find the robot and obstacle locations, and return the action that the robot must take, 
according to our Master Policy. 

  
<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/Algorithm 1.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 6. Static Policy Algorithm - Playing Phase</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div> 

You can now play with an initial version of the New Robot World by clicking on the step button and adding new obstacles. 

Here is the link to the New Robot World:

http://www.codeskulptor.org/#user47_JJSgNIMtcq_0.py

Following are parts of the code that were inserted or updated int the original simulator for the New Robot World.






```python
## Parts of the code extracted from the python obavd3.py program in the static_policy folder

# Add the master pilocy 
master_policy={0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'U', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'L', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'U', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}
master_policy_2obs={0: {0: {0: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'U', (1, 2): 'U', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 1: {0: {0: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'U', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'U', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'L', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'L', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 2: {0: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'R', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'U', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'L', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 3: {0: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'L', (2, 0): 'U', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'U', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'U', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}}, 1: {0: {0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'U', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'U', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 1: {0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'U', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'L', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'L', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 2: {0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'U', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'U', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'U', (1, 0): 'D', (1, 1): 'D', (1, 2): 'U', (1, 3): 'U', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'L', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 3: {0: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'L', (0, 3): 'R', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'U', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'U', (2, 1): 'U', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'U', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'U', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}}, 2: {0: {0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'D', (1, 2): 'L', (1, 3): 'U', (2, 0): 'U', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'D', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 1: {0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'U', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'U', (1, 2): 'D', (1, 3): 'U', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 2: {0: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'L', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'U', (1, 3): 'D', (2, 0): 'D', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'L', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'L', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 3: {0: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'U', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'L', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'L', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'L', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'U', (1, 2): 'D', (1, 3): 'L', (2, 0): 'U', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'U', (1, 3): 'U', (2, 0): 'D', (2, 1): 'L', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'U', (1, 3): 'U', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'U', (1, 3): 'U', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'D', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'L', (1, 3): 'U', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'U', (1, 1): 'D', (1, 2): 'L', (1, 3): 'U', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'U', (0, 1): 'U', (0, 2): 'L', (0, 3): 'L', (1, 0): 'U', (1, 1): 'L', (1, 2): 'L', (1, 3): 'U', (2, 0): 'U', (2, 1): 'U', (2, 2): 'U', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'U', (1, 1): 'D', (1, 2): 'U', (1, 3): 'U', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}}, 3: {0: {0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'U', (1, 1): 'D', (1, 2): 'D', (1, 3): 'U', (2, 0): 'U', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'L', (1, 2): 'U', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'U', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'U', (1, 1): 'D', (1, 2): 'L', (1, 3): 'U', (2, 0): 'L', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 1: {0: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'L', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'L', (2, 0): 'R', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'D', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'L', (2, 0): 'U', (2, 1): 'R', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'D', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'L', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}, 2: {0: {0: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'L', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'D', (1, 2): 'D', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'U', (0, 2): 'L', (0, 3): 'L', (1, 0): 'U', (1, 1): 'U', (1, 2): 'U', (1, 3): 'L', (2, 0): 'U', (2, 1): 'U', (2, 2): 'U', (2, 3): 'D', (3, 0): 'U', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'R', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'U', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}}}, 3: {0: {0: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'L', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'D', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'L', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'L', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 1: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'U', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'L', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'U', (1, 3): 'D', (2, 0): 'D', (2, 1): 'D', (2, 2): 'L', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 2: {0: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'D', (0, 3): 'D', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'D', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'D', (0, 1): 'L', (0, 2): 'D', (0, 3): 'L', (1, 0): 'R', (1, 1): 'D', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'R', (0, 1): 'D', (0, 2): 'L', (0, 3): 'L', (1, 0): 'D', (1, 1): 'D', (1, 2): 'L', (1, 3): 'L', (2, 0): 'D', (2, 1): 'D', (2, 2): 'D', (2, 3): 'D', (3, 0): 'R', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}, 3: {0: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'D', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 1: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'D', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'R', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}, 2: {(0, 0): 'R', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'U', (1, 1): 'U', (1, 2): 'U', (1, 3): 'D', (2, 0): 'U', (2, 1): 'L', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'L', (3, 2): 'R', (3, 3): 'U'}, 3: {(0, 0): 'D', (0, 1): 'R', (0, 2): 'R', (0, 3): 'D', (1, 0): 'R', (1, 1): 'R', (1, 2): 'R', (1, 3): 'D', (2, 0): 'U', (2, 1): 'U', (2, 2): 'R', (2, 3): 'D', (3, 0): 'U', (3, 1): 'R', (3, 2): 'R', (3, 3): 'U'}}}}}

# New Code
def check_obstacle(pos, obs_list):
    obstacles=[]
    location_on_map,location_on_grid = utils.find_location_onMap(pos)
    for i in obs_list:
        location_on_map1,location_on_grid1 = utils.find_location_onMap(i)
        if (location_on_map1 == location_on_map):
            obstacles.append(i)
    return obstacles
def find_location_onMap(pos):
  location_in_the_grid=[]
  location_in_the_map=[]
  i=0
  i1=0
  loc=0
  loc1=0
  for squares in range(0,10):
    i1=0
    for quare in range(0,10):
      loc=0
      #square.append((i,i1))
      if ((pos[0]>i and pos[0]<=i+50) and (pos[1]>i1 and pos[1]<=i1+50)):
        for rows in range(0,4):
          loc1=0
          for col in range(0,4):
            if ((pos[0]>loc+i and pos[0]<=loc+i+12.5) and (pos[1]>loc1+i1 and pos[1]<=loc1+12.5+i1)):           
              location_in_the_grid.append(loc)
              location_in_the_grid.append(loc1)
              location_in_the_map.append(i)
              location_in_the_map.append(i1)
            
            loc1+=12.5
          loc+=12.5
      i1+=50
    i+=50

#To to convert to 4x4 grid each is 12.5 X 12.5 pixels
  location_in_the_grid[0]=int(location_in_the_grid[0]/12.5)
  location_in_the_grid[1]=int(location_in_the_grid[1]/12.5)
#To to convert to 5x5 map each sqaure is 100X100 pixel
  location_in_the_map[0]=int(location_in_the_map[0]/50)
  location_in_the_map[1]=int(location_in_the_map[1]/50)
  return location_in_the_map, location_in_the_grid
def policy_finder (mylocation,obs):
    
    mylocation_onMap, my_location_onGrid = find_location_onMap(mylocation)
    obs_location_onMap, obs_location_onGrid = find_location_onMap(obs[0])
    policy= master_policy[obs_location_onGrid[0]][obs_location_onGrid[1]]
    direction = policy.get((my_location_onGrid[0],my_location_onGrid[1]), ' ')
    print(direction)
    return direction

def policy_finder2_obs (mylocation,obs):
  mylocation_onMap, my_location_onGrid = find_location_onMap(mylocation)
  obs_location_onMap, obs_location_onGrid = find_location_onMap(obs[0])
  obs_location_onMap1, obs_location_onGrid1 = find_location_onMap(obs[1])
  policy= master_policy_2obs[obs_location_onGrid[0]][obs_location_onGrid[1]][obs_location_onGrid1[0]][obs_location_onGrid1[1]]
  direction = policy.get((my_location_onGrid[0],my_location_onGrid[1]), ' ')
  print("kokokokoo",direction)
  return direction


# Part of code updated within the Sonar_Array Class

def weighted_sum_method(self, robot_pos, robot_co,full_obstacle_list):
        #process data by the weighted sum method and 
        #return (1) whether turn is required or not (2) index of recommended sonar LOS to turn to
        sum_d = 0
        sum_wt = 0
        alert = False
        obs=[]
        
        obs=check_obstacle(robot_pos,full_obstacle_list)
        print("---------------------------")
        print("I see obstacles")
        print("---------------------------")
        #print "checking all sonars:"      
        for sonar in self.sonar_list:
            #print "sonar:", sonar.index, " range:", sonar.output
            if sonar.output < SENSOR_ALERT_R:#has this sonar found anything in danger zone?
                alert = True
                #print "obstacle found by index ", sonar.index
                for s1 in self.sonar_list: #process the whole array
                    d = int(s1.output)
                    gain = 1#SENSOR_MAX_R/(SENSOR_MAX_R - d)
                    sum_d +=  d
                    sum_wt += s1.index * d * gain
                    #print "I:", s1.index,",D:",int(s1.output), ",sum_D:", sum_d, "sum_wt:",sum_wt
                rec_index = math.ceil(TURN_SCALE_FACTOR * float(sum_wt)/sum_d) #index of sonar with best LOS
                #rec_index = int(TURN_SCALE_FACTOR * float(sum_d)/sum_wt)
                print ("Rec index:", rec_index)
                if abs(rec_index) > n_sensor/2:
                    print ("rec index too large")
                    rec_index = n_sensor/2
#                    if rec_index < 0:
#                        rec_index = -n_sensor/2
#                    else:
#                        rec_index = n_sensor/2
                print ("Rec index:", rec_index) 
                #break # processing completed
            else: #no obstacle in danger zone
                rec_index = 0
                #return robot_co, False
                #print : index = ", sonar.index
        #print "break from loop."
        if rec_index == 0 and alert == True:
                print ("alert with no alteration")
                obs=check_obstacle(robot_pos,full_obstacle_list)
                print(obs)
               
                if (len(obs)!=0 and len(obs)<2):
                        action = policy_finder(robot_pos,obs)
                        I_was_here.append(robot_pos)
                elif(len(obs)==2):
                        action = policy_finder2_obs(robot_pos,obs)
                        I_was_here.append(robot_pos)
                else:
                        return robot_co, False
                if action:
                        print(action,"HAAH")
                        if action == 'R':
                            print ("policy recommend to go right ")
                            offset=90
                        elif action == 'D':
                            offset=180
                            print ("policy recommend to go down ")
                        elif action == 'L':
                            offset=270
                            print ("policy recommend to go left")
                        elif action == 'U':
                            offset = 359
                            print ("policy recommend to go down ")
                        #if (I_was_here[-2]==robot_pos):
                            #return robot_co+45, True
                        print("Robot positon",robot_pos)
                        print("*********")
                        print("Robot Co",robot_co)
                        print("New Direction",(offset%robot_co)+robot_co)
                        print("******")                        
                        return offset, True
                        #return (offset%robot_co)+robot_co, True 
        
                        
                
        elif abs(rec_index) > 0: # some alteration recommended
           obs=[]
           offset =  rec_index * SENSOR_FOV #how much is the angular offset  
           print(obs)
           obs=check_obstacle(robot_pos,full_obstacle_list)
           if(obs!=None):
            
                if (len(obs)!=0  and len(obs)<2):
                            action = policy_finder(robot_pos,obs)
                            I_was_here.append(robot_pos)
                           
                elif(len(obs)==2):
                            action = policy_finder2_obs(robot_pos,obs)
                            I_was_here.append(robot_pos)
                            
                else:
                            return robot_co, False
                if action:
                            if action == 'R':
                                print ("policy recommend to go right ")
                                offset=90
                            elif action == 'D':
                                offset=180
                                print ("policy recommend to go down ")
                            elif action == 'L':
                                offset=270
                                print ("policy recommend to go left ")
                            elif action == 'U':
                                offset = 359
                                print ("policy recommend to go down ")
                            #if (I_was_here[-2]==robot_pos):
                                    #return robot_co+45, True
                print("Robot positon",robot_pos)
                #print("obs positon",obs)
                print("*********")
                print("Robot Co",robot_co)
                print("New Direction",(offset%robot_co)+robot_co)
                #print("location in the grid:",find_location_onMap(robot_pos))
                #print("location in the grid:",find_location_onMap(obs[0]))
                print("******")
                return offset,True
                #return (offset%robot_co)+robot_co, True
           else:     
            
                return (offset%robot_co), True
        else:# no diversion needed
           obs=[]
           offset =  rec_index * SENSOR_FOV #how much is the angular offset  
           print(obs)
           obs=check_obstacle(robot_pos,full_obstacle_list)
           if(obs!=None):
            
                if (len(obs)!=0  and len(obs)<2):
                            action = policy_finder(robot_pos,obs)
                            I_was_here.append(robot_pos)
                            print("chinca:1")
                elif(len(obs)==2):
                            action = policy_finder2_obs(robot_pos,obs)
                            I_was_here.append(robot_pos)
                            print("chinca:2")
                else:
                            return robot_co, False
                if action:
                            if action == 'R':
                                print ("policy recommend to go right ")
                                offset=90
                            elif action == 'D':
                                offset=180
                                print ("policy recommend to go down ")
                            elif action == 'L':
                                offset=270
                                print ("policy recommend to go left ")
                            elif action == 'U':
                                offset = 359
                                print ("policy recommend to go down ")
                            #if (I_was_here[-2]==robot_pos):
                                    #return robot_co+45, True
                print("Robot positon",robot_pos)
                #print("obs positon",obs)
                print("*********")
                print("Robot Co",robot_co)
                print("New Direction",(offset%robot_co)+robot_co)
                #print("location in the grid:",find_location_onMap(robot_pos))
                #print("location in the grid:",find_location_onMap(obs[0]))
                print("******")
                return offset,True
                #return (offset%robot_co)+robot_co, True


```

Here is a simulation of our static policy algorithm

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/bayesian_static_giphy.gif" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 7. Static Policy simulation</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div> 

The results of this algorithm were not good enough. We had too many assumptions like fix start and end points, no more than two obstacles per 4 x 4 grids, two different phases (training and playing) and we could only play the game online by clicking on the step button.  

<a id='Alternative_2'></a>
## Algorithm 2 - Dynamic Policy

For our second algorithm, we decided to keep the same strategy as algorithm 1 of dividing the original world of 500 x 500 into 100 4 x 4 grids. In this algorithm, we allowed dynamic start and end points and no fix number of obstacles within a 4 x 4 grid. 

<a id='Description'></a>
### Description

Following is the definition of the Markov Decision Process (MDP): 

States: all possible states within a 4 x 4 grid with 0 to 15 obstacles<br>
Start State: dynamic, defined when the episode starts<br>
Actions(s): Up, Down, Right and left<br>
T(s'|s; a): probability of reaching s' if action a is taken in state s = 0.95 (some uncertainty)<br>
Reward(s; a; s0): -1 without obsctacle, -5 when there is an obstacle<br>
End State: dynamic, defined when the episode starts <br>
Discount factor = 0.6<br>

To compare the performance to the original code and our solution, we converted the original code into Python 3, broked it in 4 Python programs to implement the three classes (Robot, Sonar and Sonar_Array) and utilitarian functions. This was important to run multiples episodes of the Robot in a batch mode. 

Our reinforcement learning strategy is now considering a dynamic policy. We implemented just one phase (playing), starting every episode without a policy. For every step (action) taken by our robot in the New Robot World, if a policy is not available for that state, a new policy is created using the same Monte Carlo method used in the alternative 1. Then the policy for that state is  stored. If the robot enters a state where a possible had been previously defined, then the robot uses that policy. The array with the policies is being appended as long as the robot moves step by step until it reaches the goal. 


<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/Algorithm 2.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 8. Dynamic Policy Algorithm</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div> 


Our new robot, supported now by reinforcement leanirng instead of bayesian methods, can run in the same graphical interface than the original robot. However, to compare the performance of the two robots, we create a code to run both robots simultaneous, with the same number and position of obstacles, and to capture the number of steps each robot takes to reach the goal after 200 episodes. Then, we can plot two graphs to compare the accuracy and effort of both robots. 


```python
## Parts of the code extracted from the python montecarlo.py program in the dynamic_policy folder

"""## Run all episodes"""
def calculate_gridworld_policy(end_state=(3,3),obstable_list = []):
  # use the standard grid again (0 for every step) so that we can compare
  # to iterative policy evaluation
  # grid = standard_grid()
  # try the negative grid too, to see if agent will learn to go past the "bad spot"
  # in order to minimize number of steps
  grid = negative_grid(step_cost=-1)
  update_rewards(grid, obstable_list, -5)
  update_end_state(grid, end_state)

  # print rewards
  #print("rewards:")
  print_values(grid.rewards, grid)

  pi = defaultdict(lambda: 1/len(ALL_POSSIBLE_ACTIONS))  # probability of action (def random)

  # state -> action
  # initialize a random policy
  policy = {}
  for s in grid.actions.keys():
      policy[s] = np.random.choice(ALL_POSSIBLE_ACTIONS)

  # initialize Q(s,a) and returns
  Q = {}
  returns = {} # dictionary of state -> list of returns we've received
  states = grid.all_states()
  for s in states:
      if s in grid.actions: # not a terminal state
        Q[s] = {}
        for a in ALL_POSSIBLE_ACTIONS:
          Q[s][a] = -10
          returns[(s,a)] = []
  else:
      # terminal state or state we can't otherwise get to
      pass

  #print("initial Q:")
  #print_Q(Q,grid)

  # repeat until convergence
  deltas = []
  for t in range(EPISODES):
      #if t % 1000 == 0:
          #print(t)
          #print("Q:")
          #print_Q(Q,grid)

      # generate an episode using pi
      biggest_change = 0
      states_actions_returns = play_episode(grid, policy, pi)

      # calculate Q(s,a)
      seen_state_action_pairs = set()
      for s, a, G in states_actions_returns:
          # check if we have already seen s
          # called "first-visit" MC policy evaluation
          sa = (s, a)
          if sa not in seen_state_action_pairs:
              old_q = Q[s][a]
              returns[sa].append(G)
              Q[s][a] = np.mean(returns[sa])
              biggest_change = max(biggest_change, np.abs(old_q - Q[s][a]))
              seen_state_action_pairs.add(sa)
              A_star, _ = max_dict(Q[s])
              for a_index in ALL_POSSIBLE_ACTIONS:
                  if a_index == A_star:   pi[(s,a_index)] = 1 - EPS + EPS/len(ALL_POSSIBLE_ACTIONS)
                  else:                   pi[(s,a_index)] = EPS/len(ALL_POSSIBLE_ACTIONS)

      deltas.append(biggest_change)

      # calculate new policy pi(s) = argmax[a]{ Q(s,a) }
      for s in policy.keys():
          a, _ = max_dict(Q[s])
          policy[s] = a

  """## Print results"""

  #plt.plot(deltas)
  #plt.show()

  # find the optimal state-value function
  # V(s) = max[a]{ Q(s,a) }
  V = {}
  for s in policy.keys():
      V[s] = max_dict(Q[s])[1]

  #print("final values:")
  #print_values(V, grid)
  #print("final policy:")
  #print_policy(policy, grid)
  #print("final Q:")
  #print_Q(Q,grid)
  return policy

```


```python
## Parts of the code extracted from the python utils.py program in the dynamic_policy folder

def dynamic_policy_finder (mylocation, obs, master_policy, goal_pos):
    print(f"mylocation={mylocation}, obs={obs}, goal_pos={goal_pos}")
    
    mylocation_onMap, my_location_onGrid = find_location_onMap(mylocation)
    print(f"mylocation_onMap={mylocation_onMap}, my_location_onGrid={my_location_onGrid}")

    obs_location_onGrid_array = []

    for obstacle_pos in obs:
        #_, obs_location_onGrid = find_location_onMap(obstacle_pos)
        #obs_location_onGrid_array.append((obs_location_onGrid[0],obs_location_onGrid[1]))
        obs_location_onGrid_array.extend(calculate_obstacle_onGrid(obstacle_pos))
        print(f"obs_location_onGrid_array={obs_location_onGrid_array}")
    
    end_state = calculate_end_state_onGrid(mylocation, obs_location_onGrid_array, goal_pos)

    policy_key = f"{end_state}|{obs_location_onGrid_array}"
    print(f"policy_key={policy_key}")

    if policy_key in master_policy:
        policy = master_policy[policy_key]
    else:
        policy = montecarlo.calculate_gridworld_policy(end_state, obs_location_onGrid_array)
        master_policy[policy_key] = policy

    #policy= master_policy[obs_location_onGrid[0]][obs_location_onGrid[1]]
    direction = policy.get((my_location_onGrid[0],my_location_onGrid[1]), ' ')
    print(f"direction={direction}")
    return direction


```


```python
## Parts of the code extracted from the python sonar_array.py program in the dynamic_policy folder


# Part of code updated within the Sonar_Array Class

    def weighted_sum_method(self, robot_pos, robot_co,full_obstacle_list,master_policy,I_was_here,goal_pos)

        print (f"weighted_sum_method, robot_pos={robot_pos}, robot_co={robot_co}")

        sum_d = 0
        sum_wt = 0
        alert = False
        obs=[]
        
        obs=check_obstacle(robot_pos,full_obstacle_list)
               
        action = utils.dynamic_policy_finder(robot_pos,obs,master_policy,goal_pos)
        print(f"action={action},")
        if action == 'R':
            print ("policy recommend to go right ")
            offset=90
        elif action == 'D':
            offset=180
            print ("policy recommend to go down ")
        elif action == 'L':
            offset=270
            print ("policy recommend to go left ")
        elif action == 'U':
            offset = 359
            print ("policy recommend to go down ")
        else:
            offset = 0
            print ("no policy?")
        #if (I_was_here[-2]==robot_pos):
            #return robot_co+45, True
        print("Robot positon",robot_pos)
        print("*********")
        print("Robot Co",robot_co)
        print("New Direction",(offset%robot_co)+robot_co)
        print("******")                        
        return offset, True

```

Here is a simulation of our dynamic policy algorithm. 

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/dynamic_giphy.gif" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 9. Dynamic Policy simulation</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div> 

We achieved a better performance with the dynamic approach, but we had an intuition that our 4 x 4 grid was too small and we could be missing something important. We decided to test a third algorithm to try to get new answers for the problem. 

<a id='Alternative_3'></a>
## Algorithm 3 - Extended Dynamic Policy

For our third algorithm, we decided to keep the same strategy as algorithm 2 of dividing the original world of 500 x 500, but now we have choose dynamic 250 x 250 pixels grids. The agent would be always in the middle of the grid to define the police. In this algorithm, we allowed dynamic start and end points and no fix number of obstacles within a 250 x 250px grid. 

<a id='Description'></a>
### Description

Following is the definition of the Markov Decision Process (MDP): 

States: all possible states within a 20 x 20 grid with 0 to 400 obstacles<br>
Start State: dynamic, defined when the episode starts<br>
Actions(s): Up, Down, Right and left<br>
T(s'|s; a): probability of reaching s' if action a is taken in state s = 0.95 (some uncertainty)<br>
Reward(s; a; s0): -1 without obsctacle, -5 when there is an obstacle<br>
End State: dynamic, defined when the episode starts <br>
Discount factor = 0.6<br>

Our reinforcement learning strategy is now considering a dynamic policy. We implemented just one phase (playing), starting every episode without a policy. For every step (action) taken by our robot in the New Robot World (250 x 250px), if a policy is not available for that state, a new policy is created using the same Monte Carlo method. Instead of Monte-carlo in a grid of 4x4 , we are calculating a grid of 5x5. The Monte Carlo is much more expensive because the grid is larger. Then the policy for that state is  stored. If the robot enters a state where a possible new state had been previously defined, then the robot uses that policy. The array with the policies is being appended as long as the robot moves step by step until it reaches the goal.


```python
## Parts of the code extracted from the python montecarlo_5x5.py program in the extended_dynamic_policy folder

def standard_grid():
  # define a grid that describes the reward for arriving at each state
  # and possible actions at each state
  # the grid looks like this
  # S means start position
  # E means the end states
  #
  # E  .  .  .
  # .  .  . .
  # S  .  .  .
  # .  .  .  E
  g = Grid(5, 5, (2, 2))
#  rewards = {(3, 3): 0}
  rewards = {}
  actions = {
    (0, 0): ('D', 'R'),
    (0, 1): ('D', 'R', 'L'),
    (0, 2): ('D', 'R', 'L'),
    (0, 2): ('D', 'R', 'L'),
    (0, 3): ('D', 'R', 'L'),
    (0, 4): ('D', 'L'),
    (1, 0): ('D', 'R', 'U'),
    (1, 1): ('D', 'R', 'L', 'U'),
    (1, 2): ('D', 'R', 'L', 'U'),
    (1, 3): ('D', 'R', 'L', 'U'),
    (1, 4): ('D', 'U', 'L'),
    (2, 0): ('D', 'U', 'R'),
    (2, 1): ('D', 'R', 'L', 'U'),
    (2, 2): ('D', 'R', 'L', 'U'),
    (2, 3): ('D', 'R', 'L', 'U'),
    (2, 4): ('D', 'U', 'L'),
    (3, 0): ('U', 'R', 'D'),
    (3, 1): ('D', 'R', 'L', 'U'),
    (3, 2): ('D', 'R', 'L', 'U'),
    (3, 3): ('D', 'R', 'L', 'U'),
    (3, 4): ('D', 'U', 'L'),
    (4, 0): ('U', 'R', ),
    (4, 1): ('U', 'R', 'L'),
    (4, 2): ('U', 'R', 'L'),
    (4, 3): ('U', 'R', 'L'),
    (4, 4): ('U','L')
  }
  g.set(rewards, actions)
  return g

def calculate_gridworld_policy(end_state=(3,3),obstable_list = []):
  # use the standard grid again (0 for every step) so that we can compare
  # to iterative policy evaluation
  # grid = standard_grid()
  # try the negative grid too, to see if agent will learn to go past the "bad spot"
  # in order to minimize number of steps
  grid = negative_grid(step_cost=-1)
  update_rewards(grid, obstable_list, -5)
  update_end_state(grid, end_state)

  # print rewards
  #print("rewards:")
  print_values(grid.rewards, grid)

  pi = defaultdict(lambda: 1/len(ALL_POSSIBLE_ACTIONS))  # probability of action (def random)

  # state -> action
  # initialize a random policy
  policy = {}
  for s in grid.actions.keys():
      policy[s] = np.random.choice(ALL_POSSIBLE_ACTIONS)

  # initialize Q(s,a) and returns
  Q = {}
  returns = {} # dictionary of state -> list of returns we've received
  states = grid.all_states()
  for s in states:
      if s in grid.actions: # not a terminal state
        Q[s] = {}
        for a in ALL_POSSIBLE_ACTIONS:
          Q[s][a] = -10
          returns[(s,a)] = []
  else:
      # terminal state or state we can't otherwise get to
      pass

  #print("initial Q:")
  #print_Q(Q,grid)

  # repeat until convergence
  deltas = []
  for t in range(EPISODES):
      #if t % 1000 == 0:
          #print(t)
          #print("Q:")
          #print_Q(Q,grid)

      # generate an episode using pi
      biggest_change = 0
      states_actions_returns = play_episode(grid, policy, pi)

      # calculate Q(s,a)
      seen_state_action_pairs = set()
      for s, a, G in states_actions_returns:
          # check if we have already seen s
          # called "first-visit" MC policy evaluation
          sa = (s, a)
          if sa not in seen_state_action_pairs:
              old_q = Q[s][a]
              returns[sa].append(G)
              Q[s][a] = np.mean(returns[sa])
              biggest_change = max(biggest_change, np.abs(old_q - Q[s][a]))
              seen_state_action_pairs.add(sa)
              A_star, _ = max_dict(Q[s])
              for a_index in ALL_POSSIBLE_ACTIONS:
                  if a_index == A_star:   pi[(s,a_index)] = 1 - EPS + EPS/len(ALL_POSSIBLE_ACTIONS)
                  else:                   pi[(s,a_index)] = EPS/len(ALL_POSSIBLE_ACTIONS)

      deltas.append(biggest_change)

      # calculate new policy pi(s) = argmax[a]{ Q(s,a) }
      for s in policy.keys():
          a, _ = max_dict(Q[s])
          policy[s] = a

  """## Print results"""

  print_policy(policy, grid)

  return policy

```


```python
## Parts of the code extracted from the python utils.py program in the extended_dynamic_policy folder

def dynamic_policy_finder (mylocation, obs, master_policy, goal_pos):
    print(f"dynamic_policy_finder - mylocation={mylocation}, obs={obs}, goal_pos={goal_pos}")
    
    mylocation_onMap, _ = find_location_onMap(mylocation)
    print(f"dynamic_policy_finder - mylocation_onMap={mylocation_onMap}")

    policy_key = f"{mylocation_onMap}"
    #policy_key = f"{end_state}|{obs_location_onMap_array}"
    print(f"policy_key={policy_key}")

    current_state_on_grid = (2,2)
    if policy_key in master_policy:
        pos_onPolicy = master_policy[policy_key][0]
        policy = master_policy[policy_key][1]
        print(f"Reusing Policy calculated for {pos_onPolicy}")
        current_state_on_grid = find_location_onGrid(pos_onPolicy,mylocation_onMap)
        print(f"current_state_on_grid={current_state_on_grid}")
        current_state_on_grid = invertCoordinate(current_state_on_grid)
        print(f"inverted current_state_on_grid={current_state_on_grid}")
        montecarlo.print_policy_without_grid(policy)
    else:
        obs_location_onMap_array = []

        for obstacle_pos in obs:
            obs_location_onMap_array.extend(calculate_obstacle_onMap(mylocation_onMap, obstacle_pos))
            print(f"obs_location_onMap_array={obs_location_onMap_array}")
        
        addOutOfBoundsAsObstacles(mylocation_onMap, obs_location_onMap_array)
    
        # monte carlo does not work well if 2,2 has obstacle
        if (2,2) in obs_location_onMap_array:
            obs_location_onMap_array.remove((2,2))
            print(f"dynamic_policy_finder - (2,2) is removed")

        end_state = calculate_end_state_onGrid(mylocation, obs_location_onMap_array, goal_pos)

        #policy = montecarlo.calculate_gridworld_policy(end_state, obs_location_onMap_array)
        policy = runMonteCarlo(end_state, obs_location_onMap_array)
        for x in range(-1,2,1):
            for y in range(-1,2,1):
                master_policy[f"{[x+mylocation_onMap[0],y+mylocation_onMap[1]]}"] = [mylocation_onMap, policy]

    #policy = montecarlo.calculate_gridworld_policy(end_state, obs_location_onMap_array)
    direction = policy.get(current_state_on_grid, ' ')
    print(f"direction={direction}")
    return direction
```


```python
## Parts of the code extracted from the python sonar_array.py program in the extende_dynamic_policy folder


# Part of code updated within the Sonar_Array Class

def weighted_sum_method(self, robot_pos, robot_co,full_obstacle_list,master_policy,I_was_here,goal_pos):

        if skip_the_policy():
            offset = random.randint(0,359)
            print("<<<<<<<<<<<<<<<")
            print("weighted_sum_method will skip the policy this time")
            print(f"offset={offset}")
            print(">>>>>>>>>>>>>>>>")
            return offset, True


        print (f"weighted_sum_method, robot_pos={robot_pos}, robot_co={robot_co}")
        #process data by the weighted sum method and 
        #return (1) whether turn is required or not (2) index of recommended sonar LOS to turn to
        sum_d = 0
        sum_wt = 0
        alert = False
        obs=[]
        
        robot_loc_onMap, _ = utils.find_location_onMap(robot_pos)
        goal_onMap, _ = utils.find_location_onMap(goal_pos)
        if robot_loc_onMap[0]==goal_onMap[0] and robot_loc_onMap[1]==goal_onMap[1]:
            print(f"Robot and Goal are in the same square")
            return 0, False

        obs=utils.check_obstacle(robot_pos,full_obstacle_list)
               
        action = utils.dynamic_policy_finder(robot_pos,obs,master_policy,goal_pos)
        print(f"action={action},")
        if action == 'R':
            print ("policy recommend to go right ")
            offset=90+random.randint(0,5)
        elif action == 'D':
            offset=180+random.randint(0,5)
            print ("policy recommend to go down ")
        elif action == 'L':
            offset=270+random.randint(0,5)
            print ("policy recommend to go left ")
        elif action == 'U':
            offset = 359-random.randint(0,5)
            print ("policy recommend to go up ")
        else:
            offset = 0
            print ("no policy?")
        #if (I_was_here[-2]==robot_pos):
            #return robot_co+45, True
        print("Robot positon",robot_pos)
        print("*********")
        print("Robot Co",robot_co)
        print("New Direction",(offset%robot_co)+robot_co)
        print("******")                        
        return offset, True

```

Here is a simulation of our extended dynamic policy algorithm. 

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/extended_dynamic_giphy.gif" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 10. Extended Dynamic Policy simulation</b></center>
<center><i>Source: Term Project</i></center>
<center><i>.</i></center>
</div>

This algorithm was not as good as the dynamic policy, but was an important step in our learning process to understand the possibilities that reinforcement learning can provide us to solve problems. 

# Evaluation

We prepared charts to analyze the performance of all algorithms executed in 200 independent episodes. Here are the results. 

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/bayesian_200_episodes_onlySteps.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 11. Bayesian Algorithm Performance</b></center>
</div>
<br>
<br>
<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/static_policy_200_episodes_onlySteps.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 12. Static Policy Algorithm Performance</b></center>
</div>
<br>
<br>
<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/dynamic_policy_200_episodes_onlySteps.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 13. Dynamic Policy Algorithm Performance</b></center>
</div>
<br>
<br>
<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/extended_dynamic_policy_200_episodes_onlySteps.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 14. Extended Dynamic Policy Algoritm Performance</b></center>
</div>
<br>
<br>
<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/algorithm_accuracy.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 15. Algorithm Accuracy</b></center>
</div>

The Dynamic Policy algorithm has the highest consistency among all the algorithm to navigate through obstacles. We tried to achieve the best performance using reinforcement learning algorithms. 

# Conclusion

The project offered us a great opportunity to put into practice what we learned during the course. We tried different approaches and ended up with the feeling that there are many additional alternatives and more experimentation that we can do. The following are some lessons learned and future work that can be done to improve our solution.

Lesson learned:
we should not solve continuous problems using discrete solutions


Possible extensions of the work include :
1. Use deep learning – q network to further increases the accuracy for the path navigation as done in the snake game (reference : https://github.com/maurock/snake-ga)
2. Use deep deterministic policy gradient for solving the problem in continuous domain (reference : https://www.youtube.com/watch?v=PngA5YLFuvU&t=187s)

<div align="center">
<img src="https://github.com/ravasconcelos/rl_obstacle_avoidance/blob/master/notebook/images/robot_movements.png" alt="Drawing" style="width: 800px;"/>
<center><b>Figure 16. An example with reinforcement learning</b></center>
<center><i>Source: Term Project</i></center>
</div> 

<a id='Appendix_A'></a>
# Appendix A - Code and Documentation

All the code prepared for this project is available on Github. Here is the link for the project. 

https://github.com/ravasconcelos/rl_obstacle_avoidance

Description:

In the root you can find the code to run the algorithms. 

Folders: 
1. notebook - this report and presentation
2. bayseian - Original Bayseian code transformed to Python 3 and prepared to run in a bacyh mode
3. static_policy - Code with implements the Static Policy algorithm
4. dynamic_policy - Code with implements the Dynamic Policy algorithm

<a id='Appendix_B'></a>
# Appendix B - Instructions to Run the Code


Installation

1. See pip_list for the library version
2. Download and install Xming: https://sourceforge.net/projects/xming/
3. set display:
export DISPLAY=localhost:0
