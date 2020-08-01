DEBUG = False

def log(message = "", info = False):
    if info:
        print(message)
        return
    if DEBUG:
        print(message)
