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
Logger is used to reduce the prints in the console, when the system is not executed in debug mode
'''

# When this flag is false the messages are not printed
DEBUG = False

# if info flag is True the message is print even when if debug flag is false
def log(message = "", info = False):
    if info:
        print(message)
        return
    if DEBUG:
        print(message)
