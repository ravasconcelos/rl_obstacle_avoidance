
import simpleguitk as simplegui
import math
import random
import sonar
import sonar_array
import constants
import utils
import robot



       
#define globals

g_state = "None"

start_pos = [10,10]
robot_pos = [10, 10]
robot_co = 1

goal_pos = [500,500]
#obstacle_list = [(300, 213), (310, 124), (250, 110), (300, 230)]
full_obstacle_list = [(10,200),(250, 110), (200,280),(220,200), (300,300), (200,100), (400,150),(400, 110), 
                 (430, 390), (201, 304), (135, 281), 
                 (286, 373), (175, 280), (250, 375), (139, 327), (369, 278), 
                 (295, 196), (210, 111),(100,100),(110,110),(79,250)]
#create a robot with 6 sensors

n_sensor = 16 

#create a sonar array
#s1 = Sonar_Array(n_sensor, SENSOR_FOV, SENSOR_MAX_R, robot_co)
r1 = robot.Robot(robot_pos, robot_co, n_sensor, goal_pos)

r1.update(full_obstacle_list, goal_pos)
#define event handlers

def click(pos):
    global g_state, start_pos, goal_pos, robot_pos
    if g_state == "Start":
        start_pos = pos
        r1.set_pos(list(pos))
    elif g_state == "Goal":
        goal_pos = pos
        r1.set_co(utils.brg_in_deg(r1.get_pos(), pos))
    elif g_state == "Set Robot":
        r1.set_co(utils.brg_in_deg(r1.get_pos(), pos))
        r1.set_pos(list(pos))
        r1.delete_history()
    elif g_state == "Add Obs":
        full_obstacle_list.append(pos)
        print(full_obstacle_list)
        #update the robot
    r1.update(full_obstacle_list, goal_pos)
    g_state = "None"
        
def set_start():
    global g_state
    g_state = "Start"
    
def set_goal():
    global g_state
    g_state = "Goal"

def set_robot_pos():
    global g_state
    g_state = "Set Robot"

def alter_co(text):
    r1.set_co(float(text))
    r1.update()
            
def draw(canvas):
    #draw start 
    canvas.draw_circle(start_pos, 4, 3, "red")
    canvas.draw_text("S", [start_pos[0] + 10, start_pos[1] +10], 16, "red")
    #draw goal
    canvas.draw_circle(goal_pos, 4, 3, "green")
    canvas.draw_text("G", [goal_pos[0] + 10, goal_pos[1] +10], 16, "green")
    #draw the obstacles
    for obs in full_obstacle_list:
        canvas.draw_circle(obs,2,1, "red")
        canvas.draw_circle(obs,constants.OBSTACLE_RAD, 1, "white") 
    
    #draw sonar lines...
    r1.draw(canvas)

def step():
        r1.update()

def add_obs():
    global g_state
    g_state = "Add Obs"
    
    
#create simplegui controls

f1 = simplegui.create_frame("Obs Avoidance", 500, 500)
#btn_start = f1.add_button("Set Start", set_start, 100)
btn_goal = f1.add_button("Set Goal", set_goal, 100)
btn_robot = f1.add_button("Set Robot", set_robot_pos, 100)
txt_r_co = f1.add_input("Robot Co", alter_co, 100)
btn_step = f1.add_button("Step", step, 100)

btn_add_obs = f1.add_button("Add Obs", add_obs, 100)

f1.set_draw_handler(draw)
f1.set_mouseclick_handler(click)

#start simplegui

f1.start()