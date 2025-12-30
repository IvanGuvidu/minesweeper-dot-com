"""
Snake game logic module
"""
import random
from typing import List, Tuple, Dict, Optional

def create_game(rows: int = 20, cols: int = 20) -> Dict:
    """
    Create a new snake game state
    
    Returns:
        dict with keys:
            - snake: list of (row, col) tuples representing snake body
            - direction: current direction ('up', 'down', 'left', 'right')
            - food: (row, col) tuple for food position
            - score: current score
            - game_over: boolean
            - rows: board height
            - cols: board width
    """
    # Start snake in the middle
    start_row = rows // 2
    start_col = cols // 2
    
    snake = [(start_row, start_col), (start_row, start_col + 1), (start_row, start_col + 2)]
    direction = 'left'
    
    # Generate initial food
    food = generate_food(snake, rows, cols)
    
    return {
        'snake': snake,
        'direction': direction,
        'food': food,
        'score': 0,
        'game_over': False,
        'rows': rows,
        'cols': cols
    }

def generate_food(snake: List[Tuple[int, int]], rows: int, cols: int) -> Tuple[int, int]:
    """Generate a random food position that doesn't overlap with the snake"""
    snake_set = set(snake)
    attempts = 0
    max_attempts = rows * cols
    
    while attempts < max_attempts:
        food_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
        if food_pos not in snake_set:
            return food_pos
        attempts += 1
    
    # If board is full (shouldn't happen in normal gameplay)
    return (0, 0)

def change_direction(game: Dict, new_direction: str) -> bool:
    """
    Change snake direction, preventing 180-degree turns
    
    Returns:
        True if direction was changed, False if invalid
    """
    current = game['direction']
    
    # Prevent reversing direction
    opposites = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left'
    }
    
    if new_direction in opposites and opposites[new_direction] == current:
        return False
    
    if new_direction in ['up', 'down', 'left', 'right']:
        game['direction'] = new_direction
        return True
    
    return False

def move_snake(game: Dict) -> Dict:
    """
    Move the snake one step in the current direction
    
    Returns:
        Updated game state with move results
    """
    if game['game_over']:
        return game
    
    snake = game['snake']
    direction = game['direction']
    rows = game['rows']
    cols = game['cols']
    
    # Calculate new head position
    head = snake[0]
    
    if direction == 'up':
        new_head = (head[0] - 1, head[1])
    elif direction == 'down':
        new_head = (head[0] + 1, head[1])
    elif direction == 'left':
        new_head = (head[0], head[1] - 1)
    elif direction == 'right':
        new_head = (head[0], head[1] + 1)
    else:
        new_head = head
    
    # Check wall collision
    if new_head[0] < 0 or new_head[0] >= rows or new_head[1] < 0 or new_head[1] >= cols:
        game['game_over'] = True
        return game
    
    # Check self collision
    if new_head in snake:
        game['game_over'] = True
        return game
    
    # Add new head
    snake.insert(0, new_head)
    
    # Check if food was eaten
    if new_head == game['food']:
        game['score'] += 1
        game['food'] = generate_food(snake, rows, cols)
    else:
        # Remove tail if no food eaten
        snake.pop()
    
    game['snake'] = snake
    
    return game

def get_game_state(game: Dict) -> Dict:
    """
    Get a JSON-serializable representation of the game state
    """
    return {
        'snake': game['snake'],
        'food': game['food'],
        'score': game['score'],
        'gameOver': game['game_over'],
        'direction': game['direction']
    }
