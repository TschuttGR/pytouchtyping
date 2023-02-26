# ----------------------------------------------------------------
# contains the functions for lessons and for learning
# ----------------------------------------------------------------

# TODO replace with from sshkeyboard import listen_keyboard
from getkey import getkey, keys 

from utils import *
from ansi import *
from display_terminal import *
import random
import time

# different sublevels
LEVELNAMES1 = ["ml","mr","ul","ur","dl","dr","nl","nr","MM","UU","DD","NN","AA"]
LEVELNAMES2 = ["mr","ul","ur","dl","dr","nl","nr","MM","UU","DD","NN","AA"]
LEVELNAMES3 = ["ur","dl","dr","nr","MM","UU","DD","NN"]
LEVELNAMES4 = ["dr","UU","DD","NN"]

# training of a level
def train(FILES,level):
	# get the letters to tain with
	letters_set, level_lenght = letterSet(FILES,level)
	letters_set = list(letters_set)
	training_letters = []
	spaces = 0
	i = 0
	while i < level_lenght:
		training_letters.append(random.choice(letters_set))
		i+=1
		# condition to avoid longer lines
		if i == level_lenght:
			break
		# randomly add spaces (not at end of line)
		if random.random() > 0.85 and i < level_lenght-1:
			training_letters.append(" ");
			spaces += 1
			i+=1
	training_colors = [ANSI.RESET]*level_lenght
	# initialize loop
	index  = 0
	errors = 0
	start = time.time()
	while index != level_lenght:
		row = index// 64
		col = index % 64
		tprint(row, training_letters, training_colors )
		key = getkey()
		if key == keys.ESCAPE:
			return
		if key == training_letters[64*row+col]:
			training_colors[64*row+col] = ANSI.CORRECT
		else:
			training_colors[64*row+col] = ANSI.WRONG
			errors += 1
		index += 1
	tprint(row, training_letters, training_colors )
	end  = time.time()
	# compute time WPN and correctness
	completed = 100 - errors * 100 // level_lenght
	elapsed   = int(end-start)
	WPM       = 60 * (1+spaces) // elapsed
	getkey()
	# print results
	out = ["","","",
		"Completed: "+to3num(completed)+ "%",
		"Time: "+ str(elapsed)+ " seconds",
		"WPM:  "+ to3num(WPM)]
	xprint(out,9)
	getkey()
	# Save progress and exit
	dict = {}
	fileRead(FILES.levels,dict)
	old = dict[level]
	new = [to3num(completed), str(elapsed), to3num(WPM), dict[level][3]]
	k = 1
	for i in range(3):
		if k*int(old[i]) > k*int(new[i]):
			new[i] = old[i]
		k *= -1
	dict[level] = new
	fileWrite(FILES.levels, dict)

def trainFile(filename):
	# get the letters to tain with
	file = open(filename, "r")
	training_letters = list(file.read().replace('\n', ''))
	text_lenght      = len(training_letters)
	training_colors  = [ANSI.RESET]*text_lenght
	index  = 0
	errors = 0
	spaces = 0
	start = time.time()
	while index != text_lenght:
		row = index// 64
		col = index % 64
		tprint(row, training_letters, training_colors )
		key = getkey()
		if key == keys.SPACE:
			spaces += 1
		if key == training_letters[64*row+col]:
			training_colors[64*row+col] = ANSI.CORRECT
		else:
			training_colors[64*row+col] = ANSI.WRONG
			errors += 1
		index += 1
	tprint(row, training_letters, training_colors )
	end  = time.time()
	# compute time WPN and correctness
	completed = 100 - errors * 100 // text_lenght
	elapsed   = int(end-start)
	WPM       = 60 * (1+spaces) // elapsed
	getkey()
	# print results
	out = ["","","",
		"Completed: "+to3num(completed)+ "%",
		"Time: "+ str(elapsed)+ " seconds",
		"WPM:  "+ to3num(WPM)]
	xprint(out,9)
	getkey()