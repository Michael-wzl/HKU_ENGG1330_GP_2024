import sys
import os

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import curses
import random
import logging
import copy

logger = logging.getLogger(__name__)
#import Player
from map_gen_pkg import map_generator
from map_gen_pkg import mission_distributor
from map_gen_pkg.gen_algo_pkg import prim_map_gen_v2
import visible

class GameMap():
	def __init__(self,level = 1,width_int = 0,height_int = 0,roads_l2 = 0,missions_l2 = None,items_l2 = None):
		self.level = level
		self.width_int = 4*width_int+1
		self.height_int = 4*height_int+1
		self.roads_l2 = roads_l2 if roads_l2 is not None else []
		self.missions_l2 = missions_l2 if missions_l2 is not None else []
		self.items_l2 = items_l2 if items_l2 is not None else []
		#self.player = player if player is not None else Player.Player()

		#width = 100, height = 100
		#roads_l2 = [['#','#','#',...],['#',' ','@',...],...]
		#missions_l2 = [['mission_name',x,y],[],...]
		#items_l2 = [['0','B',x,y],['0','B',24,14],...]

		#init roads
		self.roads_l2 = map_generator.map_generator(self.level,(self.width_int-1)//4,(self.height_int-1)//4)

		#init missions
		self.missions_l2 = mission_distributor.mission_distributor(self.level,self.width_int,self.height_int,self.roads_l2)
		#wzl
		logging.info('GameMap init')
		
	def get_roads(self):
		return self.roads_l2
		
	def get_width(self):
		return self.width_int

	def get_height(self):
		return self.height_int

	def modify_roads(self, player_pos, sight_range):
		# Calculate the boundaries of the player's visible area
		player_x, player_y = player_pos
		view_width, view_height = sight_range
		view_start_x = max(0, player_x - view_width // 2)
		view_end_x = min(self.width_int, player_x + view_width // 2)
		view_start_y = max(0, player_y - view_height // 2)
		view_end_y = min(self.height_int, player_y + view_height // 2)

		# Define the size of the area to be modified
		modify_width = self.width_int // 8
		modify_height = self.height_int // 8

		max_attempts = 50
		for attempt in range(max_attempts):
			# Try to find a modification area that doesn't overlap with the player's visible area
			start_x = random.randint(2, self.width_int - modify_width - 8)
			start_y = random.randint(2, self.height_int - modify_height - 8)
			end_x = start_x + modify_width
			end_y = start_y + modify_height

			# Generate a new map part using prim_map_gen_v2
			new_part = prim_map_gen_v2.prim_map_gen_v2(modify_width, modify_height)

			# Remove the border of new_part
			new_part_without_border = []
			for i in range(1, len(new_part) - 1):
				row = []
				for j in range(1, len(new_part[i]) - 1):
					row.append(new_part[i][j])
				new_part_without_border.append(row)

			
			#logging.debug([player_pos,start_x,start_y,self.width_int,self.height_int,len(new_part_without_border[0]),len(new_part_without_border)])
			'''
			if (end_x <= view_start_x or start_x >= view_end_x or end_y <= view_start_y or start_y >= view_end_y):
				logging.warning('collides with player pos')
				continue  # Area overlaps, try again
			if start_x+len(new_part_without_border[0]) <= player_x and end_x+len(new_part_without_border[0]) >= player_x and start_y+len(new_part_without_border) and end_y+len(new_part_without_border) <= player_y:
				if new_part_without_border[player_x-start_x][player_y-start_y] == '#':
					logging.warning('collides with player pos')
					continue  # Area overlaps, try again
			'''

			# Create a temporary map to check for enclosed areas
			temp_map = copy.deepcopy(self.roads_l2)

			# Replace the original map part with the newly generated one
			for i in range(len(new_part_without_border)):
				for j in range(len(new_part_without_border[0])):
					if start_x + i < self.width_int and start_y + j < self.height_int:
						temp_map[start_x + i][start_y + j] = new_part_without_border[i][j]

			# Check if the newly generated part affects mission positions
			missions_affected = False
			for mission in self.missions_l2:
				if temp_map[mission[1]][mission[2]] == '#':
					#logging.debug('bug')
					missions_affected = True
					break

			if missions_affected:
				logging.warning('missions_affected')
				continue  # Mission affected, try again

			#check if the newly generated part affects item positions
			item_affected = False
			for item in self.items_l2:
				if temp_map[item[2]][item[3]] == '#':
					item_affected = True
					break
			
			if item_affected:
				logging.warning('item affected')
				continue

			# Check if it collides with player pos
			if temp_map[player_x][player_y] == '#':
				logging.warning('collide with player pos')
				continue

			# Check for enclosed areas
			if self.__has_enclosed_areas(temp_map):
				logging.warning('has_enclosed_areas')
				continue

			#if all well, use the new map
			self.roads_l2 = copy.deepcopy(temp_map)
			logging.info(f"Map modified, modification area: ({start_x}, {start_y}) to ({end_x}, {end_y})")

			#if there are ever holes in the outer wall, fill them
			for i in range(self.width_int):
				if self.roads_l2[i][0] == ' ':
					logging.warning('holes')
					self.roads_l2[i][0] = '#'
				if self.roads_l2[i][self.height_int-1] == ' ':
					logging.warning('holes')
					self.roads_l2[i][self.height_int-1] = '#'

			return True

		logging.warning(f"Unable to generate a suitable map modification after {max_attempts} attempts")
		return False

	def __has_enclosed_areas(self, map):
		# privately owned func, checking closed spaces
		visited = []
		for i in range(self.width_int):
			row = []
			for j in range(self.height_int):
				row.append(False)
			visited.append(row)
		
		def flood_fill(x, y):
			if (x < 0 or x >= self.width_int or y < 0 or y >= self.height_int or visited[x][y] or map[x][y] == '#'):
				return
			visited[x][y] = True
			flood_fill(x+1, y)
			flood_fill(x-1, y)
			flood_fill(x, y+1)
			flood_fill(x, y-1)

		# Start flood fill from a known empty space
		start_x, start_y = None, None
		for i in range(self.height_int):
			for j in range(self.width_int):
				if map[j][i] == ' ':
					start_x, start_y = j, i
					break
			if start_x is not None:
				break

		if start_x is not None:
			flood_fill(start_x, start_y)

		# Check if all empty spaces are visited
		for i in range(self.height_int):
			for j in range(self.width_int):
				if map[j][i] == ' ' and not visited[j][i]:
					return True  # Found an enclosed area
		return False

	def get_missions(self):
		return self.missions_l2

	def get_mission_pos(self):
		mission_pos = []
		for mission in self.missions_l2:
			mission_pos.append(mission[1:])
		return mission_pos

	def delete_missions(self,target_mission):
		if target_mission in self.missions_l2:
			self.missions_l2.remove(target_mission)
		else:
			logging.warning('Cannot find the target mission in the mission list in the game_map module!!!')
			
	def get_items(self):
		return self.items_l2

	def add_items(self,items):
		for item in items:
			self.items_l2.append(item)
		#self.items_l2.extend(items)

	def delete_items(self,items):
		for item in items:
			if item in self.items_l2:
				self.items_l2.remove(item)

	def visualize_global_map(self,stdscr):
		tmp_map = copy.deepcopy(self.roads_l2)
		for mission in self.missions_l2:
			tmp_map[mission[1]][mission[2]] = mission[0]
		
		for i in range(self.height_int):
			line = ''
			for j in range(self.width_int):
				char = tmp_map[j][i]
				if char == '#':
					line += '##'
				else:
					line += char + ' '  # add a space after non-wall
			stdscr.addstr(i+1, 0, line)
		
		stdscr.refresh()

	def visualize_player_view(self, sight_range, player_pos, stdscr):
		player_x, player_y = player_pos

		# cal the height and width of player view
		view_width = sight_range[0] * 2  # every char takes two spaces for beaty
		view_height = sight_range[1]

		# ini sight range
		x_start = max(0, player_x - view_width // 4)  
		x_end = min(self.width_int, player_x + view_width // 4)
		y_start = max(0, player_y - view_height // 2)
		y_end = min(self.height_int, player_y + view_height // 2)

		# find walls
		walls = [[row, col] for row in range(self.width_int) for col in range(self.height_int) if self.roads_l2[row][col] == '#']

		tmp_map = copy.deepcopy(self.roads_l2)
		# include items, missions and the player in the view
		for mission in self.missions_l2:
			if tmp_map[mission[1]][mission[2]] == mission[0]:
				logging.warning('mission in walls! when visualizing player view')
				self.roads_l2[mission[1]][mission[2]] = ' '
			tmp_map[mission[1]][mission[2]] = mission[0]
		for item in self.items_l2:
			tmp_map[item[2]][item[3]] = item[1]
		tmp_map[player_x][player_y] = '@'

		# get screen size
		screen_height, screen_width = stdscr.getmaxyx()
		
		# cal size of the sight range
		view_actual_width = (x_end - x_start) * 2 + 2  # +2 for the frame
		view_actual_height = y_end - y_start + 2  # +2 for the frame
		
		# put the sight in the middle of the scr
		start_y = (screen_height - view_actual_height) // 2
		start_x = (screen_width - view_actual_width) // 2

		# draw teh frame and the content
		for i in range(view_actual_height):
			line = ''
			for j in range(view_actual_width // 2):  
				if i == 0 or i == view_actual_height - 1:
					char = '--'
				elif j == 0 or j == view_actual_width // 2 - 1:
					char = '||'
				else:
					map_x = x_start + (j - 1)
					map_y = y_start + (i - 1)
					if 0 <= map_x < self.width_int and 0 <= map_y < self.height_int:
						if visible.visible(player_pos, [map_x, map_y], walls):
							char = tmp_map[map_x][map_y]
							if char == '#':
								char = '##'  
							else:
								char += ' ' 
						else:
							char = '..'
					else:
						char = '  '
				line += char
			
			stdscr.addstr(start_y + i, start_x, line, curses.color_pair(1))

		stdscr.refresh()

#wzl & zwq
