import time
import sys
import os

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from . import Animation
from . import art_data


def display_start_scene_nofirst(stdscr):
    welcome_animation = Animation.Animation(text = art_data.start.welcome.welcome())
    welcome_animation.display(stdscr,'appear')
    time.sleep(1.5)