import math
import random
import sonar
import constants
import utils

# This function is to check if the obtacles and agent are in the same 12.5x12.5 pixels sqaure
def check_obstacle(pos, obs_list):
  obstacles=[]
  location_on_map,location_on_grid = utils.find_location_onMap(pos)
  for i in obs_list:
    location_on_map1,location_on_grid1 = utils.find_location_onMap(i)
    if (location_on_map1 == location_on_map):
      obstacles.append(i)
  return obstacles
  #return None

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
            self.sonar_list.append(sonar.Sonar(i, SENSOR_FOV, SENSOR_MAX_R, robot_co))
   
    def update(self, robot_pos, robot_co, obstacle_list, method,full_obstacle_list,master_policy,I_was_here,goal_pos):
        #update sonar array
        for sonar in self.sonar_list:#update output of each sensor
            sonar.update(robot_pos, robot_co, obstacle_list)
            
        #if method == "w_sum":#process data by method of weighted sums
        return self.weighted_sum_method(robot_pos, robot_co,full_obstacle_list,master_policy,I_was_here,goal_pos)
    
    def weighted_sum_method(self, robot_pos, robot_co,full_obstacle_list,master_policy,I_was_here,goal_pos):

        print (f"weighted_sum_method, robot_pos={robot_pos}, robot_co={robot_co}")
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
            if sonar.output < constants.SENSOR_ALERT_R:#has this sonar found anything in danger zone?
                alert = True
                #print "obstacle found by index ", sonar.index
                for s1 in self.sonar_list: #process the whole array
                    d = int(s1.output)
                    gain = 1#SENSOR_MAX_R/(SENSOR_MAX_R - d)
                    sum_d +=  d
                    sum_wt += s1.index * d * gain
                    #print "I:", s1.index,",D:",int(s1.output), ",sum_D:", sum_d, "sum_wt:",sum_wt
                if sum_d != 0:    
                    rec_index = math.ceil(constants.TURN_SCALE_FACTOR * float(sum_wt)/sum_d) #index of sonar with best LOS
                #rec_index = int(TURN_SCALE_FACTOR * float(sum_d)/sum_wt)
                print (f"Rec index: {rec_index}")
                if abs(rec_index) > self.n_sensor/2:
                    print (f"rec index too large")
                    rec_index = self.n_sensor/2
#                    if rec_index < 0:
#                        rec_index = -n_sensor/2
#                    else:
#                        rec_index = n_sensor/2
                print (f"New Rec index: {rec_index}")
                #break # processing completed
            else: #no obstacle in danger zone
                rec_index = 0
                #return robot_co, False
                #print : index = ", sonar.index
        #print "break from loop."
        if rec_index == 0 and alert == True:
                print ("alert with no alteration")
                obs=check_obstacle(robot_pos,full_obstacle_list)
                print(f"obs={obs}")
               
                if len(obs) != 0:
                    action = utils.dynamic_policy_finder(robot_pos,obs,master_policy,goal_pos)
                    I_was_here.append(robot_pos)
                #if (len(obs)!=0 and len(obs)<2):
                #        action = policy_finder(robot_pos,obs)
                #        I_was_here.append(robot_pos)
                #elif(len(obs)==2):
                #        action = policy_finder2_obs(robot_pos,obs)
                #        I_was_here.append(robot_pos)
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
                            print ("policy recommend to go left ")
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
           offset =  rec_index * constants.SENSOR_FOV #how much is the angular offset  
           print(obs)
           obs=check_obstacle(robot_pos,full_obstacle_list)
           if(obs!=None):
            
                if len(obs) != 0:
                    action = utils.dynamic_policy_finder(robot_pos,obs,master_policy,goal_pos)
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
           offset =  rec_index * constants.SENSOR_FOV #how much is the angular offset  
           print(obs)
           obs=check_obstacle(robot_pos,full_obstacle_list)
           if(obs!=None):
                if len(obs) != 0:
                    action = utils.dynamic_policy_finder(robot_pos,obs,master_policy,goal_pos)
                    I_was_here.append(robot_pos)
                    print("chinca:1")
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
    
    def draw(self, canvas):
        for sonar in self.sonar_list:
            sonar.draw(canvas)