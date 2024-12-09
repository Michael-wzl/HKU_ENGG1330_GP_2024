import time
import sys
import os

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from . import Animation
from . import art_data

def display_end_scene_fail(stdscr):
    stdscr.clear()
    stdscr.refresh()
    time.sleep(1)

    ghost_animation = Animation.Animation(text = art_data.end.fail.ghost())
    ghost_animation.display(stdscr,'appear')
    time.sleep(1)

    naration_animation = Animation.Animation(text = art_data.end.fail.naration(),speed=0.01,acceleration=0)
    naration_animation.display(stdscr,'gradual_appear_words')
    time.sleep(3)

    end_animation = Animation.Animation(text = art_data.end.end.end())
    end_animation.display(stdscr,'appear')
    time.sleep(2)
