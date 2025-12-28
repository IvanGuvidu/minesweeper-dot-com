import itertools
from .probability_engine import ProbabilityEngine

class MinesweeperSolver:
    def __init__ (self, board):
        self.raw_board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.probabs = []
    
    def get_best_move(self):
        simple_move = self.find_simple_move()
        if simple_move:
            return simple_move
        return self.calc_probabilities()
    
    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    neighbors.append(((nx, ny), self.raw_board[nx][ny]))
        return neighbors
    
    def find_simple_move(self):
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.raw_board[i][j]

                if str(val) in ['.', 'F']:
                    continue

                val_num = int(val)
                neighbors = self.get_neighbors(i, j)
                hidden = [vecin for vecin in neighbors if vecin[1] == '.']
                flags = [vecin for vecin in neighbors if vecin[1] == 'F']

                if val_num == len(flags) + len(hidden) and len(hidden) > 0:
                    target = hidden[0][0]
                    return {
                        'x': target[0],
                        'y': target[1],
                        'action': 'flag',
                        'probability': 1.0
                    }
                
                if val_num == len(flags) and len(hidden) > 0:
                    target = hidden[0][0]
                    return {
                        'x': target[0],
                        'y': target[1],
                        'action': 'click',
                        'probability': 0.0
                    }
        return None
    
    def calc_probabilities(self):
        engine = ProbabilityEngine(self.raw_board)
        probabs = engine.calculate()

        if not probabs:
            return self.guess_random()
        
        best_cell = min(probabs, key=probabs.get)
        min_prob = probabs[best_cell]

        if min_prob == 1.0:
            return {
                'x': best_cell[0],
                'y': best_cell[1],
                'action': 'flag',
                'probability': 1.0
            }
        
        return {
            'x': best_cell[0],
            'y': best_cell[1],
            'action': 'click',
            'probability': min_prob
        }
    
    def guess_random(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.raw_board[i][j] == '.':
                    return {
                        'x': i,
                        'y': j,
                        'action': 'click',
                        'probability': -1
                    }
        return None
