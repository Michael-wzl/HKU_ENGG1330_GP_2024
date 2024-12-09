import random

def Recursive_division(r1, r2, c1, c2, M):
    if r1 < r2 and c1 < c2:
        rm = random.randint(r1, r2-1)
        cm = random.randint(c1, c2-1)
        cd1 = random.randint(c1, cm)
        cd2 = random.randint(cm+1, c2)
        rd1 = random.randint(r1, rm)
        rd2 = random.randint(rm+1, r2)
        d = random.randint(1, 4)
        if d == 1:
            M[rd2][cm][2] = 1
            M[rd2][cm+1][0] = 1
            M[rm][cd1][3] = 1
            M[rm+1][cd1][1] = 1
            M[rm][cd2][3] = 1
            M[rm+1][cd2][1] = 1
        elif d == 2:
            M[rd1][cm][2] = 1
            M[rd1][cm+1][0] = 1
            M[rm][cd1][3] = 1
            M[rm+1][cd1][1] = 1
            M[rm][cd2][3] = 1
            M[rm+1][cd2][1] = 1
        elif d == 3:
            M[rd1][cm][2] = 1
            M[rd1][cm+1][0] = 1
            M[rd2][cm][2] = 1
            M[rd2][cm+1][0] = 1
            M[rm][cd2][3] = 1
            M[rm+1][cd2][1] = 1
        elif d == 4:
            M[rd1][cm][2] = 1
            M[rd1][cm+1][0] = 1
            M[rd2][cm][2] = 1
            M[rd2][cm+1][0] = 1
            M[rm][cd1][3] = 1
            M[rm+1][cd1][1] = 1

        Recursive_division(r1, rm, c1, cm, M)
        Recursive_division(r1, rm, cm+1, c2, M)
        Recursive_division(rm+1, r2, cm+1, c2, M)
        Recursive_division(rm+1, r2, c1, cm, M)

    elif r1 < r2:
        rm = random.randint(r1, r2-1)
        M[rm][c1][3] = 1
        M[rm+1][c1][1] = 1
        Recursive_division(r1, rm, c1, c1, M)
        Recursive_division(rm+1, r2, c1, c1, M)
    elif c1 < c2:
        cm = random.randint(c1, c2-1)
        M[r1][cm][2] = 1
        M[r1][cm+1][0] = 1
        Recursive_division(r1, r1, c1, cm, M)
        Recursive_division(r1, r1, cm+1, c2, M)

def recursive_division_map_gen_v2(width, height):
    num_rows = int(width)  # row
    num_cols = int(height)  # col
    r1 = 0
    r2 = num_rows-1
    c1 = 0
    c2 = num_cols-1

    # ini maze
    M = [[[0, 0, 0, 0, 0] for _ in range(num_cols)] for _ in range(num_rows)]

    Recursive_division(r1, r2, c1, c2, M)

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
