from flask import Flask, render_template, request, session, redirect, url_for
import random
import glob
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

FLAGS_DICT = {
    'af': 'Afghanistan',
    'al': 'Albania',
    'dz': 'Algeria',
    'as': 'American Samoa',
    'ad': 'Andorra',
    'ao': 'Angola',
    'ai': 'Anguilla',
    'aq': 'Antarctica',
    'ag': 'Antigua and Barbuda',
    'ar': 'Argentina',
    'am': 'Armenia',
    'aw': 'Aruba',
    'au': 'Australia',
    'at': 'Austria',
    'az': 'Azerbaijan',
    'bs': 'Bahamas',
    'bh': 'Bahrain',
    'bd': 'Bangladesh',
    'bb': 'Barbados',
    'by': 'Belarus',
    'be': 'Belgium',
    'bz': 'Belize',
    'bj': 'Benin',
    'bm': 'Bermuda',
    'bt': 'Bhutan',
    'bo': 'Bolivia',
    'bq': 'Bonaire, Sint Eustatius, and Saba',
    'ba': 'Bosnia and Herzegovina',
    'bw': 'Botswana',
    'bv': 'Bouvet Island',
    'br': 'Brazil',
    'io': 'British Indian Ocean Territory',
    'bn': 'Brunei',
    'bg': 'Bulgaria',
    'bf': 'Burkina Faso',
    'bi': 'Burundi',
    'cv': 'Cabo Verde',
    'kh': 'Cambodia',
    'cm': 'Cameroon',
    'ca': 'Canada',
    'ky': 'Cayman Islands',
    'cf': 'Central African Republic',
    'td': 'Chad',
    'cl': 'Chile',
    'cn': 'China',
    'cx': 'Christmas Island',
    'cc': 'Cocos (Keeling) Islands',
    'co': 'Colombia',
    'km': 'Comoros',
    'cd': 'Congo (Congo-Kinshasa)',
    'cg': 'Congo (Congo-Brazzaville)',
    'ck': 'Cook Islands',
    'cr': 'Costa Rica',
    'hr': 'Croatia',
    'cu': 'Cuba',
    'cw': 'Curaçao',
    'cy': 'Cyprus',
    'cz': 'Czechia',
    'ci': 'Cote dIvoire',
    'dk': 'Denmark',
    'dj': 'Djibouti',
    'dm': 'Dominica',
    'do': 'Dominican Republic',
    'ec': 'Ecuador',
    'eg': 'Egypt',
    'sv': 'El Salvador',
    'gb-eng': 'England',
    'gq': 'Equatorial Guinea',
    'er': 'Eritrea',
    'ee': 'Estonia',
    'et': 'Ethiopia',
    'fk': 'Falkland Islands (Islas Malvinas)',
    'fo': 'Faroe Islands',
    'fj': 'Fiji',
    'fi': 'Finland',
    'fr': 'France',
    'gf': 'French Guiana',
    'pf': 'French Polynesia',
    'tf': 'French Southern Territories',
    'ga': 'Gabon',
    'gm': 'Gambia',
    'ge': 'Georgia',
    'de': 'Germany',
    'gh': 'Ghana',
    'gi': 'Gibraltar',
    'gr': 'Greece',
    'gl': 'Greenland',
    'gd': 'Grenada',
    'gp': 'Guadeloupe',
    'gu': 'Guam',
    'gt': 'Guatemala',
    'gg': 'Guernsey',
    'gn': 'Guinea',
    'gw': 'Guinea-Bissau',
    'gy': 'Guyana',
    'ht': 'Haiti',
    'hm': 'Heard Island and McDonald Islands',
    'va': 'Vatican City (Holy See)',
    'hn': 'Honduras',
    'hk': 'Hong Kong',
    'hu': 'Hungary',
    'is': 'Iceland',
    'in': 'India',
    'id': 'Indonesia',
    'ir': 'Iran',
    'iq': 'Iraq',
    'ie': 'Ireland',
    'im': 'Isle of Man',
    'il': 'Israel',
    'it': 'Italy',
    'jm': 'Jamaica',
    'jp': 'Japan',
    'je': 'Jersey',
    'jo': 'Jordan',
    'kz': 'Kazakhstan',
    'ke': 'Kenya',
    'ki': 'Kiribati',
    'kw': 'Kuwait',
    'kg': 'Kyrgyzstan',
    'la': 'Laos',
    'lv': 'Latvia',
    'lb': 'Lebanon',
    'ls': 'Lesotho',
    'lr': 'Liberia',
    'ly': 'Libya',
    'li': 'Liechtenstein',
    'lt': 'Lithuania',
    'lu': 'Luxembourg',
    'mo': 'Macao',
    'mg': 'Madagascar',
    'mw': 'Malawi',
    'my': 'Malaysia',
    'mv': 'Maldives',
    'ml': 'Mali',
    'mt': 'Malta',
    'mh': 'Marshall Islands',
    'mq': 'Martinique',
    'mr': 'Mauritania',
    'mu': 'Mauritius',
    'yt': 'Mayotte',
    'mx': 'Mexico',
    'fm': 'Micronesia',
    'md': 'Moldova',
    'mc': 'Monaco',
    'mn': 'Mongolia',
    'me': 'Montenegro',
    'ms': 'Montserrat',
    'ma': 'Morocco',
    'mz': 'Mozambique',
    'mm': 'Myanmar (Burma)',
    'na': 'Namibia',
    'nr': 'Nauru',
    'np': 'Nepal',
    'nl': 'Netherlands',
    'nc': 'New Caledonia',
    'nz': 'New Zealand',
    'ni': 'Nicaragua',
    'ne': 'Niger',
    'ng': 'Nigeria',
    'nu': 'Niue',
    'nf': 'Norfolk Island',
    'gb-nir': 'North Ireland',    
    'kp': 'North Korea',
    'mk': 'North Macedonia',
    'mp': 'Northern Mariana Islands',
    'no': 'Norway',
    'om': 'Oman',
    'pk': 'Pakistan',
    'pw': 'Palau',
    'pa': 'Panama',
    'pg': 'Papua New Guinea',
    'py': 'Paraguay',
    'pe': 'Peru',
    'ph': 'Philippines',
    'pn': 'Pitcairn Islands',
    'pl': 'Poland',
    'pt': 'Portugal',
    'pr': 'Puerto Rico',
    'qa': 'Qatar',
    'ro': 'Romania',
    'ru': 'Russia',
    'rw': 'Rwanda',
    're': 'Réunion',
    'ws': 'Samoa',
    'sm': 'San Marino',
    'sa': 'Saudi Arabia',
    'sn': 'Senegal',
    'rs': 'Serbia',
    'sc': 'Seychelles',
    'sl': 'Sierra Leone',
    'sg': 'Singapore',
    'sx': 'Sint Maarten',
    'sk': 'Slovakia',
    'si': 'Slovenia',
    'sb': 'Solomon Islands',
    'so': 'Somalia',
    'za': 'South Africa',
    'gs': 'South Georgia and South Sandwich Islands',
    'kr': 'South Korea',
    'ss': 'South Sudan',
    'es': 'Spain',
    'lk': 'Sri Lanka',
    'st': 'Sao Tomé and Principe',
    'bl': 'Saint Barthelemy',
    'sh': 'Saint Helena',
    'kn': 'Saint Kitts and Nevis',
    'lc': 'Saint Lucia',
    'mf': 'Saint Martin',
    'pm': 'Saint Pierre and Miquelon',
    'vc': 'Saint Vincent and the Grenadines',
    'gb-sct': 'Scotland',
    'sd': 'Sudan',
    'sr': 'Suriname',
    'sj': 'Svalbard and Jan Mayen',
    'sz': 'Eswatini',
    'se': 'Sweden',
    'ch': 'Switzerland',
    'sy': 'Syria',
    'tw': 'Taiwan',
    'tj': 'Tajikistan',
    'tz': 'Tanzania',
    'th': 'Thailand',
    'tl': 'Timor-Leste',
    'tg': 'Togo',
    'tk': 'Tokelau',
    'to': 'Tonga',
    'tt': 'Trinidad and Tobago',
    'tn': 'Tunisia',
    'tr': 'Turkey',
    'tm': 'Turkmenistan',
    'tc': 'Turks and Caicos Islands',
    'tv': 'Tuvalu',
    'ug': 'Uganda',
    'ua': 'Ukraine',
    'ae': 'United Arab Emirates',
    'gb': 'United Kingdom',
    'us': 'United States',
    'um': 'United States Minor Outlying Islands',
    'uy': 'Uruguay',
    'uz': 'Uzbekistan',
    'vu': 'Vanuatu',
    've': 'Venezuela',
    'vn': 'Vietnam',
    'vg': 'British Virgin Islands',
    'vi': 'U.S. Virgin Islands',
    'wf': 'Wallis and Futuna',
    'eh': 'Western Sahara',
    'ye': 'Yemen',
    'zm': 'Zambia',
    'zw': 'Zimbabwe',
    'xk': 'Kosovo',
    'gb-wls': 'Wales',
    'ax': 'Aland Islands'
}
FLAGS_DICT = dict(sorted(FLAGS_DICT.items(), key=lambda item: item[1]))
FLAGS_IMAGES_LIST = [os.path.basename(file) for file in glob.glob("C:\\Github Projects\\FlagGame\\static\\flags/*")]
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
            return render_template("main.html", flag_image=random_flag, flag_name=current_flag_name, all_flags=FLAGS_DICT.values(), logged_in_uname=session['username'], score=TOTAL_SCORE, answer=THIS_ANSWER, flag_num=FLAG_COUNTER+1)
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
                THIS_ANSWER = f"Wrong!, The Flag Was {current_flag}"
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
        with open(r"C:\Github Projects\FlagGame\static\scoreboard.json", "r") as scoreboard_file:
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
    with open(r"C:\Github Projects\FlagGame\static\scoreboard.json", "r") as scoreboard_file:
        scoreboard = json.loads(scoreboard_file.read())
    if session['username'] in scoreboard.keys():
        if current_score > scoreboard[session['username']]:
            scoreboard[session['username']] = current_score
    else:
        scoreboard[session['username']] = current_score

    with open(r"C:\Github Projects\FlagGame\static\scoreboard.json", 'w') as scoreboard_file:
        json.dump(scoreboard, scoreboard_file, indent=4)

if __name__ == '__main__':
    app.run(debug=True)