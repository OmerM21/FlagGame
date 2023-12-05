from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os
import json
from static.session_user import User, FLAGS_DICT, SCOREBOARD_PATH

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()

with app.app_context():
    countries = list(FLAGS_DICT.values())

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        if 'user' in session:
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
    
@app.route('/countries', methods=['GET'])
def get_countries():
    return jsonify(countries)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")