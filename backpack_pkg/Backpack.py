import logging

logger = logging.getLogger(__name__)

class Backpack():
	def __init__(self,beacon_int = 0,missions_l2 = None):
		self.beacon_int = beacon_int
		self.missions_l2 = missions_l2 if missions_l2 is not None else []
		logging.info('Backpack init')
	'''
	def init(self,beacon_num,mission):
		self.beacon_int = beacon_num
		self.missions_l2 = mission
	'''

	def put_in_beacon(self):
		#beacon ++
		logging.info('beacon++')
		self.beacon_int+=1

	def take_out_beacon(self):
		#beacon --
		logging.info('beacon--')
		self.beacon_int-=1

	def get_beacon_num(self):
		#logging.info(self.beacon_int)
		return self.beacon_int

	def missions_out(self,man_l1):
		#man = ['r','target_mission'] （’r‘表示remove，现阶段只会有r传入，但是这个接口保留了程序可扩展性）
		#mission out
		#logging.info(man_l1)
		for mission in self.missions_l2:
			if mission[0] == man_l1[1]:
				logging.info(man_l1)
				self.missions_l2.remove(mission)
				break
		
	def get_missions(self):
		#logging.info(self.missions_l2)
		return self.missions_l2

	def get_mission_pos(self):
		mission_pos = []
		for mission in self.missions_l2:
			mission_pos.append(mission[1:])
		#logging.info(mission_pos)
		return mission_pos

	#Matt
