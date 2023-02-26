# ----------------------------------------------------------------
# Some general crap functions
# ----------------------------------------------------------------

# TODO Objective get rid of this file
from ansi import *


# different sublevels
LEVELNAMES1 = ["ml","mr","ul","ur","dl","dr","nl","nr","MM","UU","DD","NN","AA"]
LEVELNAMES2 = ["mr","ul","ur","dl","dr","nl","nr","MM","UU","DD","NN","AA"]
LEVELNAMES3 = ["ur","dl","dr","nr","MM","UU","DD","NN"]
LEVELNAMES4 = ["dr","UU","DD","NN"]

# returns a number as string of lenght 3
def to3num(num):
	num = int(num)
	if num//100 > 0:
		return str(num)
	elif num//10 > 0:
		return " "+str(num)
	else:
		return "  "+str(num)

# transforms a dict to a list for printing with n attributes for each key
def dictToList(dict, n):
	out = []
	for key in dict:
		line = key
		for i in range(n):
			line += "\t" + dict[key][i]
		out.append(line)
	return out

# transforms a dict to a list for printing
def colorLevel(list):
	out = []
	for line in list:
		words = line.split("\t")
		if   words[4] == "True":
			if int(words[1]) == 0:
				color = ANSI.MEDIUM
			else:
				color = ANSI.GOOD
		else:
			color = ANSI.BAD
		line = color + words[0]
		color = ANSI.PERFECT
		if   int(words[1]) < 80:
			color = ANSI.BAD
		elif int(words[1]) < 95:
			color = ANSI.MEDIUM
		elif int(words[1]) < 100:
			color = ANSI.GOOD
		line += "\t" + color + words[1]
		color = ANSI.PERFECT
		if   int(words[2]) > 60:
			color = ANSI.BAD
		elif int(words[2]) > 30:
			color = ANSI.MEDIUM
		elif int(words[2]) > 10:
			color = ANSI.GOOD
		line += "\t" + color + words[2]
		color = ANSI.PERFECT
		if   int(words[3]) < 10:
			color = ANSI.BAD
		elif int(words[3]) < 50:
			color = ANSI.MEDIUM
		elif int(words[3]) < 100:
			color = ANSI.GOOD
		line += "\t" + color + words[3]
		line += ANSI.RESET
		out.append(line)
	return out

# get h elements of the list with offset
def toListData(offset, lines_length, lines_list, h):
	n = lines_length
	# short/long list fix
	out    = []
	if lines_length > h:
		n = h
	for i in range(n):
		out.append(lines_list[(offset+i)%lines_length])
	return( out )

# updates unlocked levels
def updateUnlocked(FILES):
	dict = {}
	fileRead(FILES.levels, dict)
	for key in LEVELNAMES1:
		if int(dict[key+".00"][0]) > 80 and int(dict[key+".00"][1]) < 40:
			dict[key+".01"][3] = "True"
		if int(dict[key+".01"][0]) > 80 and int(dict[key+".01"][1]) < 200:
			dict[key+".02"][3] = "True"
	for key in LEVELNAMES2:
		if int(dict[key+".03"][0]) > 80 and int(dict[key+".00"][1]) < 40:
			dict[key+".04"][3] = "True"
		if int(dict[key+".04"][0]) > 80 and int(dict[key+".01"][1]) < 200:
			dict[key+".05"][3] = "True"
	for key in LEVELNAMES3:
		if int(dict[key+".06"][0]) > 80 and int(dict[key+".00"][1]) < 40:
			dict[key+".07"][3] = "True"
		if int(dict[key+".07"][0]) > 80 and int(dict[key+".01"][1]) < 200:
			dict[key+".08"][3] = "True"
	for key in LEVELNAMES4:
		if int(dict[key+".09"][0]) > 80 and int(dict[key+".00"][1]) < 40:
			dict[key+".10"][3] = "True"
		if int(dict[key+".10"][0]) > 80 and int(dict[key+".01"][1]) < 200:
			dict[key+".11"][3] = "True"
	# separate additions
	# mr1->ml0
	if int(dict["ml.02"][0]) > 95 and int(dict["mr.02"][0]) > 95:
		dict["mr.03"][3] = "True"
	# ul1->mr1 & ul0
	if int(dict["mr.05"][0]) > 95 and int(dict["ul.02"][0]) > 95:
		dict["ul.03"][3] = "True"
	# ur1->ul0, ur2->ul1
	if int(dict["ul.02"][0]) > 95 and int(dict["ur.02"][0]) > 95:
		dict["ur.03"][3] = "True"
	if int(dict["ul.05"][0]) > 95 and int(dict["ur.02"][0]) > 95:
		dict["ur.06"][3] = "True"
	# dl1->ml0 & mr0, dl2->ur2
	if int(dict["mr.05"][0]) > 95 and int(dict["dl.02"][0]) > 95:
		dict["dl.03"][3] = "True"
	if int(dict["ur.08"][0]) > 95 and int(dict["dl.02"][0]) > 95:
		dict["dl.06"][3] = "True"
	# dr1->dl0, dr2->dl1, dl3->dl2
	if int(dict["dl.02"][0]) > 95 and int(dict["dr.02"][0]) > 95:
		dict["dr.03"][3] = "True"
	if int(dict["dl.05"][0]) > 95 and int(dict["dr.02"][0]) > 95:
		dict["dl.06"][3] = "True"
	if int(dict["dl.08"][0]) > 95 and int(dict["dr.02"][0]) > 95:
		dict["dl.09"][3] = "True"
	# nl1->dr3
	if int(dict["dr.11"][0]) > 95 and int(dict["nl.02"][0]) > 95:
		dict["nl.03"][3] = "True"
	# nr1->nl0, nr2->nl1
	if int(dict["nl.02"][0]) > 95 and int(dict["nr.02"][0]) > 95:
		dict["nr.03"][3] = "True"
	if int(dict["nl.05"][0]) > 95 and int(dict["nr.02"][0]) > 95:
		dict["nr.06"][3] = "True"
	# MM1->dr3,MM2->nr2
	if int(dict["dr.08"][0]) > 95 and int(dict["MM.02"][0]) > 95:
		dict["MM.03"][3] = "True"
	if int(dict["nr.05"][0]) > 95 and int(dict["MM.02"][0]) > 95:
		dict["MM.06"][3] = "True"
	# UU1->MM0, UU2->MM1, UU3->MM2
	if int(dict["MM.02"][0]) > 95 and int(dict["UU.02"][0]) > 95:
		dict["UU.03"][3] = "True"
	if int(dict["MM.05"][0]) > 95 and int(dict["UU.02"][0]) > 95:
		dict["UU.06"][3] = "True"
	if int(dict["MM.08"][0]) > 95 and int(dict["UU.02"][0]) > 95:
		dict["UU.09"][3] = "True"
	# DD1->UU1, DD2->UU2, DD3->MM3
	if int(dict["UU.05"][0]) > 95 and int(dict["DD.02"][0]) > 95:
		dict["DD.03"][3] = "True"
	if int(dict["UU.08"][0]) > 95 and int(dict["DD.02"][0]) > 95:
		dict["DD.06"][3] = "True"
	if int(dict["UU.11"][0]) > 95 and int(dict["DD.02"][0]) > 95:
		dict["DD.09"][3] = "True"
	# NN1->DD1, NN2->DD2, NN3->DD3
	if int(dict["DD.05"][0]) > 95 and int(dict["NN.02"][0]) > 95:
		dict["NN.03"][3] = "True"
	if int(dict["DD.08"][0]) > 95 and int(dict["NN.02"][0]) > 95:
		dict["NN.06"][3] = "True"
	if int(dict["DD.11"][0]) > 95 and int(dict["NN.02"][0]) > 95:
		dict["NN.09"][3] = "True"
	# AA1->AA0 & NN3
	if int(dict["NN.11"][0]) > 95 and int(dict["AA.02"][0]) > 95:
		dict["AA.03"][3] = "True"
	fileWrite(FILES.levels, dict)

#updates general statistics:
def updateStats(FILES):
	# get data
	dict = {}
	fileRead(FILES.levels, dict)
	# updatate percentage finished, WPM and correctness
	finished    = 0
	tested      = 0
	WPM         = 0
	correctness = 0
	for key in dict:
		if int(dict[key][0])==100:
			finished += 1
		if int(dict[key][0])!=0:
			tested += 1
			correctness += int(dict[key][0])
			WPM += int(dict[key][2])
	dict = {}
	fileRead(FILES.stats, dict)
	dict["levels_completed "] = [str(finished)]
	dict["correctness      "] = [str(correctness//tested)]
	dict["WPM              "] = [str(WPM//tested)]
	fileWrite(FILES.stats, dict)

# set correct training set
# returns set and word_count
def letterSet(FILES,level):
	level_name  =     level.split(".")[0][-2:]
	sub_level   = int(level.split(".")[1])//3
	sub_level_n = int(level.split(".")[1])%3
	# change here the numbers of letters
	letter_count= sub_level_n * sub_level_n * 64 + 64
	dict        = {}
	fileRead(FILES.layout, dict)
	letters_set = dict[level_name][0]
	if level_name == "mr":
		if sub_level > 0:
			letters_set += dict["ml"][0]
	elif level_name == "ul":
		if sub_level > 0:
			letters_set += dict["ml"][0]+dict["mr"][0]
	elif level_name == "ur":
		if sub_level > 0:
			letters_set += dict["ul"][0]
		if sub_level > 1:
			letters_set += dict["ml"][0]+dict["mr"][0]
	elif level_name == "dl":
		if sub_level > 0:
			letters_set += dict["ml"][0]+dict["mr"][0]
		if sub_level > 1:
			letters_set += dict["ul"][0]+dict["ur"][0]
	elif level_name == "dr":
		if sub_level > 0:
			letters_set += dict["dl"][0]
		if sub_level > 1:
			letters_set += dict["ml"][0]+dict["mr"][0]
		if sub_level > 2:
			letters_set += dict["ul"][0]+dict["ur"][0]
	elif level_name == "nl":
		if sub_level > 0:
			letters_set += dict["dl"][0]+dict["dr"][0]+dict["ul"][0]+dict["ur"][0]+dict["ml"][0]+dict["mr"][0]
	elif level_name == "nr":
		if sub_level > 0:
			letters_set += dict["nl"][0]
		if sub_level > 1:
			letters_set += dict["dl"][0]+dict["dr"][0]+dict["ul"][0]+dict["ur"][0]+dict["ml"][0]+dict["mr"][0]
	elif level_name == "MM":
		if sub_level > 0:
			letters_set += dict["dl"][0]+dict["dr"][0]+dict["ul"][0]+dict["ur"][0]+dict["ml"][0]+dict["mr"][0]
		if sub_level > 1:
			letters_set += dict["nl"][0]+dict["nr"][0]
	elif level_name == "UU":
		if sub_level > 0:
			letters_set += dict["MM"][0]
		if sub_level > 1:
			letters_set += dict["dl"][0]+dict["dr"][0]+dict["ul"][0]+dict["ur"][0]+dict["ml"][0]+dict["mr"][0]
		if sub_level > 2:
			letters_set += dict["nl"][0]+dict["nr"][0]
	elif level_name == "DD":
		if sub_level > 0:
			letters_set += dict["MM"][0] + dict["UU"][0]
		if sub_level > 1:
			letters_set += dict["dl"][0]+dict["dr"][0]+dict["ul"][0]+dict["ur"][0]+dict["ml"][0]+dict["mr"][0]
		if sub_level > 2:
			letters_set += dict["nl"][0]+dict["nr"][0]
	elif level_name == "NN":
		if sub_level > 0:
			letters_set += dict["DD"][0] + dict["MM"][0] + dict["UU"][0]
		if sub_level > 1:
			letters_set += dict["dl"][0]+dict["dr"][0]+dict["ul"][0]+dict["ur"][0]+dict["ml"][0]+dict["mr"][0]
		if sub_level > 2:
			letters_set += dict["nl"][0]+dict["nr"][0]
	elif level_name == "AA":
		if sub_level > 0:
			letters_set += dict["NN"][0] + dict["DD"][0] + dict["MM"][0] + dict["UU"][0]
			letters_set += dict["nr"][0] + dict["nl"][0]
			letters_set += dict["dr"][0] + dict["dl"][0] + dict["ur"][0] + dict["ul"][0] + dict["mr"][0] + dict["ml"][0]
	return([letters_set, letter_count])



# writes a file with data
def fileWrite(filename, dict):
	file = open(filename, "w")
	for key in dict:
		line = key
		for j in range(len(dict[key])):
			line += "\t"+dict[key][j]
		line += "\n"
		file.write(line)
	file.close()

# reads data from file
def fileRead(filename, dict):
	f = open(filename, "r")
	lines = f.readlines()
	for i in range(len(lines)):
		words = lines[i][:-1].split("\t")
		dict[ words[0] ] = words[1:]
	f.close()
