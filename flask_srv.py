from flask import Flask, render_template, request, session, redirect, url_for
import random
import glob
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

FLAGS_IMAGES_PATH = "C:\\Github Projects\\FlagGame\\static\\flags"
FLAGS_DICT_PATH = "C:\\Github Projects\\FlagGame\\static\\flags.json"
SCOREBOARD_PATH = "C:\\Github Projects\\FlagGame\\static\\scoreboard.json"

with open(FLAGS_DICT_PATH, "r") as flags_dict_file:
    flags_dict = json.loads(flags_dict_file.read())

FLAGS_DICT = flags_dict
FLAGS_DICT = dict(sorted(FLAGS_DICT.items(), key=lambda item: item[1]))
FLAGS_IMAGES_LIST = [os.path.basename(file) for file in glob.glob(f"{FLAGS_IMAGES_PATH}/*")]
random.shuffle(FLAGS_IMAGES_LIST)

TOTAL_SCORE = 0
THIS_ANSWER = "Blank"
FLAG_COUNTER = 0

@app.route('/', methods=['GET', 'POST'])
def main():
    global TOTAL_SCORE
    global THIS_ANSWER
    global FLAGS_IMAGES_LIST
    global FLAG_COUNTER

    if FLAG_COUNTER == 253:
        save_score(TOTAL_SCORE)
        return new_game()
        
    if request.method == 'GET':
        if 'username' in session:
            random_flag = FLAGS_IMAGES_LIST[FLAG_COUNTER]
            current_flag_name = FLAGS_DICT[random_flag.split('.')[0]]
            return render_template("main.html", flag_image=random_flag, flag_name=current_flag_name, all_flags=FLAGS_DICT.values(), logged_in_uname=session['username'], score=TOTAL_SCORE, answer=THIS_ANSWER, flag_num=FLAG_COUNTER+1, high_score=get_user_hs())
        else:
            return redirect(url_for('login'))
        
    if request.method == 'POST':
        if request.form.get('form_type') == 'game_submit':
            save_score(int(request.form.get('current_score')))
            return new_game()
            
        if request.form.get('form_type') == 'flag_guess':
            FLAG_COUNTER += 1
            selected_flag = request.form.get('selected_flag')
            current_flag = request.form.get('current_flag')
            current_score = int(request.form.get('current_score'))
            if selected_flag == current_flag:
                TOTAL_SCORE = current_score + 50
                THIS_ANSWER = "Correct!"
                return redirect(url_for('main'))
            else:
                THIS_ANSWER = f"Wrong!, It Was {current_flag}"
                return redirect(url_for('main'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return redirect(url_for('main')) 
    
@app.route('/scoreboard')
def scoreboard():
    if 'username' in session:
        with open(SCOREBOARD_PATH, "r") as scoreboard_file:
            scoreboard = json.loads(scoreboard_file.read())
        sortedScoreboard = dict(sorted(scoreboard.items(), key=lambda item: item[1], reverse=True))
        return render_template("scoreboard.html", scoreboard=sortedScoreboard)
    else:
        return redirect(url_for('login'))

def new_game():
    global TOTAL_SCORE
    global THIS_ANSWER
    global FLAGS_IMAGES_LIST
    global FLAG_COUNTER

    TOTAL_SCORE = 0
    THIS_ANSWER = "New Game Started!"
    FLAG_COUNTER = 0
    random.shuffle(FLAGS_IMAGES_LIST)
    return redirect(url_for('main'))

def save_score(current_score):
    with open(SCOREBOARD_PATH, "r") as scoreboard_file:
        scoreboard = json.loads(scoreboard_file.read())
    if session['username'] in scoreboard.keys():
        if current_score > scoreboard[session['username']]:
            scoreboard[session['username']] = current_score
    else:
        scoreboard[session['username']] = current_score

    with open(SCOREBOARD_PATH, 'w') as scoreboard_file:
        json.dump(scoreboard, scoreboard_file, indent=4)

def get_user_hs():
    with open(SCOREBOARD_PATH, "r") as scoreboard_file:
        scoreboard = json.loads(scoreboard_file.read())
    if session['username'] in scoreboard.keys():
        return scoreboard[session['username']]
    else:
        return 0

if __name__ == '__main__':
    app.run(debug=True)