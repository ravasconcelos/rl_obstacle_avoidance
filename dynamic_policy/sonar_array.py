import math
import random
import sonar
import constants
import utils

EPISILON = 0.05

# add some random ness
def skip_the_policy():
    if EPISILON > random.random():
        return True
    return False





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
        
        obs=utils.check_obstacle(robot_pos,full_obstacle_list)
               
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
            return offset, False
        #if (I_was_here[-2]==robot_pos):
            #return robot_co+45, True
        print("Robot positon",robot_pos)
        print("*********")
        print("Robot Co",robot_co)
        print("New Direction",(offset%robot_co)+robot_co)
        print("******")                        
        return offset, True

    def draw(self, canvas):
        for sonar in self.sonar_list:
            sonar.draw(canvas)