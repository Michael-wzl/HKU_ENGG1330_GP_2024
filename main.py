import curses
import time
import logging
import random
import os
import datetime

from backpack_pkg import Backpack
from gamemap_pkg import GameMap
from player_pkg import Player
from login_pkg import login_manager
from login_pkg import user_manager
from animation_pkg import display_end_scene_success
from animation_pkg import display_end_scene_fail
from animation_pkg import display_start_scene
from animation_pkg import display_algo
from animation_pkg import display_start_scene_nofirst
'''
def get_input(stdscr,promt):
	#curses.echo()
	stdscr.addstr(0,0,promt)
	stdscr.refresh()
	input_str = stdscr.getstr().decode('utf-8')
	#curses.noecho()
	return input_str
'''

# create a logging handler, set the max size to 1MB and have 5 backups
'''
handler = RotatingFileHandler(
    filename='depressionland.log',
    maxBytes=1024*1024,  # 1MB
    backupCount=5,
    encoding='utf-8'
)

# set logging format
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# get logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
'''
#logging sys
#limit size
file_path = 'depressionland.log'  
file_size = os.path.getsize(file_path)/(1024*1024)
if file_size <= 1:
	file_mode = 'a'
else:
	file_mode = 'w'
#set up logger
logging.basicConfig(
	filename = 'depressionland.log',
	filemode = file_mode,
	format = '%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
	level = logging.INFO,
	force = True
)

def main(stdscr,info_mem):
	logging.info('main entrance')
	#############ini curses settings###################
	curses.curs_set(0)  #hide the mouse
	stdscr.nodelay(1)  #no waiting for input
	stdscr.timeout(100)  #renew every 100ms

	################bg settings#####################
	curses.start_color()  # enable color
	# set color pair
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # blue bg, white text
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)  # red bg, white text
	curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_RED)  # blue bg, red text
	# set bg color
	stdscr.bkgd(' ', curses.color_pair(1))

	############init the data#################
	if not info_mem:
		#player login and read data
		login_state,name,level,skip = login_manager.login_manager(stdscr)
		if not login_state:
			return False,None
		level = int(level)
	else:
		name = info_mem[0]
		level = info_mem[1]
		skip = True
	#backpack
	beacon_num = abs(10-level*3)+1
	#map
	'''
	max_y,max_x = stdscr.getmaxyx()
	if level <= 2:
		height = (max_y//10)*level
		width = (max_x//25)*level
	elif level >= 3:
		height = 6
		width = 9
	'''
	if level <= 2:
		height = 2*(level+1)+1
		width = 3*(level+1)+2
	else:
		height = 7
		width = 12

	max_y, max_x = stdscr.getmaxyx()
	if max_y < 4*height+1 or max_x < 4*width+1:
		logging.error('Screen too small!')
		stdscr.nodelay(0)
		stdscr.addstr(0,0,'Screen too small! Please enlarge the terminal window and restart the game!')
		stdscr.refresh()
		time.sleep(3)
		return False,None

	#instantiation and init
	game_map = GameMap.GameMap(level,width,height)
	backpack = Backpack.Backpack(beacon_num, game_map.get_missions())
	player = Player.Player(name,[game_map.get_width()//2-1,game_map.get_height()//2-1],backpack,game_map)

	#sight_range
	sight_range = [(4*height+1)//2-1,(4*height+1)//2-1]

	logging.info([name,level,height,width,beacon_num])

	#global demo mode
	show_global_map = False

	#message to be displayed
	message = None
	family_related_msg = ['When to have children makes you anxious, fearing you might miss the optimal time.',
							'You worry about the impact of having children on your career.',
							'You strive to find the right boundary between career and family.',
							'You are worried about the family issues.',
							'The division of housework in your family is not balanced.',
							'You do not like the chores you have to do.',
							'There is little privacy in your relationship.']
	work_related_msg = ['You are feeling the pressure of career advancement.',
						'Gender discrimination in the workplace leaves you feeling powerless.',
						'You feel lonely, struggling to maintain a social life amidst your hectic schedule.',
						'You are worried about realizing your potential and ambitions at work.',
						'Your work to prove yourself in a male-dominated environment is tedious.',
						'You are overwhelmed by the responsibilities and tight deadlines.']

	#change times
	change_times = 0

	#max time allowed
	if level < 3:
		max_time = 300//(level)
	else:
		max_time = 137
	#max_time = 5

	#start animation
	if not skip:
		display_start_scene.display_start_scene(stdscr)
	else:
		display_start_scene_nofirst.display_start_scene_nofirst(stdscr)

	#timing starts
	time_start = time.time()
	global_timer_start = time.time()
	display_timer_start = time.time()

	###########main loop###########
	while len(player.backpack.get_missions()) != 0:
		if not show_global_map:
			# get the screen size
			max_y, max_x = stdscr.getmaxyx()
			
			# define the title
			title = "Depressionland"
			line_length = max_x - 2  # 两侧各留一个空格
			line = '-' * ((line_length - len(title)) // 2)
			title_line = f'{line} {title} {line}'

			if level == 1:
				chapter_str = 'Work'
			elif level == 2:
				chapter_str = 'Family and relationships'
			else:
				chapter_str = 'Everything'

			# display title and player status
			stdscr.clear()
			stdscr.addstr(0, 0, title_line, curses.color_pair(2) | curses.A_BOLD)
			stdscr.addstr(1,0,f'Chapter {level}: {chapter_str}')
			stdscr.addstr(2, 0, f'Current Beacons: {player.backpack.get_beacon_num()} ; Targets to be placed: {[mission[0] for mission in player.backpack.get_missions()]}' + '\n')
			stdscr.addstr(3, 0, f'Hints: 1. Use arrow keys to move 2. Press "m" to view the whole map 3. Press "t" to place the target 4. Press "b" to place or collect the beacon 5.Press "x" to exit' + '\n')
			display_timer_end = time.time()
			display_time = display_timer_end - display_timer_start
			stdscr.addstr(5, 0, f'You have {int(max_time - display_time)} seconds left.')
			stdscr.refresh()

			#show player view
			game_map.visualize_player_view(sight_range,player.get_pos(),stdscr)

			#if any message, display it
			if message:
				stdscr.addstr(6,0,f'The Master of Depressionland has a message for {name}:')
				stdscr.addstr(7,0,message)
				logging.info(message)
			
			stdscr.refresh()

		#listen to key board
		key = stdscr.getch()
		#logging.info(['key',key])

		#press R to restart
		if key == ord('r'):
			logging.info('key R')
			return True,[name,level]

		#press x to log out
		if key == ord('x'):
			logging.info('key X')
			break

		#press m again to close gobal map
		if show_global_map and key != ord('m'):
			continue

		#press m to show global map
		if key == ord('m'):
			logging.info('key M')
			if not show_global_map:
				stdscr.clear()
				stdscr.addstr(0, 0, f"Press 'm' again to hide the map.")
				game_map.visualize_global_map(stdscr)
				stdscr.refresh()
				show_global_map = True
			else:
				#stdscr.clear()
				show_global_map = False
				continue

		#move character
		elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
			#logging.debug('direction')
			if key == curses.KEY_UP:
				#logging.debug('up')
				player.move(0,-1)
			elif key == curses.KEY_DOWN:
				player.move(0,1)
			elif key == curses.KEY_LEFT:
				player.move(-1,0)
			elif key == curses.KEY_RIGHT:
				player.move(1,0)

		#pick up or place the beacon
		elif key == ord('b'):
			logging.info('key B')
			modify_mode = player.set_beacon()
			if modify_mode == -1:
				logging.info('Not enough beacons!!!')
				message = "Not enough beacons!!!"
				#stdscr.refresh()
			elif modify_mode == 0:
				logging.info('Do not put the beacon on the mission!!!')
				message = "Do not put the beacon on the mission!!!"
				#stdscr.refresh()
			elif modify_mode == 1:
				game_map.add_items([[0,'B',player.get_pos()[0],player.get_pos()[1]]])
				logging.info('added beacon')
				message = None
			elif modify_mode == 2:
				game_map.delete_items([[0,'B',player.get_pos()[0],player.get_pos()[1]]])
				logging.info('deleted beacon')
				message = None
			
				

		#put down the mission
		elif key == ord('t'):
			logging.info('key T')
			modify_mode = player.set_missions()
			if modify_mode:
				if level == 1:
					message = random.choice(work_related_msg)
				elif level == 2:
					message = random.choice(family_related_msg)
				elif level == 3:
					all_related_msg = family_related_msg + work_related_msg
					message = random.choice(all_related_msg)
			'''
			if not player.set_missions():
				stdscr.addstr(sight_range[1]+5, 0, f"WHAT?! Why would anyone place sth wrong HERE?!")
				stdscr.refresh()
			'''
		'''
		#显示全局map
		elif key == ord('m'):
			stdscr.clear()
			global_map.visualize_map(global_map_l2d)
			stdscr.addstr(width, 0, f"Press 'm' again to hide the map.")
			stdscr.refresh()
			key = stdscr.getch()
			if key == 'm':
				local_map.visualize_player_view(stdscr,local_map_l2d,player_location_l1d)
		'''
		#timer renew, modify the maze
		time_end = time.time()

		#failure judgement
		failure = False
		if time_end-global_timer_start >= max_time:
			failure = True
			logging.info('failed')
			break

		#modify map
		modify_time = 60//level if 60//level >= 10 else 10
		#modify_time = 0.5
		if time_end - time_start >= modify_time:
			#stdscr.clear()
			#stdscr.addstr(, 0, f"The maze starts to change...")
			#time.sleep(2)
			modify_stat = game_map.modify_roads(player.get_pos(),sight_range)
			if modify_stat:
				change_times += 1
				message = f'The maze starts to change for the {change_times}th time...'
			time_start = time.time()
			stdscr.refresh()

	#failure
	if failure:
		stdscr.clear()
		logging.info('time is up')
		#level = int(''.join(level))
		stdscr.refresh()
		display_end_scene_fail.display_end_scene_fail(stdscr)
		return False,None
	
	#next level
	end = False
	if len(player.backpack.get_missions()) == 0:
		stdscr.clear()
		stdscr.refresh()
		if level == 1:
			text1 = """
			You have overcome the pressures in the workplace, 
			"""
			display_algo.gradual_appear_words(text = text1,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(2)
			text2 = """
			recalling the confident and ambitious self you were when you first graduated. 
			"""
			display_algo.gradual_appear_words(text = text2,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(2)
			text3 = """
			You believe that you can certainly perform even better in your job.
			"""
			display_algo.gradual_appear_words(text = text3,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(2)
			text4 = 'But there is more to face...'
			display_algo.gradual_appear_words(text = text4,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(1)
		elif level == 2:
			text1 = """
			Actually, the family issues aren't that bad, right?  
			"""
			display_algo.gradual_appear_words(text = text1,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(2)
			text2 = """
			After all, you have a loving husband, and no matter what problems arise, you can face them together.
			"""
			display_algo.gradual_appear_words(text = text2,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(2)
			text3 = """
			You really don't have to shoulder so much on your own; you both will surely find a way!
			"""
			display_algo.gradual_appear_words(text = text3,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(2)
			text4 = 'But there is more to face...'
			display_algo.gradual_appear_words(text = text4,speed=0.01,acceleration=0,stdscr=stdscr)
			time.sleep(1)
		file_name = './level.txt'
		user_manager.update_data(name,level+1)
		stdscr.refresh()
		if level+1 <= 3:
			return True,[name,level+1]
		else:
			end = True

	#end animation
	if end:
		stdscr.clear()
		stdscr.refresh()
		display_end_scene_success.display_end_scene_success(stdscr)
		stdscr.refresh()
		return False,None

	logging.info('main end')
	#logging.shutdown()
	return False,None

if __name__ == "__main__":
    def wrapper(stdscr):
        info_mem = []
        while True:
            return_info = main(stdscr,info_mem)
            if not return_info[0]:
                break
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, "(Re)Starting")
                info_mem = return_info[1]
                stdscr.refresh()
                time.sleep(2)
    
    curses.wrapper(wrapper)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

'''
##########初始化###########
    #初始化map
   	height = 100
   	width = 100

   	file_name = './level.txt'#!!!!!
    with open(file_name) as file_obj:
    	level = file_obj.readline()
    level = int(''.join(level))

    game_map.init(level,height,width)

	#初始化backpack
	beacon_num = 10-level*2
	backpack.init(beacon_num,game_map.get_missions())

    #初始化player
    name = input('Name: ') #!!!
    player.init(level,name,backpack,game_map)
	game_map.player = player
'''

#wzl

