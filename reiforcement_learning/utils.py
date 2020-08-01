import math
import monte_carlo as montecarlo
import numpy as np
import random
import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../')
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


'''  
  i=0
  i1=0
  loc=0
  loc1=0
  for squares in range(0,10):
    i1=0
    for quare in range(0,10):
      loc=0
      #square.append((i,i1))
      if (pos[0]>i and pos[0]<=i+50) and (pos[1]>i1 and pos[1]<=i1+50):
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

  if len(location_in_the_grid) == 2:
    #To to convert to 4x4 grid each is 12.5 X 12.5 pixels
    location_in_the_grid[0]=int(location_in_the_grid[0]/12.5)
    location_in_the_grid[1]=int(location_in_the_grid[1]/12.5)
    #To to convert to 5x5 map each sqaure is 100X100 pixel
    location_in_the_map[0]=int(location_in_the_map[0]/50)
    location_in_the_map[1]=int(location_in_the_map[1]/50)
  else:
    print(f"Some bug here... pos={pos}")  
    location_in_the_grid.append(0)      
    location_in_the_grid.append(0)      
    location_in_the_map.append(0)      
    location_in_the_map.append(0)      
  return location_in_the_map, location_in_the_grid
'''

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

# The obstacle can be in more than one space in the grid
#           U
#         L O R 
#           D  
def calculate_obstacle_onGrid(obstacle_pos):
    logger.log(f"calculate_obstacle_onGrid - obstacle_pos={obstacle_pos}")
    obs_location_onGrid_array = []
    obs_onMap, obs_onGrid = find_location_onMap(obstacle_pos)
    logger.log(f"calculate_obstacle_onGrid - obs_onGrid={obs_onGrid}")
    obs_location_onGrid_array.append((obs_onGrid[0],obs_onGrid[1]))
    # Up
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]-constants.OBSTACLE_RAD,obstacle_pos[1]])
    if border_obs_onGrid != obs_onGrid and border_obs_onMap == obs_onMap:
        logger.log(f"calculate_obstacle_onGrid - U border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append((border_obs_onGrid[0],border_obs_onGrid[1]))
    # Down
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0]+constants.OBSTACLE_RAD,obstacle_pos[1]])
    if border_obs_onGrid != obs_onGrid and border_obs_onMap == obs_onMap:
        logger.log(f"calculate_obstacle_onGrid - D border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append((border_obs_onGrid[0],border_obs_onGrid[1]))
    # Left 
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0],obstacle_pos[1]-constants.OBSTACLE_RAD])
    if border_obs_onGrid != obs_onGrid and border_obs_onMap == obs_onMap:
        logger.log(f"calculate_obstacle_onGrid - L border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append((border_obs_onGrid[0],border_obs_onGrid[1]))
    # Right
    border_obs_onMap, border_obs_onGrid = find_location_onMap([obstacle_pos[0],obstacle_pos[1]+constants.OBSTACLE_RAD])
    if border_obs_onGrid != obs_onGrid and border_obs_onMap == obs_onMap:
        logger.log(f"calculate_obstacle_onGrid - R border_obs_onGrid={border_obs_onGrid}")
        obs_location_onGrid_array.append((border_obs_onGrid[0],border_obs_onGrid[1]))
    return obs_location_onGrid_array

def calculate_end_state_onGrid(mylocation, obs_location_onGrid_array, goal_pos):

    print(f"obs_location_onGrid_array={obs_location_onGrid_array}")

    possible_end_states = [(0,0),(0,1),(0,2),(0,3),(1,0),(1,3),(2,3),(3,0),(3,1),(3,2),(3,3),]    
    possible_end_states_in_the_middle = [(1,1),(1,2),(2,1),(2,2)]    
    print(f"full possible_end_states={possible_end_states}")
    end_state = None

    for state in obs_location_onGrid_array:
        print(f"state={state}")
        if state in possible_end_states:
            print(f"possible_end_states.remove(state)")
            possible_end_states.remove(state)   
        if state in possible_end_states_in_the_middle:
            print(f"possible_end_states_in_the_middle.remove(state)")
            possible_end_states_in_the_middle.remove(state)   
    print(f"mylocation={mylocation}, goal_pos={goal_pos}, possible_end_states={possible_end_states}")

    # agent is in the bottom right of the target    
    if mylocation[0] > goal_pos[0] and mylocation[1] > goal_pos[1]:
        end_state = (0,0)
    # agent is in the top right of the target    
    elif mylocation[0] > goal_pos[0] and mylocation[1] < goal_pos[1]:
        end_state = (3,0)
    # agent is in the top left of the target    
    elif mylocation[0] < goal_pos[0] and mylocation[1] < goal_pos[1]:
        end_state = (3,3)
    # agent is in the bottom left of the target    
    else:
        end_state = (0,3)

    print(f"possible end_state={end_state}")

    if end_state not in possible_end_states:
        end_state = random.choice(possible_end_states)        

    if end_state is None and len(possible_end_states_in_the_middle) > 0:
        print("Interesting... we a reunning out of options... let's try the middle")
        end_state = random.choice(possible_end_states_in_the_middle)

    if end_state is None:
        print("The grid is full of obstacles... expect a bug")
    print(f"final end_state={end_state}")

    return end_state     