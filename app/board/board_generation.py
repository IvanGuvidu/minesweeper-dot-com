import random

def generate_mines(rows = 10, cols = 10, mines = 15, first_row=None, first_col=None):
    mines_positions = set()
    forbidden = set()
    if first_row is not None and first_col is not None:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = first_row + dx, first_col + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    forbidden.add((nx, ny))
    
    while len(mines_positions) < mines:
        i = random.randint(0, rows - 1)
        j = random.randint(0, cols - 1)
        if (i, j) in mines_positions or (i, j) in forbidden:
            continue
        forbidden.add((i, j))
        mines_positions.add((i, j))

    board = [[0 for _ in range(cols)] for _ in range(rows)]
    for x, y in mines_positions:
        board[x][y] = 'M'

    for i in range(rows):
        for j in range(cols):
            if board[i][j] != 'M':
                count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < rows and 0 <= ny < cols:
                            if board[nx][ny] == 'M':
                                count += 1
                board[i][j] = count
    return board
