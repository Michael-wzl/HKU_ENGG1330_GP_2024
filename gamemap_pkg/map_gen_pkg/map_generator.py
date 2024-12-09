import sys
import os

# add to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from gen_algo_pkg import recursive_division_map_gen_v2
from gen_algo_pkg import recursive_backtracker_map_gen_v2
from gen_algo_pkg import prim_map_gen_v2
import logging

def map_generator(level,width,height):
    #ini maze
    maze = [['']*(height*4+1) for _ in range(width*4+1)]

    #gen four mazes in four directions
    if level == 1:
        #recursive_division_map_gen_v2 straight roads, easy
        maze_L_U = recursive_backtracker_map_gen_v2.recursive_backtracker_map_gen_v2(width,height)
        maze_L_D = recursive_backtracker_map_gen_v2.recursive_backtracker_map_gen_v2(width,height)
        maze_R_U = recursive_backtracker_map_gen_v2.recursive_backtracker_map_gen_v2(width,height)
        maze_R_D = recursive_backtracker_map_gen_v2.recursive_backtracker_map_gen_v2(width,height)
    elif level == 2:
        #recursive_backtracker_map_gen_v2 clear main road, mild
        maze_L_U = recursive_division_map_gen_v2.recursive_division_map_gen_v2(width,height)
        maze_L_D = recursive_division_map_gen_v2.recursive_division_map_gen_v2(width,height)
        maze_R_U = recursive_division_map_gen_v2.recursive_division_map_gen_v2(width,height)
        maze_R_D = recursive_division_map_gen_v2.recursive_division_map_gen_v2(width,height)
    else:
        #prim_map_gen_v2 natural, hard
        maze_L_U = prim_map_gen_v2.prim_map_gen_v2(width,height)
        maze_L_D = prim_map_gen_v2.prim_map_gen_v2(width,height)
        maze_R_U = prim_map_gen_v2.prim_map_gen_v2(width,height)
        maze_R_D = prim_map_gen_v2.prim_map_gen_v2(width,height)

    '''
    logging.debug('maze_L_D')
    logging.debug(maze_L_D)
    logging.debug(maze_L_U)
    logging.debug(maze_R_D)
    logging.debug(maze_R_U)
    logging.debug('114')
    '''
    #prepare the mazes for putting them up

    #remove left frame of right mazes
    maze_R_U.pop(0)
    maze_R_D.pop(0)
    #link l and r
    for col in range(height*2+1):
        if maze_L_U[width*2-1][col] == ' ' and maze_R_U[0][col] == ' ':
            maze_L_U[width*2][col] = ' '
        if maze_L_D[width*2-1][col] == ' ' and maze_R_D[0][col] == ' ':
            maze_L_D[width*2][col] = ' '
    '''
    logging.debug(maze_L_D)
    logging.debug(maze_L_U)
    logging.debug(maze_R_D)
    logging.debug(maze_R_U)
    logging.debug('113')
    '''

    #remove upper frames of lower mazes
    for row in range(width*2+1):
        maze_L_D[row].pop(0)
    for row in range(width*2):
        maze_R_D[row].pop(0)
    #link u and d
    for row in range(width*2+1):
        if maze_L_D[row][0] == ' ' and maze_L_U[row][height*2-1] == ' ':
            maze_L_U[row][height*2] == ' '
    for row in range(width*2):
        if maze_R_D[row][0] == ' ' and maze_R_U[row][height*2-1] == ' ':
            maze_R_U[row][height*2] == ' '
    '''
    logging.debug(maze_L_D)
    logging.debug(maze_L_U)
    logging.debug(maze_R_D)
    logging.debug(maze_R_U)
    logging.debug('115')
    '''
    #put together
    for row in range(2*width+1):
        for col in range(2*height):
            maze[row][col] = maze_L_U[row][col]
            maze[row][col+2*height+1] = maze_L_D[row][col]
        maze[row][2*height] = maze_L_U[row][2*height]

    for row in range(2*width):
        for col in range(2*height):
            maze[row+2*width+1][col] = maze_R_U[row][col]
            maze[row+2*width+1][col+2*height+1] = maze_R_D[row][col]
        maze[row+2*width+1][2*height] = maze_R_U[row][2*height]
    '''
    logging.debug(maze_L_D)
    logging.debug(maze_L_U)
    logging.debug(maze_R_D)
    logging.debug(maze_R_U)
    logging.debug(maze)
    logging.debug('116')
    '''
    #create a sapce in the middle
    for row in range(-1,2,1):
        for col in range(-1,2,1):
            maze[2*width+1+row][2*height+1+col] = ' '

    return maze
'''
maze = map_generator(3,20,20)
for row in range(len(maze)):
    print(''.join(maze[row]),end = '\n')
'''
#wzl
