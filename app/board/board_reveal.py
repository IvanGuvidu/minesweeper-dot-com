import collections
import random

def reveal_cells(board, row, col):
	rows, cols = len(board), len(board[0])
	revealed = set()
	queue = collections.deque()
	queue.append((row, col))
	while queue:
		x, y = queue.popleft()
		if (x, y) in revealed:
			continue
		revealed.add((x, y))
		if board[x][y] == 0:
			for dx in [-1, 0, 1]:
				for dy in [-1, 0, 1]:
					nx, ny = x + dx, y + dy
					if 0 <= nx < rows and 0 <= ny < cols:
						if (nx, ny) not in revealed and board[nx][ny] != 'M':
							queue.append((nx, ny))
	return revealed

def check_victory(board, revealed_cells):
        total_cells = len(board) * len(board[0])
        total_mines = sum(1 for row in board for cell in row if cell == 'M')
        safe_cells = total_cells - total_mines
        return len(revealed_cells) >= safe_cells

def reveal_cell_hint (board, revealed):
    rows = len(board)
    cols = len(board[0])
    
    target = 0
    while(1):
        s = set()
        for i in range(rows):
            for j in range(cols):
                if board[i][j] != target:
                    continue
                if (i, j) in revealed:
                    continue
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) in revealed:
                            s.add((i, j))
        if len(s) > 0:
            return random.choice(list(s))
        target += 1
        if target > 8:
            break
    return None

def assistant_hint(board, revealed):
    pass
