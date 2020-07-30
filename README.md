# Title: Robot obstacle avoidance with reinforcement learning
Haithan came here
## Group Members:
    1. Alexandre Dietrich
    2. Ankur Tyagi
    3. Haitham Alamri
    4. Rodolfo Vasconcelos

## Installation

1) See pip_list for the library version
2) Download and install Xming: https://sourceforge.net/projects/xming/
3) set display:
```
export DISPLAY=localhost:0
```

Error:

```
(venv) rodolfo@WS571:/c/personal/uot/reinforcement/term_proj/rl_obstable_avoidance/bayesian$ python baysian_obs_avoid.py
no alert no diversion
path clear. ignoring recommendation
Traceback (most recent call last):
  File "baysian_obs_avoid.py", line 408, in <module>
    f1 = simplegui.create_frame("Obs Avoidance", 1000, 800)
  File "/mnt/c/personal/uot/reinforcement/term_proj/gym-minigrid/venv/lib/python3.7/site-packages/simpleguitk/frame.py", line 114, in create_frame
    return Frame(title, canvas_width, canvas_height, control_width)
  File "/mnt/c/personal/uot/reinforcement/term_proj/gym-minigrid/venv/lib/python3.7/site-packages/simpleguitk/frame.py", line 47, in __init__
    self._root = self._create_root(title)
  File "/mnt/c/personal/uot/reinforcement/term_proj/gym-minigrid/venv/lib/python3.7/site-packages/simpleguitk/frame.py", line 24, in _create_root
    root = tkinter.Tk()
  File "/usr/lib/python3.7/tkinter/__init__.py", line 2023, in __init__
    self.tk = _tkinter.create(screenName, baseName, className, interactive, wantobjects, useTk, sync, use)
_tkinter.TclError: no display name and no $DISPLAY environment variable
(venv) rodolfo@WS571:/c/personal/uot/reinforcement/term_proj/rl_obstable_avoidance/bayesian$ echo $DISPLAY

(venv) rodolfo@WS571:/c/personal/uot/reinforcement/term_proj/rl_obstable_avoidance/bayesian$ export DISPLAY=localhost:0
(venv) rodolfo@WS571:/c/personal/uot/reinforcement/term_proj/rl_obstable_avoidance/bayesian$ python baysian_obs_avoid.py
```
