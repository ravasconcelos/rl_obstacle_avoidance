# Master policy for 2 Obstacles

import numpy as np
import random
from collections import defaultdict

master_policy={}

class Grid: # Environment
  def __init__(self, width, height, start):
    self.width = width
    self.height = height
    self.i = start[0]
    self.j = start[1]

  def set(self, rewards, actions):
    # rewards should be a dict of: (i, j): r (row, col): reward
    # actions should be a dict of: (i, j): A (row, col): list of possible actions
    self.rewards = rewards
    self.actions = actions

  def set_state(self, s):
    self.i = s[0]
    self.j = s[1]

  def current_state(self):
    return (self.i, self.j)

  def is_terminal(self, s):
    return s not in self.actions

  def move(self, action):
    # check if legal move first
    if action in self.actions[(self.i, self.j)]:
      same_state = (self.i,self.j)
      if action == 'U':
        self.i -= 1
      elif action == 'D':
        self.i += 1
      elif action == 'R':
        self.j += 1
      elif action == 'L':
        self.j -= 1
    # # if agent hit the wall go back to same position.
    if (self.i==4 or self.i==-1):
      (self.i,self.j)=same_state
    if (self.j==4 or self.j==-1):
      (self.i,self.j)=same_state
        # return a reward (if any)
    return self.rewards.get((self.i, self.j), 0)

  def game_over(self):
    # returns true if game is over, else false
    # true if we are in end state (0,0) or (3,3)
    end_state = [(3,3)]
    return (self.i, self.j) in end_state

  def all_states(self):
    # either a position that has possible next actions
    # or a position that yields a reward
    return set(self.actions.keys()) | set(self.rewards.keys())


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


def negative_grid(step_cost,k1,k2,x1,x2):
  # we minimize the number of moves
  # so we will penalize every move (-1) except for the end-state (0)
  
  states = [[i, j] for i in range(4) for j in range(4)]
  initState = random.choice(states[1:-1])
  g = standard_grid(initState,k1,k2,x1,x2)
  g.rewards.update({
    (0, 0): step_cost,
    (0, 1): step_cost,
    (0, 2): step_cost,
    (0, 3): step_cost,
    (1, 0): step_cost,
    (1, 0): step_cost,
    (1, 1): step_cost,
    (1, 2): step_cost,
    (1, 3): step_cost,
    (2, 0): step_cost,
    (2, 1): step_cost,
    (2, 2): step_cost,
    (2, 3): step_cost,
    (3, 0): step_cost,
    (3, 1): step_cost,
    (3, 2): step_cost,
    (3, 3): 0,
    (k1,k2): -5,
    (x1,x2): -5,

  })
  return g


def print_values(V, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      v = V.get((i,j), 0)
      if v >= 0:
        print(" %.2f|" % v, end="")
      else:
        print("%.2f|" % v, end="") # -ve sign takes up an extra space
    print("")


def print_policy(P, g):
  for i in range(g.width):
    print("---------------------------")
    for j in range(g.height):
      a = P.get((i,j), ' ')
      print("  %s  |" % a, end="")
    print("")
# the Monte Carlo Epsilon-Greedy method to find the optimal policy and value function
import numpy as np
import matplotlib.pyplot as plt

GAMMA = 0.7
ALL_POSSIBLE_ACTIONS = ('U', 'D', 'L', 'R')

def random_action(a, eps=0.1):
  # choose given a with probability 1 - eps + eps/4
  p = np.random.random()
  if p < (1 - eps):
    return a
  else:
    return np.random.choice(ALL_POSSIBLE_ACTIONS)

def max_dict(d):
  # returns the argmax (key) and max (value) from a dictionary
  max_key = None
  max_val = float('-inf')
  for k, v in d.items():
    if v > max_val:
      max_val = v
      max_key = k
  return max_key, max_val

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

for i in range(0,4):
  master_policy[i]={}
  for i1 in range(0,4):
    if (i==3 & i1==3):
      k1=2
      k2=2
    else:
      k1=i
      k2=i1
    master_policy[i][i1]={}
    for s0 in range(0,4):
      master_policy[i][i1][s0]={}
      for s1 in range(0,4): 
        if (s0==3 & s1==3):
          x1=2
          x2=2
        else:
          x1=s0
          x2=s1
        grid = negative_grid(-1,k1,k2,x1,x2)
# print rewards
        print("rewards:")
        print_values(grid.rewards, grid)

# state -> action
# initialize a random policy
        policy = {}
        for s in grid.actions.keys():
          policy[s] = np.random.choice(ALL_POSSIBLE_ACTIONS)
  
# initial policy
        print("initial policy:")
        print_policy(policy, grid)

# initialize Q(s,a) and returns
        Q = {}
        returns = {} # dictionary of state -> list of returns we've received
        states = grid.all_states()
        for s in states:
          if s in grid.actions: # not a terminal state
            Q[s] = {}
            for a in ALL_POSSIBLE_ACTIONS:
              Q[s][a] = 0
              returns[(s,a)] = []
          else:
    # terminal state or state we can't otherwise get to
            pass
  
# initial Q values for all states in grid
        print(Q)
        print(s)



# repeat
        deltas = []
        for t in range(1000):
  # generate an episode using pi
          biggest_change = 0
          states_actions_returns = play_game(grid, policy)

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
          deltas.append(biggest_change)

  # calculate new policy pi(s) = argmax[a]{ Q(s,a) }
          for s in policy.keys():
            a, _ = max_dict(Q[s])
            policy[s] = a


        plt.plot(deltas)
        plt.show()

# find the optimal state-value function
# V(s) = max[a]{ Q(s,a) }
        V = {}
        for s in policy.keys():
          V[s] = max_dict(Q[s])[1]

# Print the table of the estimated function Q(s,a) for the optimal policy 
        print("final values:")
        print_values(V, grid)

        print("final policy:")
# Print the policy pi(s) 
        print_policy(policy, grid)
        print(policy)
        print("#########################")
        print(i,i1,s0,s1)
        master_policy[i][i1][s0][s1]={}
        master_policy[i][i1][s0][s1]=policy
        print("#########################")
       
      