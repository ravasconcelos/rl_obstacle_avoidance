#
# School of Continuing Studies, University of Toronto
# 3547 TERM PROJECT
# Intelligent Systems and Reinforcement Learning
# Robot obstacle avoidance with reinforcement learning
#
# Alexandre Dietrich
# Ankur Tyagi
# Haitham Alamri
# Rodolfo Vasconcelos
#

'''
Utility functions used by several other files
'''

import math
import monte_carlo_5x5 as montecarlo
import numpy as np
import random
import sys
sys.path.insert(0,'..')
import constants
import logger

def brg_in_deg(p0, p1):#bearing only in degrees
    [x1, y1] = p0
    [x2, y2] = p1
    a = math.degrees(math.atan((y1 - y2)/(x1 - x2 + 0.000000001)))
    #find and correct the quadrant...
    if  x2 >= x1:
        b = 90 + a
    else:
        b = 270 + a
    return b

def dist(p1, p0):#distance only
    return math.sqrt((p1[0] - p0[0])**2+(p1[1]-p0[1])**2)

def relative_brg(b1, b2):
    rb = b2 - b1
    if rb > 180:
        rb = 360 - rb
    if rb < -180:
        rb += 360
        rb *= -1
    return rb


def angle_to_vector(ang):#resolve angles into vectors
    ang = math.radians(ang)
    return [math.cos(ang), math.sin(ang)]

def create_vector(from_pos, length, brg):       
        u_vec = angle_to_vector(brg)
        #print "generating target line..."
        vec0 = from_pos[0] + length * u_vec[1] 
        vec1 = from_pos[1] - length * u_vec[0]
        
        return [vec0, vec1]

def dist_and_brg_in_deg(p0, p1):#bearing and distance in degrees between two points
    [x1, y1] = p0
    [x2, y2] = p1
    r = math.sqrt((x1 - x2)**2 + (y1 - y2)**2) # distance
    a = math.degrees(math.atan((y1 - y2)/(x1 - x2 + 0.000000001)))
    #find and correct the quadrant...
    if  x2 >= x1:
        b = 90 + a
    else:
        b = 270 + a
    return r, b

def rel_brg_fm_offset_sensor(true_hdg, sensor_offset, tgt_brg):
    #given robot's true heading, the sensor offset angle and the
    #true brg of the target, this fn will return the relative brg
    #of the target from the sensor's line of sight
    
    sensor_look_brg = (true_hdg + sensor_offset)%360
    tgt_rel_fm_sensor = tgt_brg - sensor_look_brg

    if tgt_rel_fm_sensor < -180:
        tgt_rel_fm_sensor += 360
    
    return tgt_rel_fm_sensor


# this function to find the location of agent or obtacles in the map 
# it convert 500X500 pixels word to 10x10 squares each with 50x50 pixxels
def find_location_onMap(pos):
    print(f"find_location_onMap - pos={pos}")
    location_in_the_grid=[]
    location_in_the_map=[]
    x = pos[0]
    y = pos[1]
    location_in_the_map.append(int(x / constants.SMALL_GRID_SIZE))
    location_in_the_map.append(int(y / constants.SMALL_GRID_SIZE))
    print(f"location_in_the_map={location_in_the_map}")
    return location_in_the_map, None

# robot pos is always (2,2) in the grid
def find_location_onGrid(robot_pos_onMap, pos_onMap):
    grid_x = robot_pos_onMap[0] - pos_onMap[0]
    grid_y = robot_pos_onMap[1] - pos_onMap[1]
    if grid_x > 0:
        grid_x = 2 - grid_x
    else:
        grid_x = 2 + abs(grid_x)    
    if grid_y > 0:
        grid_y = 2 - grid_y
    else:
        grid_y = 2 + abs(grid_y)    
    return (grid_x,grid_y)


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

def isOutOfBounds(x,y):
    print(f"isOutOfBounds - x={x}, y={y}")
    if x < 0 or x > 4 or y < 0 or y > 4:
        return True
    return False

def addOutOfBoundsAsObstacles(mylocation_onMap, obs_location_onGrid_array):
    print(f"addOutOfBoundsAsObstacles - mylocation_onMap={mylocation_onMap}")
    robot_x = mylocation_onMap[0]
    robot_y = mylocation_onMap[1]
    for x in range(-2,3,1):
        for y in range(-2,3,1):
            obs_x = robot_x + x
            obs_y = robot_y + y
            print(f"obs_x={obs_x}, obs_y={obs_y}, x={x}, y={y}")
            if obs_x < 0 or obs_x > 9 or obs_y < 0 or obs_y > 9:
                obs_location_onGrid = find_location_onGrid(mylocation_onMap, [obs_x,obs_y])
                if isOutOfBounds(obs_location_onGrid[0],obs_location_onGrid[1]) == False:
                    obs_location_onGrid_array.append(obs_location_onGrid)
                    print(f"obs_location_onGrid will be added to obstacle array: {obs_location_onGrid}")
                else:
                    print(f"obs_location_onGrid will NOT be added to obstacle array: {obs_location_onGrid}")
            else:
                print(f"obs_x={obs_x}, obs_y={obs_y} is in the map, so it should not be considered an obstacle")
    

def addObstacleToMonteCarloCoordinates(mylocation_onMap, obs_onMap, obs_location_onGrid_array):
    # the reference point is the center of the grid (2,2)
    print(f"addObstacleToMonteCarloCoordinates - mylocation_onMap={mylocation_onMap}, obs_onMap={obs_onMap}")

    obs_onGrid = find_location_onGrid(mylocation_onMap, obs_onMap)
    print(f"addObstacleToMonteCarloCoordinates - obs_onGrid={obs_onGrid}")
    if isOutOfBounds(obs_onGrid[0],obs_onGrid[1]):
        print("addObstacleToMonteCarloCoordinates - the obstacle is out of the Monte Carlo grid")
        return
    obs_location_onGrid_array.append(obs_onGrid)
    return

# The obstacle can be in more than one space in the grid
#           U
#         L O R 
#           D  
def calculate_obstacle_onMap(mylocation_onMap, obstacle_pos):
    print(f"calculate_obstacle_onMap - mylocation_onMap={mylocation_onMap}, obstacle_pos={obstacle_pos}")
    obs_location_onGrid_array = []
    obs_onMap, _ = find_location_onMap(obstacle_pos)
    print(f"calculate_obstacle_onMap - obs_onMap={obs_onMap}")

    addObstacleToMonteCarloCoordinates(mylocation_onMap, obs_onMap, obs_location_onGrid_array)

    # Up
    border_obs_onMap, _ = find_location_onMap([obstacle_pos[0]-constants.OBSTACLE_RAD,obstacle_pos[1]])
    if border_obs_onMap != obs_onMap:
        print(f"calculate_obstacle_onMap - U border_obs_onMap={border_obs_onMap}")
        addObstacleToMonteCarloCoordinates(mylocation_onMap, border_obs_onMap, obs_location_onGrid_array)

    # Down
    border_obs_onMap, _ = find_location_onMap([obstacle_pos[0]+constants.OBSTACLE_RAD,obstacle_pos[1]])
    if border_obs_onMap != obs_onMap:
        print(f"calculate_obstacle_onMap - D border_obs_onMap={border_obs_onMap}")
        addObstacleToMonteCarloCoordinates(mylocation_onMap, border_obs_onMap, obs_location_onGrid_array)

    # Left 
    border_obs_onMap, _ = find_location_onMap([obstacle_pos[0],obstacle_pos[1]-constants.OBSTACLE_RAD])
    if border_obs_onMap != obs_onMap:
        print(f"calculate_obstacle_onMap - L border_obs_onMap={border_obs_onMap}")
        addObstacleToMonteCarloCoordinates(mylocation_onMap, border_obs_onMap, obs_location_onGrid_array)

    # Right
    border_obs_onMap, _ = find_location_onMap([obstacle_pos[0],obstacle_pos[1]+constants.OBSTACLE_RAD])
    if border_obs_onMap != obs_onMap:
        print(f"calculate_obstacle_onMap - R border_obs_onMap={border_obs_onMap}")
        addObstacleToMonteCarloCoordinates(mylocation_onMap, border_obs_onMap, obs_location_onGrid_array)

    return obs_location_onGrid_array

def calculate_end_state_onGrid(mylocation, obs_location_onGrid_array, goal_pos):

    print(f"obs_location_onGrid_array={obs_location_onGrid_array}")

    all_end_states = [(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(1,4),(2,4),(3,4),(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]    
    print(f"full all_end_states={all_end_states}")
    end_state = None

    for state in obs_location_onGrid_array:
        logger.log(f"state={state}")
        if state in all_end_states:
            logger.log(f"all_end_states.remove(state)")
            all_end_states.remove(state)   
    print(f"mylocation={mylocation}, goal_pos={goal_pos}, all_end_states={all_end_states}")

    robot_loc_onMap, _ = find_location_onMap(mylocation)
    goal_onMap, _ = find_location_onMap(goal_pos)
    goal_onGrid = find_location_onGrid(robot_loc_onMap, goal_onMap)
    if isOutOfBounds(goal_onGrid[0], goal_onGrid[1]) == False:
        end_state = goal_onGrid
        print(f"Goal is at end_state={end_state}")
        if end_state in obs_location_onGrid_array:
            obs_location_onGrid_array.remove(end_state)
    else:    
        best_end_states = getBestEndState(mylocation, goal_pos)
        print(f"best_end_states={best_end_states}")
        for state in best_end_states:
            if state not in obs_location_onGrid_array:
                end_state = state
                break

    if end_state is None and len(all_end_states) > 0:
        print("We will ramdomly pick an end state")
        end_state = random.choice(all_end_states)

    if end_state is None:
        print("We will colide, sorry")
        end_state = best_end_states[0]
        if end_state in obs_location_onGrid_array:
            obs_location_onGrid_array.remove(end_state)

    print(f"final end_state={end_state}")

    return end_state     

def getBestEndState(mylocation, goal_pos):
    robot_onMap, _ = find_location_onMap(mylocation)
    goal_onMap, _ = find_location_onMap(goal_pos)

    print(f"getBestEndState - robot_onMap={robot_onMap}, goal_onMap={goal_onMap}")

    # agent is above the target    
    if agentIsAboveGoal(robot_onMap, goal_onMap):
        end_states = [(2,4),(1,4),(3,4),(0,4),(4,4)]
    # agent is below the target    
    elif agentIsBelowGoal(robot_onMap, goal_onMap):
        end_states = [(2,0),(1,0),(3,0),(0,0),(4,0)]
    # agent is on the right of the target    
    elif agentIsRightOfGoal(robot_onMap, goal_onMap):
        end_states = [(0,2),(0,1),(0,3),(0,0),(0,4)]
    # agent is on the left of the target    
    elif agentIsLeftOfGoal(robot_onMap, goal_onMap):
        end_states = [(4,2),(4,1),(4,3),(4,0),(4,4)]
    # agent is in the bottom right of the target    
    elif agentIsBottonRightOfGoal(robot_onMap, goal_onMap):
        end_states = [(0,0),(1,0),(0,1),(2,0),(0,2)]
    # agent is in the top right of the target    
    elif agentIsTopRightOfGoal(robot_onMap, goal_onMap):
        end_states = [(0,4),(0,3),(1,4),(0,2),(2,4)]
    # agent is in the top left of the target    
    elif agentIsTopLeftOfGoal(robot_onMap, goal_onMap):
        end_states = [(4,4),(4,3),(3,4),(4,2),(2,4)]
    # agent is in the bottom left of the target    
    else:
        print(f"agent is in the bottom left of the target")
        end_states = [(4,0),(3,0),(4,1),(2,0),(4,2)]

    return end_states

def agentIsAboveGoal(robot_onMap, goal_onMap):
    print(f"agentIsAboveGoal - robot_onMap]{robot_onMap}, goal_onMap={goal_onMap}")
    if robot_onMap[0] == goal_onMap[0] and robot_onMap[1] < goal_onMap[1]:
        return True
    return False

def agentIsBelowGoal(robot_onMap, goal_onMap):
    print(f"agentIsBelowGoal - robot_onMap]{robot_onMap}, goal_onMap={goal_onMap}")
    if robot_onMap[0] == goal_onMap[0] and robot_onMap[1] > goal_onMap[1]:
        return True
    return False

def agentIsRightOfGoal(robot_onMap, goal_onMap):
    print(f"agentIsRightOfGoal - robot_onMap]{robot_onMap}, goal_onMap={goal_onMap}")
    if robot_onMap[0] > goal_onMap[0] and robot_onMap[1] == goal_onMap[1]:
        return True
    return False

def agentIsLeftOfGoal(robot_onMap, goal_onMap):
    print(f"agentIsLeftOfGoal - robot_onMap]{robot_onMap}, goal_onMap={goal_onMap}")
    if robot_onMap[0] < goal_onMap[0] and robot_onMap[1] == goal_onMap[1]:
        return True
    return False

def agentIsBottonRightOfGoal(robot_onMap, goal_onMap):
    print(f"agentIsBottonRightOfGoal - robot_onMap]{robot_onMap}, goal_onMap={goal_onMap}")
    if robot_onMap[0] > goal_onMap[0] and robot_onMap[1] > goal_onMap[1]:
        return True
    return False

def agentIsTopRightOfGoal(robot_onMap, goal_onMap):
    print(f"agentIsTopRightOfGoal - robot_onMap]{robot_onMap}, goal_onMap={goal_onMap}")
    if robot_onMap[0] > goal_onMap[0] and robot_onMap[1] < goal_onMap[1]:
        return True
    return False

def agentIsTopLeftOfGoal(robot_onMap, goal_onMap):
    print(f"agentIsTopLeftOfGoal - robot_onMap]{robot_onMap}, goal_onMap={goal_onMap}")
    if robot_onMap[0] < goal_onMap[0] and robot_onMap[1] < goal_onMap[1]:
        return True
    return False


# This function is to check if the obtacles and agent are in the 5x5
def check_obstacle(pos, obs_list):
  logger.log(f"check_obstacle - pos={pos}", True)  
  obstacles=[]
  robot_loc_onMap, _ = find_location_onMap(pos)
  logger.log(f"check_obstacle - robot_loc_onMap={robot_loc_onMap}", True)
  for i in obs_list:
    obs_loc_onMap, _ = find_location_onMap(i)
    logger.log(f"check_obstacle - obs_loc_onMap={obs_loc_onMap}", True)

    obs_loc_onGrid = find_location_onGrid(robot_loc_onMap, obs_loc_onMap)
    if isOutOfBounds(obs_loc_onGrid[0],obs_loc_onGrid[1]):
      logger.log(f"{obs_loc_onGrid} is NOT in the range of 5x5 square", True)
    else: 
      logger.log(f"{obs_loc_onGrid} is in the range of 5x5 square", True)
      obstacles.append(i)

    logger.log(f"check_obstacle - obstacles={obstacles}", True)

  return obstacles

# This function is to check if the obtacles and agent are in the same 3x3
def check_obstacle_3x3(pos, obs_list):
  logger.log(f"check_obstacle_3x3 - pos={pos}", True)  
  obstacles=[]
  robot_loc_onMap, _ = find_location_onMap(pos)
  logger.log(f"check_obstacle_3x3 - robot_loc_onMap={robot_loc_onMap}", True)
  for i in obs_list:
    obs_loc_onMap, _ = find_location_onMap(i)
    logger.log(f"check_obstacle_3x3 - obs_loc_onMap={obs_loc_onMap}", True)

    obs_loc_onGrid = find_location_onGrid(robot_loc_onMap, obs_loc_onMap)
    x = obs_loc_onGrid[0]
    y = obs_loc_onGrid[1]
    if x < 1 or x > 3 or y < 1 or y > 3:
      logger.log(f"{obs_loc_onGrid} is NOT in the range of 3x3 square", True)
    else: 
      logger.log(f"{obs_loc_onGrid} is in the range of 3x3 square", True)
      obstacles.append(i)

    logger.log(f"check_obstacle_3x3 - obstacles={obstacles}", True)
  return obstacles


def runMonteCarlo(end_state, obs_location_onMap_array):
    newEndState = invertCoordinate(end_state)
    newObs_location_onMap_array = [invertCoordinate(location) for location in obs_location_onMap_array]
    return montecarlo.calculate_gridworld_policy(newEndState, newObs_location_onMap_array)

def invertCoordinate(pos):
    return (pos[1],pos[0])
