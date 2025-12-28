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

