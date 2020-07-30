import math
import random
import constants
import utils

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
        
        dist, brg = utils.dist_and_brg_in_deg(self.pos, obstacle_pos)
        
        if dist < self.max_r: #if the object is within max_r....
            rel_brg = utils.rel_brg_fm_offset_sensor(robot_co, self.offset, brg)#rel brg of tgt from sensor LOS
            print(f"dist={dist}, rel_brg={rel_brg}")
            rel_brg_radians = math.radians(rel_brg)
            print(f"rel_brg_radians={rel_brg_radians}")
            if rel_brg_radians < -1 or rel_brg_radians > 1:
                return False, 0
            print(f"math.asin(math.radians(rel_brg))={math.asin(math.radians(rel_brg))}")
            print(f"abs(dist * math.asin(math.radians(rel_brg)))={abs(dist * math.asin(math.radians(rel_brg)))}")
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
        
        self.vec = utils.create_vector(self.pos, self.output + constants.ROBOT_RAD, self.look_brg)#calculate distance vector for drawing on canvas
        
        #print "sensor index:", self.index, " look brg:", self.look_brg
    def draw(self, canvas): # draw the sensor's output
        #if self.has_valid_echo:
        canvas.draw_line(self.pos,self.vec, 1, 'lime')
        canvas.draw_text(str(self.index),(self.vec[0]+4, self.vec[1]+4), 10, "lime"),
        #print self.index, " VE:" , self.has_valid_echo