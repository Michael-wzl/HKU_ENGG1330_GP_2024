import time
import sys
import os

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from . import Animation
from . import art_data

def display_end_scene_success(stdscr):
    stdscr.clear()
    stdscr.refresh()
    time.sleep(0.1)

    fireworks_animation = Animation.Animation(frames = art_data.end.success.fireworks(),replay_times=2,speed=0.1)
    fireworks_animation.display(stdscr,'stop_motion')
    time.sleep(1)

    naration_animation = Animation.Animation(text = art_data.end.success.naration(),speed=0.01,acceleration=0)
    naration_animation.display(stdscr,'gradual_appear_words')
    time.sleep(5)  

    end_animation = Animation.Animation(text = art_data.end.end.end())
    end_animation.display(stdscr,'appear')
    time.sleep(2)
