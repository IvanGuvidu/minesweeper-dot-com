import itertools
from collections import defaultdict

class ProbabilityEngine:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.variables = set()
        self.constraints = []
    
    def calculate(self):
        self.build_constraints()
        components = self.get_connected_components()
        ans_probab = {}

        for component_constrains in components:
            component_vars = set()
            for c in component_constrains:
                component_vars.update(c['cells'])
            
            probs = self.solve_component(list(component_vars), component_constrains)
            ans_probab.update(probs)
        
        return ans_probab
    
    def get_neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = x + dx
                ny = y + dy
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    neighbors.append(((nx, ny), self.board[nx][ny]))
        
        return neighbors
    
    def build_constraints(self):
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.board[i][j]
                if str(val) in ['.', 'F']:
                    continue

                val_num = int(val)
                neighbors = self.get_neighbors(i, j)
                hidden = [vecin[0] for vecin in neighbors if vecin[1] == '.']
                flags = [vecin[0] for vecin in neighbors if vecin[1] == 'F']

                if hidden:
                    remaining_mines = val_num - len(flags)
                    self.constraints.append({
                        'cells': hidden,
                        'value': remaining_mines,
                    })
                    self.variables.update(hidden)
    
    def get_connected_components(self):
        if not self.constraints:
            return []
        
        var_to_constraints = defaultdict(list)
        for i, const in enumerate(self.constraints):
            for cell in const['cells']:
                var_to_constraints[cell].append(i)
        
        visited_constraints = set()
        components = []

        for i in range(len(self.constraints)):
            if i in visited_constraints:
                continue
            
            queue = [i]
            visited_constraints.add(i)
            current_component = []

            while queue:
                curr = queue.pop(0)
                current_component.append(self.constraints[curr])

                for cell in self.constraints[curr]['cells']:
                    for neighbor_const_idx in var_to_constraints[cell]:
                        if neighbor_const_idx not in visited_constraints:
                            visited_constraints.add(neighbor_const_idx)
                            queue.append(neighbor_const_idx)
            components.append(current_component)
        
        return components
    
    def solve_component(self, variables, constraints):
        solutions = []

        def backtrack(index, assignment):
            for const in constraints:
                sum = 0
                assigned_count = 0
                for cell in const['cells']:
                    if cell in assignment:
                        sum += assignment[cell]
                        assigned_count += 1
                
                if sum > const['value']:
                    return
                
                unassigned_count = len(const['cells']) - assigned_count
                if sum + unassigned_count < const['value']:
                    return
                
            if index == len(variables):
                solutions.append(assignment.copy())
                return
            
            var = variables[index]
            
            assignment[var] = 0
            backtrack(index + 1, assignment)

            assignment[var] = 1
            backtrack(index + 1, assignment)
            del assignment[var]
        
        backtrack(0, {})

        nr_sols = len(solutions)
        if nr_sols == 0:
            return {var: 0.5 for var in variables}
        
        counts = defaultdict(int)
        for sol in solutions:
            for cell, val in sol.items():
                if val == 1:
                    counts[cell] += 1
        
        return {cell: counts[cell] / nr_sols for cell in variables}
