import random
import threading
from flask import Flask, render_template, request, redirect, url_for, flash

# Kivy graphical requirements
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

# Android hardware thread controls
from android.runnable import run_on_ui_thread
from jnius import autoclass

app = Flask(__name__)
app.secret_key = 'sudoku_arcade_secret_key'

# Base solved matrices to seed our infinite shuffling engine
BASE_BOARDS = {
    6: [
        [1, 2, 3, 4, 5, 6],
        [4, 5, 6, 1, 2, 3],
        [2, 3, 4, 5, 6, 1],
        [5, 6, 1, 2, 3, 4],
        [3, 4, 5, 6, 1, 2],
        [6, 1, 2, 3, 4, 5]
    ],
    9: [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9]
    ]
}

# App Global State Tracker
game_state = {
    'size': 9,
    'block_r': 3,
    'block_c': 3,
    'difficulty': 'easy',
    'board': [],
    'original': [],
    'won': False
}

def generate_procedural_puzzle(size, difficulty):
    base = [row[:] for row in BASE_BOARDS[size]]
    nums = list(range(1, size + 1))
    shuffled_nums = list(range(1, size + 1))
    random.shuffle(shuffled_nums)
    mapping = dict(zip(nums, shuffled_nums))
    
    for r in range(size):
        for c in range(size):
            base[r][c] = mapping[base[r][c]]
            
    mask_rates = {'easy': 0.35, 'medium': 0.55, 'hard': 0.70}
    rate = mask_rates.get(difficulty, 0.4)
    
    play_board = [row[:] for row in base]
    orig_board = [[0]*size for _ in range(size)]
    
    for r in range(size):
        for c in range(size):
            if random.random() > rate:
                orig_board[r][c] = play_board[r][c]
            else:
                play_board[r][c] = 0
                
    return play_board, orig_board

def check_valid_move(bo, num, pos, size, br, bc):
    row, col = pos
    for j in range(size):
        if bo[row][j] == num and col != j:
            return f"There is already a {num} in that row. Keep searching!"
    for i in range(size):
        if bo[i][col] == num and row != i:
            return f"Vertical clash! Another {num} blocks this column."
    box_x = col // bc
    box_y = row // br
    for i in range(box_y * br, box_y * br + br):
        for j in range(box_x * bc, box_x * bc + bc):
            if bo[i][j] == num and (i, j) != pos:
                return f"Sub-grid conflict! That area already claims a {num}."
    return None

def check_win_condition():
    bo = game_state['board']
    sz = game_state['size']
    br = game_state['block_r']
    bc = game_state['block_c']
    for r in range(sz):
        for c in range(sz):
            if bo[r][c] == 0 or check_valid_move(bo, bo[r][c], (r, c), sz, br, bc) is not None:
                return False
    return True

game_state['board'], game_state['original'] = generate_procedural_puzzle(9, 'easy')

@app.route('/')
def index():
    return render_template('index.html', state=game_state)

@app.route('/setup', methods=['POST'])
def setup():
    global game_state
    size = int(request.form.get('size', 9))
    diff = request.form.get('difficulty', 'easy')
    
    game_state['size'] = size
    game_state['difficulty'] = diff
    game_state['block_r'] = 2 if size == 6 else 3
    game_state['block_c'] = 3
    game_state['won'] = False
    
    game_state['board'], game_state['original'] = generate_procedural_puzzle(size, diff)
    return redirect(url_for('index'))

@app.route('/move', methods=['POST'])
def move():
    if game_state['won']:
        return redirect(url_for('index'))
        
    r = int(request.form['row']) - 1
    c = int(request.form['col']) - 1
    num = int(request.form['num'])
    sz = game_state['size']
    
    if 0 <= r < sz and 0 <= c < sz and 1 <= num <= sz:
        if game_state['original'][r][c] == 0:
            old_val = game_state['board'][r][c]
            game_state['board'][r][c] = num
            
            error_msg = check_valid_move(
                game_state['board'], num, (r, c), 
                sz, game_state['block_r'], game_state['block_c']
            )
            
            if error_msg:
                game_state['board'][r][c] = old_val 
                openers = ["Nice try, Einstein! ", "Bold strategy, but no. ", "Sudoku police alert! "]
                flash(random.choice(openers) + error_msg)
            else:
                if check_win_condition():
                    game_state['won'] = True
            
    return redirect(url_for('index'))

@app.route('/next_stage', methods=['POST'])
def next_stage():
    global game_state
    game_state['won'] = False
    game_state['board'], game_state['original'] = generate_procedural_puzzle(
        game_state['size'], game_state['difficulty']
    )
    return redirect(url_for('index'))

# --- Native Android Window Wrapper ---
def start_flask_server():
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)

class SudokuWarriorsApp(App):
    def build(self):
        # Added a 2.0 second delay to give Flask full breathing room to boot up cleanly
        Clock.schedule_once(self.initialize_android_webview, 2.0)
        return Widget()

    # The magic decorator that forces Android to run this inside the primary UI thread safely
    @run_on_ui_thread
    def initialize_android_webview(self, *args):
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setDomStorageEnabled(True)
        webview.setWebViewClient(WebViewClient())
        
        webview.loadUrl('http://127.0.0.1:5000/')
        activity.setContentView(webview)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=start_flask_server)
    flask_thread.daemon = True
    flask_thread.start()
    
    SudokuWarriorsApp().run()
