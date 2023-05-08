from flask import Flask, render_template, request, session, jsonify
import os
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "boggle_game"

boggle_game = Boggle()

@app.route('/')
def index():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

@app.route('/check-word')
def check_word():
    word = request.args.get('word', '')
    board = session['board']
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/post-score', methods=['POST'])
def post_score():
    score = request.json.get('score', 0)
    session['plays'] = session.get('plays', 0) + 1
    session['high_score'] = max(session.get('high_score', 0), score)
    return jsonify({'plays': session['plays'], 'high_score': session['high_score']})

if __name__ == '__main__':
    app.run(debug=True)
