import curses
import logging

from backpack_pkg import Backpack
from gamemap_pkg import GameMap

logger = logging.getLogger(__name__)

class Player():
	def __init__(self,name = 'Michael',position = None,backpack = Backpack.Backpack(),game_map = None):
		self.name = name
		self.position = position if position is not None else [0,0]
		self.backpack = backpack if backpack is not None else Backpack.Backpack()
		self.game_map = game_map if game_map is not None else GameMap.GameMap()
		logging.info('Player init')

	'''
	def init(self,level,name,backpack,game_map):
		self.level = level
		self.name = name
		self.backpack = backpack
		self.game_map = game_map
	'''

	def get_name(self):
		return self.name

	def get_pos(self):
		return self.position

	def move(self,delta_x,delta_y):
		#logging.debug('==============')
		#print('114514')
		logging.info([delta_x,delta_y,'move'])
		new_x = self.position[0] + delta_x
		new_y = self.position[1] + delta_y
		
		if 0 <= new_x < self.game_map.get_width() and 0 <= new_y < self.game_map.get_height() and self.game_map.get_roads()[new_x][new_y] != '#':
			self.position = [new_x, new_y]
		#根据传入的xy增量改变player位置

	def set_beacon(self):
		if [0,'B',self.position[0],self.position[1]] in self.game_map.get_items() and self.position not in self.backpack.get_mission_pos():
			#self.game_map.delete_items(['0','B',self.position[0],self.position[1]])
			logging.info('deleted beacon mode')
			self.backpack.put_in_beacon()
			modify_mode = 2
		elif self.position not in self.game_map.get_items() and self.backpack.get_beacon_num() > 0 and self.position not in self.backpack.get_mission_pos() :
			#self.game_map.add_items(['0','B',self.position[0],self.position[1]])
			logging.info('added beacon mode')
			self.backpack.take_out_beacon()
			modify_mode = 1
		elif self.position in self.backpack.get_mission_pos():
			logging.info('wrong place')
			modify_mode = 0
		elif self.backpack.get_beacon_num() <= 0:
			modify_mode = -1
		else:
			logging.warning('Unidentified error when player trying to place or collect the beacon')
			modify_mode = -2
		# 0 for wrong place, 1 for add, 2 for delete, -1 for not enough beacon, -2 for unknown error
		return modify_mode
	
	def set_missions(self):
		missions = self.game_map.get_missions()

		for mission in missions:
			if self.position == mission[1:]:
				self.backpack.missions_out(['r',mission[0]])
				logging.info('mission out')
				self.game_map.delete_items(mission)
				modify_mode = True
			else:
				logging.info('wrong place, mission out failed')
				modify_mode = False
		return modify_mode
		#调用后，判断删除是否合法，如果合法就调用gamemap类里面的delete_items函数，删去对应target，再返回modify_mode = True；传入delete_items函数的数据形式看gamemap里面的init部分的注释
		#不合法就执行现在写的这两行代码

	#wpr,lcz
