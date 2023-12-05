import os
import json
import random
import glob

current_dir = os.path.dirname(os.path.abspath(__file__))
FLAGS_IMAGES_PATH = os.path.join(current_dir, "flags")
FLAGS_DICT_PATH = os.path.join(current_dir, "flags.json")
SCOREBOARD_PATH = os.path.join(current_dir, "scoreboard.json")

with open(FLAGS_DICT_PATH, "r") as flags_dict_file:
    flags_dict = json.loads(flags_dict_file.read())

FLAGS_DICT = flags_dict
FLAGS_DICT = dict(sorted(FLAGS_DICT.items(), key=lambda item: item[1]))
FLAGS_IMAGES_LIST = [os.path.basename(file) for file in glob.glob(f"{FLAGS_IMAGES_PATH}/*")]
FLAGS_POS_LIST = list(range(253))
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
        if self.flagcounter == len(self.flagposlist)-1:
            self.submit_game()
        else:
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