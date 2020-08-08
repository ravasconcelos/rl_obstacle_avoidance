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
Implementing a robot obstacle avoidance algorithm.
Adapted from https://bayesianadventures.wordpress.com/2015/08/31/obstacle-avoidance-for-clever-robots/
'''

import math
import random
import sys
sys.path.insert(0,'..')
import constants

def rel_brg_fm_offset_sensor(true_hdg, sensor_offset, tgt_brg):
    #given robot's true heading, the sensor offset angle and the
    #true brg of the target, this fn will return the relative brg
    #of the target from the sensor's line of sight
    
    sensor_look_brg = (true_hdg + sensor_offset)%360
    tgt_rel_fm_sensor = tgt_brg - sensor_look_brg

    if tgt_rel_fm_sensor < -180:
        tgt_rel_fm_sensor += 360
    
    return tgt_rel_fm_sensor

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
    print(f"dist - p1={p1}, p0={p0}")
    return math.sqrt((p1[0] - p0[0])**2+(p1[1]-p0[1])**2)

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

def angle_to_vector(ang):#resolve angles into vectors
    ang = math.radians(ang)
    return [math.cos(ang), math.sin(ang)]

def relative_brg(b1, b2):
    rb = b2 - b1
    if rb > 180:
        rb = 360 - rb
    if rb < -180:
        rb += 360
        rb *= -1
    return rb

def create_vector(from_pos, length, brg):       
        u_vec = angle_to_vector(brg)
        #print "generating target line..."
        vec0 = from_pos[0] + length * u_vec[1] 
        vec1 = from_pos[1] - length * u_vec[0]
        
        return [vec0, vec1]

    
#define classes

class Sonar:
    def __init__(self, index, FOV, max_r, robot_co):
        #create a instance of this class
        self.pos = [0,0]
        self.index = index
        self.max_r = max_r
        self.offset =  index * FOV #+ FOV/2 # on what relative bearing is this sensor looking?
        self.look_brg = (robot_co + self.offset)%360
        self.vec = [0,0] # just a vector for grpahical ouptut of pings
        self.has_valid_echo = False #indicates if this sonar has a "valid" obstacle in sight
        #print "Creating Sonar:" , index, " offset ", self.offset, "true LOS:", self.look_brg
            
    def ping_actual():#ping for real in a robot and return range observed
        pass
    
    def ping_simulated(self, obstacle_list, robot_co):
        #from robot position and robot_co, run through obs_list
        #return the distance to closest object within 
        #FOV and within self.max_r of THIS SENSOR
        # range all the obstacles in view, find the nearest
        
        range_list = []
        
        for obs in obstacle_list:# find objects within max_r and inside FOV
            #print "pinging for robot_co:", robot_co
            can_observe, d = self.can_observe(robot_co, obs, constants.OBSTACLE_RAD)
            #print can_observe, d
            if can_observe:
                range_list.append(d) 
        if len(range_list) > 0:
            self.output = min(range_list)- constants.SAFETY_DISTANCE
        else:
            self.output = constants.SENSOR_MAX_R
        #print "closest point: " , obs , " distance:", self.output
    
    def get_output(self):
        return self.output
    
    def can_observe(self, robot_co, obstacle_pos, obstacle_rad):
        #if obstacle is within within the max_r of the sensor
        #and within FOV, return True and the distance observed
        #else return False, 0
        
        dist, brg = dist_and_brg_in_deg(self.pos, obstacle_pos)
        
        if dist < self.max_r: #if the object is within max_r....
            rel_brg = rel_brg_fm_offset_sensor(robot_co, self.offset, brg)#rel brg of tgt from sensor LOS

            if math.radians(rel_brg) < -1 or math.radians(rel_brg) > 1:
                return False, 0

            d_test = abs(dist * math.asin(math.radians(rel_brg)))
            if d_test < constants.OBSTACLE_RAD + constants.ROBOT_RAD: 
                self.has_valid_echo = True
                return True, dist # if the object is within min allowed lateral separation
            else:
                self.has_valid_echo = False
                return False, 0 # ignore it
        else:#if the object is outside max_r of this sonar...ignore it
            self.has_valid_echo = False
            return False, 0
      
    def update(self, platform_pos, platform_co, obstacle_list):
              
        #update own parameters
        self.pos = platform_pos
        
        self.look_brg = (platform_co + self.offset)%360
        
        #calculate output of this sensor
        
        self.ping_simulated(obstacle_list, platform_co)
        
        self.vec = create_vector(self.pos, self.output + constants.ROBOT_RAD, self.look_brg)#calculate distance vector for drawing on canvas
        
        #print "sensor index:", self.index, " look brg:", self.look_brg
    def draw(self, canvas): # draw the sensor's output
        #if self.has_valid_echo:
        canvas.draw_line(self.pos,self.vec, 1, 'lime')
        canvas.draw_text(str(self.index),(self.vec[0]+4, self.vec[1]+4), 10, "lime"),
        #print self.index, " VE:" , self.has_valid_echo
        
# It has some utility functions for the group of sensors
class Sonar_Array:
    def __init__(self, n_sensor, SENSOR_FOV, SENSOR_MAX_R, robot_co):
        self.sonar_list = []
        self.need_diversion_flag = False
        self.n_sensor = n_sensor
        
        i_pos = list(range(1, int(n_sensor/2) + 1))
        i_neg = list(range(int(-n_sensor/2) , 0))
        i_pos.reverse()
        i_neg.reverse()
        i_pos.extend(i_neg)
        
        for i in i_pos:#create a list of individual sonars...
            self.sonar_list.append(Sonar(i, SENSOR_FOV, SENSOR_MAX_R, robot_co))
   
    # called by the robot to get the direction of the next movement
    def update(self, robot_pos, robot_co, obstacle_list, method):
        #update sonar array
        for sonar in self.sonar_list:#update output of each sensor
            sonar.update(robot_pos, robot_co, obstacle_list)
            
        if method == "w_sum":#process data by method of weighted sums
            return self.weighted_sum_method(robot_pos, robot_co)
    
    def weighted_sum_method(self, robot_pos, robot_co):
        #process data by the weighted sum method and 
        #return (1) whether turn is required or not (2) index of recommended sonar LOS to turn to
        sum_d = 0
        sum_wt = 0
        alert = False
        #print "checking all sonars:"      
        for sonar in self.sonar_list:
            #print "sonar:", sonar.index, " range:", sonar.output
            if sonar.output < constants.SENSOR_ALERT_R:#has this sonar found anything in danger zone?
                alert = True
                #print "obstacle found by index ", sonar.index
                for s1 in self.sonar_list: #process the whole array
                    d = int(s1.output)
                    gain = 1#SENSOR_MAX_R/(SENSOR_MAX_R - d)
                    sum_d +=  d
                    sum_wt += s1.index * d * gain
                    #print "I:", s1.index,",D:",int(s1.output), ",sum_D:", sum_d, "sum_wt:",sum_wt
                if sum_d == 0:
                    print("sum_d == 0 is this a bug??? what to do?")
                    sum_d = 1
                rec_index = math.ceil(constants.TURN_SCALE_FACTOR * float(sum_wt)/sum_d) #index of sonar with best LOS
                if abs(rec_index) > self.n_sensor/2:
                    print("rec index too large")
                    rec_index = self.n_sensor/2
                print("Rec index:", rec_index) 
                break # processing completed
            else: #no obstacle in danger zone
                rec_index = 0
        #print "break from loop."
        if rec_index == 0 and alert == True:
            print("alert with no alteration")
            return robot_co, False
        elif abs(rec_index) > 0: # some alteration recommended
            print("turn recommended")
            offset =  rec_index * constants.SENSOR_FOV #how much is the angular offset
            return (robot_co + offset)%360, True
        else:# no diversion needed
            print("no alert no diversion")
            return robot_co, False
    
    # draw the sonar
    def draw(self, canvas):
        for sonar in self.sonar_list:
            sonar.draw(canvas)

# Robot is the agent.
# It knows its position and the goal position
class Robot:
    def __init__(self, pos, co, n_sensor, goal_pos):
        self.steps = 0
        self.pos = pos
        self.history = [pos]
        self.co = co
        self.spd = 10 # robot speed in pixels/ step
        self.s_array = Sonar_Array(n_sensor, constants.SENSOR_FOV, constants.SENSOR_MAX_R, self.co)
        self.goal_brg = brg_in_deg(self.pos, goal_pos)
        self.obstacles_in_view = []
        self.goal_pos = goal_pos
        
    
    def get_obstacles_in_view(self):
        return self.obstacles_in_view
    
    # this is the most important methond, which moves the agent in the environment
    def update(self, full_obstacle_list, goal_pos):
        self.steps += 1
        self.obstacles_in_view = [] #delete all the old obstacles in view
        for obs in full_obstacle_list:
            if dist(self.pos, obs) < constants.SENSOR_MAX_R:
                self.obstacles_in_view.append(obs)
                
        #re-calculate direction to goal
        self.goal_brg = brg_in_deg(self.pos, goal_pos)
        #re-estimate sensor output by weighted sum method
        co1, need_turn = self.s_array.update(self.pos, self.goal_brg, self.obstacles_in_view, "w_sum")
        if self.path_is_clear(goal_pos):#can we reach the goal directly from here?
            self.co = brg_in_deg(self.pos, goal_pos)
        elif need_turn: #do we need to turn
            self.co = co1
        else: # path is not fully clear, but there are no immediate obstacles
            pass

        #move the robot by one step...
        self.move(1)
        return self.has_hit_obstacle(full_obstacle_list), self.has_reached_goal(goal_pos)

    #return True if there is a clear path to the goal
    def path_is_clear(self, goal_pos):#return True if there is a clear path to the goal
        goal_brg = brg_in_deg(self.pos, goal_pos)
        for obs in self.obstacles_in_view:
            if dist(self.pos, goal_pos) > dist(self.pos, obs):
                d_obs, obs_brg = dist_and_brg_in_deg(self.pos, obs)
                rel_brg = abs(relative_brg(goal_brg, obs_brg))
                rel_brg_radians = math.radians(rel_brg)
                print(f"rel_brg_radians={rel_brg_radians}")
                if rel_brg_radians < -1 or rel_brg_radians > 1:
                    print(f"invalid rel_brg_radians={rel_brg_radians}")
                    return False
                d_lateral = abs(d_obs * math.asin(rel_brg_radians))
                if d_lateral < constants.OBSTACLE_RAD + constants.ROBOT_RAD: 
                    return False
        return True

    # detect if the robot has reached the goal
    def has_reached_goal(self, goal_pos):
        print(f"self.pos={self.pos}, goal_pos={goal_pos}")
        x = self.pos[0]
        y = self.pos[1]
        radius = 12.5
        center_x = goal_pos[0]
        center_y = goal_pos[1]
        print(f"x={x}, y={y}, center_x={center_x}, center_y={center_y}")
        if (x - center_x)**2 + (y - center_y)**2 < radius**2:
            print("WE REACHED THE GOAL! CONGRATS!!!!")
            return True
        return False
    
    # detect if the robot has hit an obstacle
    def has_hit_obstacle(self, full_obstacle_list):
        print(f"self.pos={self.pos}, full_obstacle_list={full_obstacle_list}")
        x = self.pos[0]
        y = self.pos[1]
        radius = 12.5

        for obstacle_pos in full_obstacle_list:
            center_x = obstacle_pos[0]
            center_y = obstacle_pos[1]
            print(f"x={x}, y={y}, center_x={center_x}, center_y={center_y}")
            if (x - center_x)**2 + (y - center_y)**2 < radius**2:
                print("WE HIT THE OBSTACLE! START CRYING!!!!")
                return True
        return False
    
    def move(self, dT):
                
        u_vec = angle_to_vector(self.co)
        
        self.pos[0] += self.spd * dT * u_vec[1]
        self.pos[1] -= self.spd * dT * u_vec[0]
        
        self.history.append([self.pos[0], self.pos[1]])
        
    def get_pos(self):
        return self.pos
    
    def set_pos(self, pos):
        self.pos = pos
    
    def set_co(self, co):
        self.co = co
        #print "setting robot co:", self.co
    
    def delete_history(self):
        self.history = []

    # draw the robot in the ui
    def draw(self, canvas):
        #Draw the robot
        canvas.draw_circle(self.pos, 4, 3, "yellow")
        canvas.draw_text("R", [self.pos[0] + 10, self.pos[1] +10], 16, "yellow")
        #Draw brg line to goal
        self.goal_vec = create_vector(self.pos, 150, self.goal_brg)
        canvas.draw_line(self.pos, self.goal_vec, 2, "teal")
        #Draw current heading vector
        self.co_vec = create_vector(self.pos, 150, self.co)
        canvas.draw_line(self.pos, self.co_vec, 2, "white")
        #draw the output of the sonar array
        self.s_array.draw(canvas)
        #draw the obstacles in view
        for obs in self.obstacles_in_view:
            canvas.draw_circle(obs,2,1, "red")
            canvas.draw_circle(obs,constants.OBSTACLE_RAD, 1, "green") 
        #draw history
        for point in self.history:
            canvas.draw_circle(point,2,2, "lime")        
        
        canvas.draw_text(f"Steps = {self.steps}", (5, 500), 12, 'White')
        
