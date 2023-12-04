from flask import Flask, render_template, request, session, redirect, url_for
import random
import glob
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

current_dir = os.path.dirname(os.path.abspath(__file__))
FLAGS_IMAGES_PATH = os.path.join(current_dir, "static/flags")
FLAGS_DICT_PATH = os.path.join(current_dir, "static/flags.json")
SCOREBOARD_PATH = os.path.join(current_dir, "static/scoreboard.json")

with open(FLAGS_DICT_PATH, "r") as flags_dict_file:
    flags_dict = json.loads(flags_dict_file.read())

FLAGS_DICT = flags_dict
FLAGS_DICT = dict(sorted(FLAGS_DICT.items(), key=lambda item: item[1]))
FLAGS_IMAGES_LIST = [os.path.basename(file) for file in glob.glob(f"{FLAGS_IMAGES_PATH}/*")]
FLAGS_POS_LIST = list(range(254))
random.shuffle(FLAGS_POS_LIST)

class User:
    def __init__(self, username, score=0, answer="Blank", flagcounter=0, flagposlist=FLAGS_POS_LIST, currentflag=None, currentflagfile=None):
        self.username = username
        self.score = score
        self.answer = answer
        self.flagcounter = flagcounter
        self.flagposlist = flagposlist
        if currentflagfile == None:
            self.currentflagfile = FLAGS_IMAGES_LIST[self.flagposlist[self.flagcounter]]
        else:
            self.currentflagfile = currentflagfile
        if currentflag == None:
            self.currentflag = FLAGS_DICT[self.currentflagfile.split('.')[0]]
        else:
            self.currentflag = currentflag

    def to_json(self):
        return {
            "username": self.username,
            "score": self.score,
            "answer": self.answer,
            "flagcounter": self.flagcounter,
            "flagposlist": self.flagposlist,
            "currentflagfile": self.currentflagfile,
            "currentflag": self.currentflag
        }
    
    @classmethod
    def from_json(cls, user_json):
        return cls(
            username = user_json["username"],
            score = user_json["score"],
            answer = user_json["answer"],
            flagcounter = user_json["flagcounter"],
            flagposlist = user_json["flagposlist"],
            currentflag = user_json["currentflag"],
            currentflagfile = user_json["currentflagfile"]
        )

    def first_flag(self):
        self.flagcounter = 0
        self.currentflagfile = FLAGS_IMAGES_LIST[self.flagposlist[self.flagcounter]]
        self.currentflag = FLAGS_DICT[self.currentflagfile.split('.')[0]]
    
    def next_flag(self):
        self.flagcounter += 1
        self.currentflagfile = FLAGS_IMAGES_LIST[self.flagposlist[self.flagcounter]]
        self.currentflag = FLAGS_DICT[self.currentflagfile.split('.')[0]]

    def submit_flag(self, selectedflag):
        if selectedflag == self.currentflag:
            self.score += 50
            self.answer = "Correct!"
        else:
            self.score -= 50
            self.answer = f"Wrong!, It Was {self.currentflag}" 
        self.next_flag()

    def new_game(self):
        self.score = 0
        self.answer = "New Game Started!"
        random.shuffle(self.flagposlist)
        self.first_flag()

    def submit_game(self):
        with open(SCOREBOARD_PATH, "r") as scoreboard_file:
            scoreboard = json.loads(scoreboard_file.read())
        if self.username in scoreboard.keys():
            if self.score > scoreboard[self.username]:
                scoreboard[self.username] = self.score
        else:
            scoreboard[self.username] = self.score

        with open(SCOREBOARD_PATH, 'w') as scoreboard_file:
            json.dump(scoreboard, scoreboard_file, indent=4)
        self.new_game()

    def get_user_hs(self):
        with open(SCOREBOARD_PATH, "r") as scoreboard_file:
            scoreboard = json.loads(scoreboard_file.read())
        if self.username in scoreboard.keys():
            return scoreboard[self.username]
        else:
            return 0

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        if 'user' in session:
            if session['user']['flagcounter'] == 253:
                current_user = User.from_json(session['user'])
                current_user.new_game()
                session['user'] = current_user.to_json()
                return redirect(url_for('main'))
            else:
                current_user = User.from_json(session['user'])
                current_hs = current_user.get_user_hs()
                session['user'] = current_user.to_json()
                return render_template("main.html", flag_image=session['user']['currentflagfile'], all_flags=FLAGS_DICT.values(), logged_in_uname=session['user']['username'], score=session['user']['score'], answer=session['user']['answer'], flag_num=session['user']['flagcounter']+1, high_score=current_hs)
        else:
            return redirect(url_for('login'))
        
    if request.method == 'POST':
        if request.form.get('form_type') == 'game_submit':
            current_user = User.from_json(session['user'])
            current_user.submit_game()
            session['user'] = current_user.to_json()
            return redirect(url_for('main'))
            
        if request.form.get('form_type') == 'flag_guess':
            selectedflag = request.form.get('selectedflag')
            current_user = User.from_json(session['user'])
            current_user.submit_flag(selectedflag)
            session['user'] = current_user.to_json()
            return redirect(url_for('main'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        session['user'] = User(request.form.get('username')).to_json()
        return redirect(url_for('main')) 
    
@app.route('/scoreboard')
def scoreboard():
    if 'user' in session:
        with open(SCOREBOARD_PATH, "r") as scoreboard_file:
            scoreboard = json.loads(scoreboard_file.read())
        sortedScoreboard = dict(sorted(scoreboard.items(), key=lambda item: item[1], reverse=True))
        return render_template("scoreboard.html", scoreboard=sortedScoreboard)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)