import time
import sys
import os

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from . import Animation
from . import art_data

def display_start_scene(stdscr):
    stdscr.clear()
    stdscr.refresh()
    time.sleep(0.01)

    exhale_animation = Animation.Animation(text = art_data.start.scream.exhale(),speed = 1,acceleration = 0.1)
    exhale_animation.display(stdscr,'gradual_appear_words')
    time.sleep(0.5)

    scream_animation = Animation.Animation(text = art_data.start.scream.scream(),speed = 0.05,acceleration = 0)
    scream_animation.display(stdscr,'gradual_appear_letters')

    scream_narrate_1 = Animation.Animation(text = art_data.start.scream.narrate_1(),speed=0.01,acceleration=0)
    scream_narrate_1.display(stdscr,'gradual_appear_words')
    time.sleep(3)
    scream_narrate_2 = Animation.Animation(text = art_data.start.scream.narrate_2(),speed=0.01,acceleration=0)
    scream_narrate_2.display(stdscr,'gradual_appear_words')
    time.sleep(5)
    scream_narrate_3 = Animation.Animation(text = art_data.start.scream.narrate_3(),speed=0.01,acceleration=0)
    scream_narrate_3.display(stdscr,'gradual_appear_words')
    time.sleep(3)

    welcome_animation = Animation.Animation(text = art_data.start.welcome.welcome())
    welcome_animation.display(stdscr,'appear')
    time.sleep(1.5)

    walk_animation = Animation.Animation(frames = art_data.start.walking.walking(),replay_times=1,speed=0.8)
    walk_animation.display(stdscr,'stop_motion')
    time.sleep(1)

    notice_1_animation = Animation.Animation(text = art_data.start.notice.notice_1())
    notice_1_animation.display(stdscr,'appear')
    time.sleep(12)
    notice_2_animation = Animation.Animation(text = art_data.start.notice.notice_2())
    notice_2_animation.display(stdscr,'appear')
    time.sleep(10)