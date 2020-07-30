import math
import random
import sonar
import sonar_array
import constants
import utils

#define constants
master_policy={}
I_was_here=[0,0]

class Robot:
    def __init__(self, pos, co, n_sensor,goal_pos):
        self.pos = pos
        self.history = [pos]
        self.co = co
        self.spd = 10 # robot speed in pixels/ step
        self.s_array = sonar_array.Sonar_Array(n_sensor, constants.SENSOR_FOV, constants.SENSOR_MAX_R, self.co)
        self.goal_brg = utils.brg_in_deg(self.pos, goal_pos)
        self.obstacles_in_view = []
    
    def get_obstacles_in_view(self):
        return self.obstacles_in_view
    
    def update(self, full_obstacle_list, goal_pos):
        self.obstacles_in_view = [] #delete all the old obstacles in view
        for obs in full_obstacle_list:
            if utils.dist(self.pos, obs) < constants.SENSOR_MAX_R:
                self.obstacles_in_view.append(obs)
                
        #re-calculate direction to goal
        self.goal_brg = utils.brg_in_deg(self.pos, goal_pos)
        #re-estimate sensor output by weighted sum method
        co1, need_turn = self.s_array.update(self.pos, self.goal_brg, self.obstacles_in_view, "w_sum", full_obstacle_list,master_policy,I_was_here,goal_pos)
        #print "Path Clear:", self.path_is_clear()
        if self.path_is_clear(goal_pos):#can we reach the goal directly from here?
            self.co = utils.brg_in_deg(self.pos, goal_pos)
            print("path clear. ignoring recommendation")
        elif need_turn: #do we need to turn
            self.co = co1
            print("path not clear. following recommendation")
        else: # path is not fully clear, but there are no immediate obstacles
            pass
            #self.co = brg_in_deg(self.pos, goal_pos)

        #m5e the robot by one step...
        self.move(2)
        print(f"master_policy.keys()={master_policy.keys()}")

    def path_is_clear(self, goal_pos):#return True if there is a clear path to the goal
        goal_brg = utils.brg_in_deg(self.pos, goal_pos)
        for obs in self.obstacles_in_view:
            if utils.dist(self.pos, goal_pos) > utils.dist(self.pos, obs):
                d_obs, obs_brg = utils.dist_and_brg_in_deg(self.pos, obs)
                rel_brg = abs(utils.relative_brg(goal_brg, obs_brg))

                print(f"rel_brg={rel_brg}")
                rel_brg_radians = math.radians(rel_brg)
                print(f"rel_brg_radians={rel_brg_radians}")
                if rel_brg_radians < -1 or rel_brg_radians > 1:
                    return False

                d_lateral = abs(d_obs * math.asin(math.radians(rel_brg)))
                if d_lateral < constants.OBSTACLE_RAD + constants.ROBOT_RAD: 
                    return False
        return True
    
    def move(self, dT):
        print("VVVVVBVV")        
        print((self.co))
        u_vec = utils.angle_to_vector(self.co)
        
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
   
    def draw(self, canvas):
        #Draw the robot
        canvas.draw_circle(self.pos, 4, 3, "yellow")
        canvas.draw_text("R", [self.pos[0] + 10, self.pos[1] +10], 16, "yellow")
        #Draw brg line to goal
        self.goal_vec = utils.create_vector(self.pos, 150, self.goal_brg)
        canvas.draw_line(self.pos, self.goal_vec, 2, "teal")
        #Draw current heading vector
        self.co_vec = utils.create_vector(self.pos, 150, self.co)
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
