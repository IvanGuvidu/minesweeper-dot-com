from flask import current_app, jsonify, request, render_template, session, redirect, url_for
from .board.board_generation import generate_mines
from .board.board_reveal import reveal_cells
from .games import tic_tac_toe as ttt

@current_app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('home.html')

@current_app.route('/minesweeper')
def minesweeper():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('index.html', n=10, m=10)

@current_app.route('/snake')
def snake():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('snake.html')

@current_app.route('/tic-tac-toe')
def tic_tac_toe():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template('tic_tac_toe.html')

@current_app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        session['logged_in'] = True
        session['username'] = username or 'Player'

        session['board'] = None
        session['first_move'] = True
        session['revealed_cells'] = []

        return redirect(url_for('home'))

    return render_template('login.html')

@current_app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

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

        total_cells = len(board) * len(board[0])
        total_mines = sum(1 for row in board for cell in row if cell == 'M')
        safe_cells = total_cells - total_mines

        victory = len(revealed_cells) >= safe_cells

        return jsonify({'mine': False, 'adjacentMines': cell_val, 'revealed': revealed_json, 'victory': victory})

@current_app.route('/tic-tac-toe/move', methods=['POST'])
def tic_tac_toe_move():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.get_json()
    row = data['row']
    col = data['col']
    
    if 'ttt_board' not in session:
        session['ttt_board'] = ttt.create_board()
        session['ttt_current_player'] = 'X'
    
    board = session['ttt_board']
    current_player = session['ttt_current_player']
    
    success, message = ttt.make_move(board, row, col, current_player)
    
    if not success:
        return jsonify({'success': False, 'message': message})
    
    winner = ttt.check_winner(board)
    
    # Update session
    session['ttt_board'] = board
    
    if winner:
        game_over = True
        next_player = current_player
    else:
        next_player = ttt.get_next_player(current_player)
        session['ttt_current_player'] = next_player
        game_over = False
    
    return jsonify({
        'success': True,
        'board': board,
        'winner': winner,
        'gameOver': game_over,
        'nextPlayer': next_player
    })

@current_app.route('/tic-tac-toe/restart', methods=['POST'])
def tic_tac_toe_restart():
    if not session.get('logged_in'):
        return jsonify({'error': 'Not logged in'}), 401
    
    session['ttt_board'] = ttt.create_board()
    session['ttt_current_player'] = 'X'
    
    return jsonify({'success': True, 'currentPlayer': 'X'})