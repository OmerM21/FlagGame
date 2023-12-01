from flask import Flask, render_template, request, session, redirect, url_for
import random
import glob
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

FLAGS_DICT = {'1f7fc295e3f492e073078756': 'Andorra', 'e45b053f058d6290974b04e1': 'United Arab Emirates', '5f29444aaa4b97e53bede02e': 'Afghanistan', 'dc74bd9b1badb811a028bd24': 'Antigua and Barbuda', '1c64ae244697da4f08d0edb9': 'Anguilla', 'f420c46ec9374a61a9a6bd06': 'Albania', '57bb2e07b58350dbaf4f6633': 'Armenia', '62c3b29a275ce8119471c079': 'Angola', 'ad8bfcc2d7134f61dd7e0546': 'Antarctica', 'd7d91cdadd6646e3e88c893a': 
'Argentina', '6fbc153931cf82c5b6617838': 'American Samoa', 'a3595b830e4b7190cff7eb43': 'Austria', '9e602a948dd7eeba15b9a797': 'Australia', '2965d7f684386ee728f2e7d4': 'Aruba', '6e80a869b6703088e7675b22': 'Aland Islands', '7ce739bf4ac86a954a20378f': 'Azerbaijan', 'c6a0e29f21a5d5dfa6f077d2': 'Bosnia and Herzegovina', '2846f13f003235a73a597fac': 'Barbados', '14b80aa2f3a1865395d47807': 'Bangladesh', '547cae4512d468c67b617bc9': 'Belgium', '1031150af5782288206dee8b': 'Burkina Faso', '30d92046c4ec1e14dd66ef49': 'Bulgaria', 'ad95a0b15cd214bb25b2b31d': 'Bahrain', 'a6f658fefe26b3434b228b65': 'Burundi', '313acd6c42165934a62a96fb': 'Benin', 'c5c05ed5b37701e42c90c73d': 'Saint Barthelemy', '7d802f0da12691c9e96311b4': 'Bermuda', 'bc2d9ef3a0573ae183eb2f1a': 'Brunei', '26e2f656f82f80a040f52a61': 'Bolivia', '5969fcece0544928c8f3b1c5': 'Bonaire, Sint Eustatius, and Saba', 'bec5b7869f486094aef3f9d7': 'Brazil', '2ba094fa509101e08a3dbe40': 'Bahamas', 'a2a7fc870b7eb4a5e986d287': 'Bhutan', '6465c207f14dc8ae2d33de24': 'Bouvet Island', 'c71c1ce7784d4c6a12b0171e': 'Botswana', '8019fee0e8986e19c3df0866': 'Belarus', 'ad48c8690d70345af9c697eb': 'Belize', 'a2a8ef3c72070478745c10c1': 'Canada', 'd87ac4262661d68e6bf3ed25': 'Cocos (Keeling) Islands', 
'3a46e01fddb6fedf8a62d218': 'Congo (Congo-Kinshasa)', '66a91bda055a0ee923f90a44': 'Central African Republic', '22f5f967544df6d68ad55a5b': 'Congo (Congo-Brazzaville)', 'bd089bc3e148cbdab1e3332d': 'Switzerland', 'cbc8c9412cc955f59ece964a': 'Cote dIvoire', '58fa5c4793c4667ff8191083': 'Cook Islands', '601effce8d8af9673e53428c': 'Chile', 'ca3d967d3898421188e50040': 'Cameroon', 'fe4a4dcd55a0be2590bdaabb': 'China', 
'0d75bf67bb7bf9efa3e01082': 'Colombia', 'fc681e4b6c939ed5ffd19ed1': 'Costa Rica', '09f2da1e0139838c091916a6': 'Cuba', 'd8817aaa4a00886560567cbe': 'Cabo Verde', 'ddefa3f3b0b44548eaf0e5cd': 'Curaçao', '7838f05f535751204708a1b6': 'Christmas Island', '105a5512e114f0a95f701a21': 'Cyprus', '38723827802055c25faa2a82': 'Czechia', 'd91d3a5c3c4ac88f13ce3a9e': 'Germany', '8a380a56ae939384c0cf9f35': 'Djibouti', '4a14e55298eb845d92669c75': 'Denmark', '270f9a5bd99196982db267d0': 'Dominica', '97f3ef473e76252ddd9e4c7c': 'Dominican Republic', 'afd925b930854e7c49c739c5': 'Algeria', '6288e709cfd5a194f87a20e8': 'Ecuador', 'c138bc72d04d4b6855919a1a': 'Estonia', 'c2915153e9554609ca37b47a': 'Egypt', '68f1369699d9213d63260558': 'Western Sahara', '04dcad29e5f22e39e0dec12f': 'Eritrea', 'fc1ad8d7164c91295c29b75e': 'Spain', '16e8a954b72eff662aaca1f1': 'Ethiopia', '9f0e8a78f19b3e1636bcab58': 'Finland', '1193ecf781e55dd0a2c780be': 'Fiji', '8d7a1bc35977a94277743b1a': 'Falkland Islands (Islas Malvinas)', '4e5359586cdd5d752c2e2039': 'Micronesia', 
'37e70919dde9f8a9fe0ff422': 'Faroe Islands', 'a2ab2045526fc5f9413e7e5c': 'France', 'cce44a464cb6a354169279cd': 'Gabon', '1c1ca900866a741a2062d961': 'England', '054f92e99b611084ed491788': 'North Ireland', '921ec51f7b919fd6f38d0edc': 'Scotland', '880e3adbc4272a9c5612f3f0': 'Wales', '85453f6784c2844505ae565f': 'United Kingdom', '6169610ab9d77d491cdfd4ba': 'Grenada', '58a7abe41ea4f1d6ba56bccc': 'Georgia', 'a1ee63e0b61f624f5c4788d5': 'French Guiana', 'cbb1f89f92d0ab55dfcfaa3b': 'Guernsey', '87cfb653be68eaf18cecebb2': 'Ghana', '3866873efa637cbac4a7b458': 'Gibraltar', '6f5897e8f6068e61e13481cf': 'Greenland', '49f558dc2c6eb5c01df69339': 'Gambia', '9c4a8a1fd3e34e9aba1de93e': 'Guinea', '98e47fc5a1f94a8863c8e82a': 'Guadeloupe', 'b0f4527498543c145c5567dd': 'Equatorial Guinea', 'a9929dfcb111943445f789c3': 'Greece', '6b3aa7368647e85a7287997e': 'South Georgia and South Sandwich Islands', '790a781fb1117fa395ca6044': 'Guatemala', 'd9d5adc5c4a5f7f6c0b314ab': 'Guam', '2704fcbca37986b30091b92d': 'Guinea-Bissau', 'f7f617c97649abab3f93f617': 'Guyana', '6018ff0139209850e8fd37ea': 'Hong Kong', '88ef149e131259716fcd0e9e': 'Heard Island and McDonald Islands', 'eebfd1dd1fda96eb9613d0e9': 'Honduras', '76707422298c825530204485': 'Croatia', '7ade1c6fbbe23f7a5ab3434d': 'Haiti', '780f5b71da3ce11b6216e56d': 'Hungary', '5597c428aef2dec1762a8f7c': 'Indonesia', 'c81c3845a84c719e9d0d3555': 'Ireland', 'cd749f43e8ef7692a2d9b678': 'Israel', '972f728e8b106452b41b2942': 'Isle of Man', '9bc1b5fddc0532fa21ce47b6': 'India', '22f33a39a0e403e55baf0791': 'British Indian Ocean Territory', '499e48baf91d5ff0cbfb4dcf': 'Iraq', '3a46ecfa8637e1b6c8690b15': 'Iran', 'eebd4c0f4e425f2432862a9a': 'Iceland', 'ca20744335bbda62caf9ba0f': 'Italy', 'a1c85af490ce11dcf17cb699': 'Jersey', 'c7d236306541ce69289c84d9': 'Jamaica', 'ad239e17445bd1e2988f86d6': 'Jordan', 'ace2fe9cc089f55a3ac5d61d': 'Japan', 'ea3dfbf54d2380720b49031b': 'Kenya', '6a9065628f4c06e6d5da51b2': 'Kyrgyzstan', '74d10b19838a84440812be31': 'Cambodia', '3970777540b901ecaad6d2a0': 'Kiribati', '55d902e48a62c0516d087682': 'Comoros', 'c5ed6dc212ace3b55597b07e': 'Saint Kitts and Nevis', '00e08788ec64f5625df5accc': 'North Korea', '3061f8fdeec0b4e5647a307c': 'South Korea', 'd1beb985415445d20959f353': 'Kuwait', '4a00220d34b93d2ea8eaf3ba': 'Cayman Islands', 'd173ac14427685617163594c': 'Kazakhstan', '27d5b2bcba946b1b97818ae3': 'Laos', '7bcbcc13e68dbf3b58d22862': 'Lebanon', '89494fb2af8961dd20f12007': 'Saint Lucia', 'ef944933b42dd1d708e8147a': 'Liechtenstein', 'b2609a10779f4fdc896af235': 'Sri Lanka', '3cb40d7b43e9250878a967a5': 'Liberia', 'a0d4b73406c58fe995e18a84': 'Lesotho', '99b3b4cb5c97d96e42030932': 'Lithuania', '6e1e307fe8487628ac2eebb5': 'Luxembourg', '8bbe2cb2c79e443a973a6f61': 'Latvia', 'd58be3d38f5c8ec9ea561cf7': 'Libya', '25da0afad0be4f2072a920e4': 'Morocco', 'cb73377c73f7b81e2702523b': 'Monaco', '095ca8c3512a87a7f6a4e3d6': 'Moldova', '86e89857bb7c6d430140abbc': 'Montenegro', '010e7f1ff9e8d2ccc06d108e': 'Saint Martin', '9c42c78c2b9595266e27fa5f': 'Madagascar', '473b979e1eb020ff62255e40': 'Marshall Islands', 'f61b42fd8eae6423ce03b9d2': 
'North Macedonia', 'df8912164e5f131fd1760c6c': 'Mali', '22569de0f851b0423ca191dc': 'Myanmar (Burma)', 'ebef5712b54afe3825b7ccf8': 'Mongolia', 'ec382c87376cbac4aa68d90a': 'Macao', '94a7ed0ce03e64d109384253': 'Northern Mariana Islands', 'e8309719e2e546d4802c2c64': 'Martinique', 'd54ad25df5670ab2eecddf40': 'Mauritania', 'ba5f3495f4649c966dadf549': 'Montserrat', '7b5a8935e0ccb9519abc659b': 'Malta', '316704cfb21f90110db48901': 'Mauritius', '91d62bc888f259bdec5a86e3': 'Maldives', '6f36a96fa2fc5493142319da': 'Malawi', '02beab092bb7827fe00cc564': 'Mexico', 'f1dcbc9aa546fe0ca176c962': 'Malaysia', '128eb51ef47e14924595650c': 'Mozambique', '4cea2f14cbb1af16ea124d30': 'Namibia', 'f8a2a7518a315b8f81e2bf9b': 'New Caledonia', '853aa63e515166545675e4b1': 'Niger', 'b07f043c6ce69f6c88490e98': 'Norfolk Island', '47a92f02425a2a350324b265': 'Nigeria', 'ed3e1511bd5c877c15d56735': 'Nicaragua', '3ef488b87a1d07d2ac1b6660': 'Netherlands', '4c3057ff35daba762e6a3c6a': 'Norway', '68b62ef95049431081f11c3a': 'Nepal', '348a346eb5711fa5d1d97a52': 
'Nauru', '29893d1e9ccea592e4a95e65': 'Niue', '23ba4f5556fdc4126b0bca1c': 'New Zealand', 'e16b2948280c38787cb203e4': 'Oman', 'ad2a9021067a2ac2a92bd1c8': 'Panama', 'b6896296205ba132617fca48': 'Peru', '721c220dce00f681c87146ef': 'French Polynesia', '63006fd55405921796920e78': 'Papua New Guinea', '27cdb5ec579432143f906628': 'Philippines', '3f4e6bdd7f44426572da385f': 'Pakistan', '76a9bbd6a53b2d29a1ff8fde': 'Poland', 'fe6681b20c15335ab75e102e': 'Saint Pierre and Miquelon', '7601005e1a19501a71328f93': 'Pitcairn Islands', 'e68b98c422a3797ddd23a392': 'Puerto Rico', 'dea83e69f9f045e9ced20060': 'Portugal', '93b0843067125f898a50e4ea': 'Palau', '552d92e2cb2bf3ca120efa58': 'Paraguay', '67a6233d2894903e773cac2f': 'Qatar', 'fed272df0283289f1e22770b': 'Réunion', 'e2897c1d9a930edde118c63c': 'Romania', 'b5649298eb58ba271feb54f5': 'Serbia', 'c4024ece1a1ed36f609a3574': 'Russia', 'aeb9ef5b688066f625706690': 'Rwanda', '1dae1f476e608cec6d33e791': 'Saudi Arabia', '23031966de8b90133ede8999': 'Solomon Islands', '587e39fbef252c41f9f92930': 'Seychelles', 'b0af9883386bc549a460ca32': 'Sudan', '2b453f0ffc4646431fd7f2f0': 'Sweden', 'bde5e3ddfc9b16f11ae04e77': 'Singapore', 'd287868dd46ab3299221b4ee': 'Saint Helena', 'cc1c04a3923d307d289528e0': 'Slovenia', '47068e0e654774fde181e56f': 'Svalbard and Jan Mayen', 'aff1de6777a1d646ca7d3f97': 'Slovakia', 'a0f025991fa1165eaeb4154f': 'Sierra Leone', '721b9c215009a87710f65ce6': 'San Marino', '124a5117549906eb372e58e9': 'Senegal', 'd8ff55ecb61e7a9f6f4b6d34': 'Somalia', '33a3d4458cba96ade8d72d66': 'Suriname', '6bdb6af161816222958e2eb5': 'South Sudan', '04481d9f4b56171202432766': 'Sao Tomé and Principe', 'ebd92380391f0a748dded8e3': 'El Salvador', 'e27b7832c36c524983b00877': 'Sint Maarten', 'c5e58436e9f7d5a262cc46aa': 'Syria', '9c883f3585e2a66823daffca': 'Eswatini', 'e28cab3de95bb385270096f4': 'Turks and Caicos Islands', '8815cb30ba010fe8d7182461': 'Chad', '1d005a69afdd1cc6b9b00b90': 'French Southern Territories', 'ab5a1d1f5882b67eb02b21fa': 'Togo', 'b33b0c406e0ae91182b4e31b': 'Thailand', '436eb4b0de3528d2a53f7fc9': 'Tajikistan', 'd7a347914f27e5b1564834a8': 'Tokelau', '48ed9c03b119a1c216c7cb98': 'Timor-Leste', '79f57593ed0cde753cc4e178': 'Turkmenistan', '4de171e1edf1e93d13d7c72d': 'Tunisia', 'dccd5e5623b4139a4c8f179d': 'Tonga', 'ad7b3a195b259a2e5729472e': 'Turkey', 'b29b9ac51c0233c1f551e01c': 'Trinidad and Tobago', 'fbf984829eb2cbf005292ef5': 'Tuvalu', '04cfe44da275870a714710aa': 'Taiwan', 'd67dfe4b533290f96be9e964': 'Tanzania', '2ffed9c2a2f94c754bc763c8': 'Ukraine', 'bfcaed574f4d7f97c93bc8b7': 'Uganda', '785beba16e16994ec0d0eb99': 'United States Minor Outlying Islands', '19c0aeec94b8b11ecf09980a': 'United States', 'b5cf55576b493351ee14721d': 'Uruguay', 'd73a8abeda1cc5f65e5c5e7c': 'Uzbekistan', 'ccca7ea4c7ec69a6aa00ce8c': 'Vatican City (Holy See)', 'c0a9c16fb22fe59c3f6f7db0': 'Saint Vincent and the Grenadines', '6c02aa10715a4e23c624420d': 'Venezuela', 'a8ca43ce12f771b195b35e74': 'British Virgin Islands', '9338a67edcc1ccabec41de16': 'U.S. Virgin Islands', '439881ea6fb5cd9a48d8a9e0': 'Vietnam', '0509e47b239f12cdfbec87e1': 'Vanuatu', 
'70828274966fa66fa94f710e': 'Wallis and Futuna', 'b463c47b247a0a5902e582b1': 'Samoa', '7930b9aa739665c468a5cac3': 'Kosovo', '2337e567c9bef7c4424b0d25': 'Yemen', 'bfe014dccfa45a63c2597a7b': 'Mayotte', 'fec98e8bd9222b340dca12c4': 'South Africa', '28617cd06a1ccdb8b441ce7c': 'Zambia', 'f1ab2c56ecc80119aef02b8f': 'Zimbabwe'}

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

def get_user_hs():
    with open(r"C:\Github Projects\FlagGame\static\scoreboard.json", "r") as scoreboard_file:
        scoreboard = json.loads(scoreboard_file.read())
    if session['username'] in scoreboard.keys():
        return scoreboard[session['username']]
    else:
        return 0

if __name__ == '__main__':
    app.run(debug=True)