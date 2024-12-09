import logging

def bresenham(x1,y1,x2,y2):			#Bresenham algo
		points=[]						#store all points on the line
		x_distance = abs(x1-x2)			#difference in distance for x and y
		y_distance = abs(y1-y2)
		x_direction = 1 if x1<x2 else -1#if start < end, x += 1
		y_direction = 1 if y1<y2 else -1
		error = x_distance - y_distance	#error for deciding the next point
		while True:
			points.append([x1,y1])
			if x1 == x2 and y1 == y2:
				break
			error_now = error * 2
			if error_now > -y_distance:
				error -= y_distance
				x1 += x_direction
			if error_now < x_distance:
				error += x_distance
				y1 += y_direction
		return points

def visible(player_pos,target_pos,walls):#check visibility
		#player_pos = self.player.get_pos()
		target_line = bresenham(player_pos[0], player_pos[1], target_pos[0], target_pos[1])
		#logging.debug(target_line)
		#logging.debug(player_pos)
		#logging.debug(target_pos)
		for point in target_line[:-1]: #check all points on the line
			if point in walls:
				#logging.debug(f'point {point} is in walls')
				return False#if blocked，return False
		return True

#zwq
