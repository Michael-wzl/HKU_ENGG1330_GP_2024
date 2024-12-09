import random

def recursive_backtracker_map_gen_v2(width, height):
    num_rows = int(width)  # row
    num_cols = int(height)  # col

    # ini maze 
    M = [[[0, 0, 0, 0, 0] for _ in range(num_cols)] for _ in range(num_rows)]

    # set starting pos
    r, c = 0, 0
    history = [(r, c)]  # record the visited pos

    # check four directions
    while history:
        M[r][c][4] = 1  # mark as visited
        check = []

        # check four directions
        if c > 0 and M[r][c-1][4] == 0:
            check.append('L')
        if r > 0 and M[r-1][c][4] == 0:
            check.append('U')
        if c < num_cols-1 and M[r][c+1][4] == 0:
            check.append('R')
        if r < num_rows-1 and M[r+1][c][4] == 0:
            check.append('D')

        if check:  #randomly choose a direction
            history.append([r, c])
            move_direction = random.choice(check)
            if move_direction == 'L':
                M[r][c][0] = 1
                c -= 1
                M[r][c][2] = 1
            elif move_direction == 'U':
                M[r][c][1] = 1
                r -= 1
                M[r][c][3] = 1
            elif move_direction == 'R':
                M[r][c][2] = 1
                c += 1
                M[r][c][0] = 1
            elif move_direction == 'D':
                M[r][c][3] = 1
                r += 1
                M[r][c][1] = 1
        else:  
            r, c = history.pop()

    # generate the maze
    maze = [['#' for _ in range(num_cols * 2 + 1)] for _ in range(num_rows * 2 + 1)]

    for row in range(num_rows):
        for col in range(num_cols):
            cell_data = M[row][col]
            maze[row * 2 + 1][col * 2 + 1] = ' '
            if cell_data[0] == 1:  # left
                maze[row * 2 + 1][col * 2] = ' '
            if cell_data[1] == 1:  # up
                maze[row * 2][col * 2 + 1] = ' '
            if cell_data[2] == 1:  # right
                maze[row * 2 + 1][col * 2 + 2] = ' '
            if cell_data[3] == 1:  # down
                maze[row * 2 + 2][col * 2 + 1] = ' '

    return maze

#wzl
#adapted
