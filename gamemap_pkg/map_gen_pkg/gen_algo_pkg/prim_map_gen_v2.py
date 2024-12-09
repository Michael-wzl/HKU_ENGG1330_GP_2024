import random

def prim_map_gen_v2(width, height):
    num_rows = int(width) 
    num_cols = int(height) 

    # initialize the maze
    M = [[[0, 0, 0, 0, 0] for _ in range(num_cols)] for _ in range(num_rows)]
    maze = [['#'] * (num_cols * 2 + 1) for _ in range(num_rows * 2 + 1)]

    # set the starting pos
    r, c = 0, 0
    history = [(r, c)]  # record the visited pos

    # traverse the maze
    while history:
        r, c = random.choice(history)
        M[r][c][4] = 1  # mark as visited
        history.remove((r, c))
        check = []

        # check four directions
        if c > 0:
            if M[r][c - 1][4] == 1:
                check.append('L')
            elif M[r][c - 1][4] == 0:
                history.append((r, c - 1))
                M[r][c - 1][4] = 2
        if r > 0:
            if M[r - 1][c][4] == 1:
                check.append('U')
            elif M[r - 1][c][4] == 0:
                history.append((r - 1, c))
                M[r - 1][c][4] = 2
        if c < num_cols - 1:
            if M[r][c + 1][4] == 1:
                check.append('R')
            elif M[r][c + 1][4] == 0:
                history.append((r, c + 1))
                M[r][c + 1][4] = 2
        if r < num_rows - 1:
            if M[r + 1][c][4] == 1:
                check.append('D')
            elif M[r + 1][c][4] == 0:
                history.append((r + 1, c))
                M[r + 1][c][4] = 2

        # randomly choose a direction
        if check:
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

    # generate the maze
    for row in range(num_rows):
        for col in range(num_cols):
            cell_data = M[row][col]
            maze[row * 2 + 1][col * 2 + 1] = ' '
            if cell_data[0] == 1:
                maze[row * 2 + 1][col * 2] = ' '
            if cell_data[1] == 1:
                maze[row * 2][col * 2 + 1] = ' '
            if cell_data[2] == 1:
                maze[row * 2 + 1][col * 2 + 2] = ' '
            if cell_data[3] == 1:
                maze[row * 2 + 2][col * 2 + 1] = ' '

    return maze

#wzl
# adapted
