import math
import monte_carlo as montecarlo
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
# it convert 500X500 pixels word to 10x10 squars each with 12.5x12.5 pixxels
def find_location_onMap(pos):
    logger.log(f"find_location_onMap - pos={pos}")
    location_in_the_grid=[]
    location_in_the_map=[]
    x = pos[0]
    y = pos[1]
    location_in_the_map.append(int(x / constants.SMALL_GRID_SIZE))
    location_in_the_map.append(int(y / constants.SMALL_GRID_SIZE))
    logger.log(f"location_in_the_map={location_in_the_map}")
    rest_x = x % constants.SMALL_GRID_SIZE
    rest_y = y % constants.SMALL_GRID_SIZE
    location_in_the_grid.append(int(rest_x / (constants.SMALL_GRID_SIZE / 4)))
    location_in_the_grid.append(int(rest_y / (constants.SMALL_GRID_SIZE / 4)))
    logger.log(f"location_in_the_grid={location_in_the_grid}")
    return location_in_the_map, location_in_the_grid


def dynamic_policy_finder (mylocation, obs, master_policy, goal_pos):
    print(f"mylocation={mylocation}, obs={obs}, goal_pos={goal_pos}")
    
    mylocation_onMap, my_location_onGrid = find_location_onMap(mylocation)
    print(f"mylocation_onMap={mylocation_onMap}, my_location_onGrid={my_location_onGrid}")

    obs_location_onGrid_array = []

    for obstacle_pos in obs:
        obs_location_onGrid_array.extend(calculate_obstacle_onGrid(mylocation_onMap, obstacle_pos))
        print(f"obs_location_onGrid_array={obs_location_onGrid_array}")
    
    end_state = calculate_end_state_onGrid(mylocation, obs_location_onGrid_array, goal_pos)

    policy_key = f"{end_state}|{obs_location_onGrid_array}"
    print(f"policy_key={policy_key}")

    if policy_key in master_policy:
        policy = master_policy[policy_key]
        print("Saved policy:")
        montecarlo.print_policy_without_grid(policy)
    else:
        #policy = montecarlo.calculate_gridworld_policy(end_state, obs_location_onGrid_array)
        policy = runMonteCarlo(end_state, obs_location_onGrid_array)
        master_policy[policy_key] = policy
        print("Created policy:")
        montecarlo.print_policy_without_grid(policy)

    #policy= master_policy[obs_location_onGrid[0]][obs_location_onGrid[1]]
    direction = policy.get(invertCoordinate((my_location_onGrid[0],my_location_onGrid[1])), ' ')
    print(f"direction={direction}")
    return direction

# The obstacle can be in more than one space in the grid
#           U
#         L O R 
#           D  
def calculate_obstacle_onGrid(mylocation_onMap, obstacle_pos):
    logger.log(f"calculate_obstacle_onGrid - obstacle_pos={obstacle_pos}", True)
    obs_location_onGrid_array = []
    obs_onMap, obs_onGrid = find_location_onMap(obstacle_pos)
    logger.log(f"calculate_obstacle_onGrid - mylocation_onMap={mylocation_onMap}, obs_onGrid={obs_onGrid}", True)

    if mylocation_onMap == obs_onMap:
        obs_location_onGrid_array.append((obs_onGrid[0],obs_onGrid[1]))
        print(f"Robot and obstacle are in the same grid on the map")
    else:
        print(f"Robot and obstacle are NOT in the same grid on the map")

    # Up
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]-constants.OBSTACLE_RAD,obstacle_pos[1]])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - U border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added U border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)
    # Down
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]+constants.OBSTACLE_RAD,obstacle_pos[1]])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - D border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added D border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)
    # Left 
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0],obstacle_pos[1]-constants.OBSTACLE_RAD])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - L border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added L border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)
    # Right
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0],obstacle_pos[1]+constants.OBSTACLE_RAD])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - R border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added R border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)
    # North West
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]-constants.OBSTACLE_RAD,obstacle_pos[1]-constants.OBSTACLE_RAD])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - NW border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added NW border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)
    # North East
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]-constants.OBSTACLE_RAD,obstacle_pos[1]+constants.OBSTACLE_RAD])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - NE border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added NE border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)
    # South West
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]+constants.OBSTACLE_RAD,obstacle_pos[1]-constants.OBSTACLE_RAD])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - SW border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added SW border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)
    # South East
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]+constants.OBSTACLE_RAD,obstacle_pos[1]+constants.OBSTACLE_RAD])
    border_obs_onGrid = (border_obs_onGrid[0],border_obs_onGrid[1])
    logger.log(f"calculate_obstacle_onGrid - SE border_obs_onMap={border_obs_onMap}, border_obs_onGrid={border_obs_onGrid}")
    if border_obs_onMap == mylocation_onMap and (border_obs_onGrid not in obs_location_onGrid_array):
        logger.log(f"calculate_obstacle_onGrid - added SE border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append(border_obs_onGrid)

    return obs_location_onGrid_array

def calculate_end_state_onGrid(mylocation, obs_location_onGrid_array, goal_pos):

    logger.log(f"obs_location_onGrid_array={obs_location_onGrid_array}")

    all_end_states = [(0,0),(0,1),(2,0),(0,3),(1,0),(1,3),(2,3),(3,0),(3,1),(3,2),(3,3),(1,1),(1,2),(2,1),(2,2)]    
    logger.log(f"full all_end_states={all_end_states}")
    end_state = None

    for state in obs_location_onGrid_array:
        logger.log(f"state={state}")
        if state in all_end_states:
            logger.log(f"all_end_states.remove(state)")
            all_end_states.remove(state)   
    print(f"mylocation={mylocation}, goal_pos={goal_pos}, all_end_states={all_end_states}")

    best_end_states = getBestEndState(mylocation, goal_pos)
    print(f"best_end_states={best_end_states}")
    for state in best_end_states:
        if state not in obs_location_onGrid_array:
            end_state = state
            break

    logger.log(f"possible end_state={end_state}")

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
        end_states = [(2,3),(1,3),(0,3),(3,3)]
    # agent is below the target    
    elif agentIsBelowGoal(robot_onMap, goal_onMap):
        end_states = [(2,0),(1,0),(3,0),(0,0)]
    # agent is on the right of the target    
    elif agentIsRightOfGoal(robot_onMap, goal_onMap):
        end_states = [(0,1),(0,3),(0,0),(1,0)]
    # agent is on the left of the target    
    elif agentIsLeftOfGoal(robot_onMap, goal_onMap):
        end_states = [(3,2),(3,1),(3,3),(3,0)]
    # agent is in the bottom right of the target    
    elif agentIsBottonRightOfGoal(robot_onMap, goal_onMap):
        end_states = [(0,0),(1,0),(0,1),(2,0),(0,3)]
    # agent is in the top right of the target    
    elif agentIsTopRightOfGoal(robot_onMap, goal_onMap):
        end_states = [(0,3),(1,3),(2,3),(0,1),(0,0)]
    # agent is in the top left of the target    
    elif agentIsTopLeftOfGoal(robot_onMap, goal_onMap):
        end_states = [(3,3),(3,2),(2,3),(3,1),(1,3)]
    # agent is in the bottom left of the target    
    else:
        print(f"agent is in the bottom left of the target")
        end_states = [(3,0),(3,1),(2,0),(3,2),(1,0)]

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

def isNearby(pos1, pos2):
    if abs(pos1[0] - pos2[0]) <= 1 and abs(pos1[1] - pos2[1]) <= 1:
        return True
    return False  

# This function is to check if the obtacles are in the nearby grids
def check_obstacle(pos, obs_list):
  logger.log(f"check_obstacle - pos={pos}")  
  obstacles=[]
  robot_loc_onMap, _ = find_location_onMap(pos)
  logger.log(f"check_obstacle - robot_loc_onMap={robot_loc_onMap}")
  for i in obs_list:
    obs_loc_onMap, _ = find_location_onMap(i)
    logger.log(f"check_obstacle - obs_loc_onMap={obs_loc_onMap}")

    if isNearby(robot_loc_onMap, obs_loc_onMap):
      logger.log(f"obs_loc_onMap {obs_loc_onMap} is near to robot_loc_onMap {robot_loc_onMap}")
      obstacles.append(i)
    else: 
      logger.log(f"obs_loc_onMap {obs_loc_onMap} is NOT near to robot_loc_onMap {robot_loc_onMap}")

    logger.log(f"check_obstacle - obstacles={obstacles}", True)

  return obstacles    

def check_obstacle_in_this_grid(pos, obs_list):
  logger.log(f"check_obstacle_in_this_grid - pos={pos}", True)  
  mylocation_onMap, _ = find_location_onMap(pos)

  obs_location_onGrid_array = []

  for obstacle_pos in obs_list:
    obs_location_onGrid_array.extend(calculate_obstacle_onGrid(mylocation_onMap, obstacle_pos))
  print(f"obs_location_onGrid_array={obs_location_onGrid_array}")

  return len(obs_location_onGrid_array) > 0  
  
def runMonteCarlo(end_state, obs_location_onMap_array):
    newEndState = invertCoordinate(end_state)
    newObs_location_onMap_array = [invertCoordinate(location) for location in obs_location_onMap_array]
    return montecarlo.calculate_gridworld_policy(newEndState, newObs_location_onMap_array)

def invertCoordinate(pos):
    return (pos[1],pos[0])