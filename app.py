from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', n = 10, m = 10)
@app.route('/restart', methods=['POST'])
def restart_game():
    return jsonify({"success": True})

@app.route('/reveal', methods=['POST'])
def reveal():
    data = request.get_json()
    row = data['row']
    col = data['col']
    # For demonstration, let's assume every cell is safe except (0,0)
    if row == 0 and col == 0:
        return jsonify({'mine': True, 'adjacentMines': 0})
    else:
        # Return a random number of adjacent mines (0-8)
        return jsonify({'mine': False, 'adjacentMines': (row + col) % 9})
    
if __name__ == '__main__':
    app.run(debug=True)