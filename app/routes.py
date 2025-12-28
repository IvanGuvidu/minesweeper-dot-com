from flask import current_app, jsonify, request, render_template, session
from .minesweeper.board_generation import generate_mines
from .minesweeper.board_reveal import check_victory, reveal_cells
from .minesweeper.solver import MinesweeperSolver

@current_app.route('/')
def home():
    session.clear()
    return render_template('index.html', n = 10, m = 10)

@current_app.route('/restart', methods=['POST'])
def restart_game():
    session['board'] = None
    session['first_move'] = True
    return jsonify({"success": True})

@current_app.route('/reveal', methods=['POST'])
def reveal():
    data = request.get_json()
    row = data['row']
    col = data['col']
    
    if session.get('first_move', True):
        board = generate_mines(
            rows=10,
            cols=10,
            mines=15,
            first_row=row,
            first_col=col
        )
        session['board'] = board
        session['first_move'] = False
        session['revealed_cells'] = []
    else:
        board = session.get('board')
    
    cell_val = board[row][col]
    if cell_val == 'M':
        return jsonify({'mine': True, 'adjacentMines': 0, 'revealed': [], 'victory': False})
    else:
        revealed = list(reveal_cells(board, row, col))
        revealed_json = [{'row': r, 'col': c, 'value': board[r][c]} for r, c in revealed]

        revealed_cells = set(session.get('revealed_cells', []))
        revealed_cells.update([(r, c) for r, c in revealed])
        session['revealed_cells'] = list(revealed_cells)

        victory = check_victory(board, revealed_cells)

        return jsonify({'mine': False, 'adjacentMines': cell_val, 'revealed': revealed_json, 'victory': victory})

@current_app.route('/hint_cell', methods=['POST'])
def hint_cell():
    board = session.get('board')
    revealed = set(tuple(cell) for cell in session.get('revealed_cells', []))

    solver_board = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[0])):
            if (i, j) in revealed:
                row.append(str(board[i][j]))
            else:
                row.append('.')
        solver_board.append(row)

    solver = MinesweeperSolver(solver_board)
    best_move = solver.get_best_move()

    if best_move:
        x, y = best_move['x'], best_move['y']
        revealed_cells = session.get('revealed_cells', [])
        action = best_move['action']

        if action == 'click' and (x, y) not in revealed:
            revealed_cells.append((x, y))
            session['revealed_cells'] = revealed_cells
        
        if action == 'flag':
            return jsonify({'row': -1, 'col': -1, 'value': -1, 'victory': False})

        victory = check_victory(board, set(revealed_cells))

        return jsonify({'row': x, 'col': y, 'value': board[x][y], 'victory': victory})
    else:
        return jsonify({'row': -1, 'col': -1, 'value': -1, 'victory': False})
