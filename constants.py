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
All other files read the constants from here
'''

FRAME_SIZE = 500 # Window size when playing with UI
SMALL_GRID_SIZE = 50 # Small grid size (white square in UI)
OBSTACLE_RAD = 12.5 # how big (radius) are the obstacles
ROBOT_RAD = 50 # how big (radius) is the robot?
SENSOR_FOV = 10.0 # FOV of each sensor THIS MUST BE A FLOAT!!!!!! 
SENSOR_MAX_R = 20 # max range that each sensor can report
SENSOR_ALERT_R = 20 #range within which sensor reports are acted upon
TURN_SCALE_FACTOR = 2 # how drastic do we want the turns to be
SAFETY_DISTANCE = 20 # distance the robot tries to be far from obstacles in Bayesian algo

N_SENSOR = 16 # number of sensors
N_OBSTACLES = 16 # number of obstacles in the test data
N_EPISODES = 200 # number of episodes when running in batch mode