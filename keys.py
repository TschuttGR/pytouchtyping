#!/usr/local/bin/python3

import sys
import os
import shutil
import random
import time
from getkey import getkey, keys

#ERASE_LINE = '\x1b[0K'
#CURSOR_UP_ONE = '\x1b[1A'
#CURSOR_DOWN_ONE = '\x1b[1B'
#CURSOR_RIGHT_ONE = '\x1b[1C'
#CURSOR_LEFT_ONE = '\x1b[1D'

# CLASSES:
# ------------------------------------------------------------------------------

# Stored colors:
class COLORS:
    # text color form 30 to 37 or 90 to 97
    # background from 40 to 47 or 100 to 106
    # black, red, lime, yellow, blue, pink, cyan, white
    RESET   = "\033[0;0m"
    NORMAL  = "\033[0;37;40m"
    CORRECT = "\033[0;37;42m"
    WRONG   = "\033[0;37;41m"
    PERFECT = "\033[96m"
    GOOD    = "\033[92m"
    MEDIUM  = "\033[93m"
    BAD     = "\033[91m"

# stored path names:
class FILE:
    home     = ""    # user home folder
    main     = ""    # hidden folder containing data
    keyboard = ""    # keyboard layouts folder
    layout   = ""    # selected keyboard layout
    files    = ""    # files folder
    levels   = ""    # levels data
    stats    = ""    # statistics data

# different sublevels
LEVELNAMES1 = ["ml","mr","ul","ur","dl","dr","nl","nr","MM","UU","DD","NN","AA"]
LEVELNAMES2 = ["mr","ul","ur","dl","dr","nl","nr","MM","UU","DD","NN","AA"]
LEVELNAMES3 = ["ur","dl","dr","nr","MM","UU","DD","NN"]
LEVELNAMES4 = ["dr","UU","DD","NN"]

# UTILITIES:
# ------------------------------------------------------------------------------

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
                color = COLORS.MEDIUM
            else:
                color = COLORS.GOOD
        else:
            color = COLORS.BAD
        line = color + words[0]
        color = COLORS.PERFECT
        if   int(words[1]) < 80:
            color = COLORS.BAD
        elif int(words[1]) < 95:
            color = COLORS.MEDIUM
        elif int(words[1]) < 100:
            color = COLORS.GOOD
        line += "\t" + color + words[1]
        color = COLORS.PERFECT
        if   int(words[2]) > 60:
            color = COLORS.BAD
        elif int(words[2]) > 30:
            color = COLORS.MEDIUM
        elif int(words[2]) > 10:
            color = COLORS.GOOD
        line += "\t" + color + words[2]
        color = COLORS.PERFECT
        if   int(words[3]) < 10:
            color = COLORS.BAD
        elif int(words[3]) < 50:
            color = COLORS.MEDIUM
        elif int(words[3]) < 100:
            color = COLORS.GOOD
        line += "\t" + color + words[3]
        line += COLORS.RESET
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
def updateUnlocked():
    dict = {}
    fileRead(FILE.levels, dict)
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
    fileWrite(FILE.levels, dict)

#updates general statistics:
def updateStats():
    # get data
    dict = {}
    fileRead(FILE.levels, dict)
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
    fileRead(FILE.stats, dict)
    dict["levels_completed "] = [str(finished)]
    dict["correctness      "] = [str(correctness//tested)]
    dict["WPM              "] = [str(WPM//tested)]
    fileWrite(FILE.stats, dict)

# set correct training set
# returns set and word_count
def letterSet(level):
    level_name  =     level.split(".")[0][-2:]
    sub_level   = int(level.split(".")[1])//3
    sub_level_n = int(level.split(".")[1])%3
    # change here the numbers of letters
    letter_count= sub_level_n * sub_level_n * 64 + 64
    dict        = {}
    fileRead(FILE.layout, dict)
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

# PRINTINGS
# ------------------------------------------------------------------------------

# prints a 9*80 block
# plist is the data and h the height
def xprint(plist, h):
    """prints message of height 9"""
    print("\x1b[9A", end = '')
    l = len(plist)
    for i in range(l):
        print("\x1b[0K"+plist[i])
    for i in range(h-l):
        print("\x1b[0K")

def tprint(row, data, colors):
    """Imports the list of chars and colors and lenght"""
    """correctly prints the list with colors"""
    leng = len(data)-1
    max_row = leng// 64
    max_col = leng % 64
    out = [""]*3
    line = "       "
    k = -1
    while k <= 1:
        # avoid to jump out
        i = k + row
        if i == max_row:
            end = max_col
        elif i > max_row:
            end = -1
        elif i == -1:
            end = -1
        else:
            end = 63
        j = 0
        line = "        "
        while j <= end:
            #print(str(i)+" "+str(j))
            line += colors[i*64+j] + data[i*64+j]
            j += 1
        line += COLORS.RESET
        out.append(line)
        k+=1
    xprint(out,9)

# prints a 9*80 full list with cursor
def sprint(index, data):
    """Gets arrow index, and data array"""
    """Prints it in a fancy way"""
    n = len(data)
    out = [""]
    # print spaced from border
    for i in range(n):
        out.append("    "+data[i])
    out+=[""]*(8-n)
    xprint(out, 9)
    # print cursor
    index = str(index+2)
    print(
        "\x1b["+index+"A"+"\x1b[2C"+">"+"\x1b[3D"+"\x1b["+index+"B",
        end='', flush=True)

# prints a 9*80 level with fancy title
def lprint(index, data):
    """Gets arrow index, and levels array"""
    """Prints it in a fancy way"""
    n = len(data)
    # add title
    out = [
        "",
        "    LEVEL   Completed  Time    WPM",
        "    --------------------------------"
    ]
    # print spaced from border
    for i in range(n):
        out.append("    "+data[i])
    out+=[""]*(6-n)
    xprint(out, 9)
    # print cursor
    index = str(index+2)
    print(
        "\x1b["+index+"A"+"\x1b[2C"+">"+"\x1b[3D"+"\x1b["+index+"B",
        end='', flush=True)

# prints a 9*80 menu
def mprint(index, data):
    """Gets arrow index, and data array"""
    """Prints it in a fancy way"""
    # ["keyboard layout", "completed percentage", "filename", "correct percentage", "WPM"]
    # index from bottom to top
    out = [""]
    out.append("    To move use <arrows>, to select press <enter> to go back <esc>")
    out.append("    Passed files have to be txt")
    out.append("")
    out.append("    SET KEYBOARD LAYOUT    X                    ")
    out.append("    LEVELS                 XXX% completed       ")
    out.append("    FILE                   X                    ")
    out.append("    STATS                  XXX% correct  XXX WPM")
    out.append("")
    xprint(out, 9)
    # add details
    # print cursor
    index = str(index+2)
    print(
        "\x1b["+index+"A"+"\x1b[2C"+">"+"\x1b[3D"+"\x1b["+index+"B",
        end='', flush=True)
    # print keyboard layout
    n = str(len(data[0]))
    print(
        "\x1b[5A"+"\x1b[27C"+data[0]+"\x1b["+n+"D"+"\x1b[27D"+"\x1b[5B",
        end='', flush=True)
    # print completion percentage
    s = to3num(data[1])
    print(
        "\x1b[4A"+"\x1b[27C"+s+"\x1b[30D"+"\x1b[4B",
        end='', flush=True)
    # print filename
    n = str(len(data[2]))
    print(
        "\x1b[3A"+"\x1b[27C"+data[2]+"\x1b["+n+"D"+"\x1b[27D"+"\x1b[3B",
        end='', flush=True)
    # print correctness
    s = to3num(data[3])
    print(
        "\x1b[2A"+"\x1b[27C"+s+"\x1b[30D"+"\x1b[2B",
        end='', flush=True)
    # print WPM
    s = to3num(data[4])
    print(
        "\x1b[2A"+"\x1b[41C"+s+"\x1b[44D"+"\x1b[2B",
        end='', flush=True)

#INTERACTION
# ------------------------------------------------------------------------------

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

# training of a level
def train(level):
    # get the letters to tain with
    letters_set, level_lenght = letterSet(level)
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
    training_colors = [COLORS.RESET]*level_lenght
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
            training_colors[64*row+col] = COLORS.CORRECT
        else:
            training_colors[64*row+col] = COLORS.WRONG
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
    fileRead(FILE.levels,dict)
    old = dict[level]
    new = [to3num(completed), str(elapsed), to3num(WPM), dict[level][3]]
    k = 1
    for i in range(3):
        if k*int(old[i]) > k*int(new[i]):
            new[i] = old[i]
        k *= -1
    dict[level] = new
    fileWrite(FILE.levels, dict)

def trainFile(filename):
    # get the letters to tain with
    file = open(filename, "r")
    training_letters = list(file.read().replace('\n', ''))
    text_lenght      = len(training_letters)
    training_colors  = [COLORS.RESET]*text_lenght
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
            training_colors[64*row+col] = COLORS.CORRECT
        else:
            training_colors[64*row+col] = COLORS.WRONG
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

# sets the keyboard from user input
def setKeyboard():
    message = ["",
        "    What name should your new keyboard layout have?",
        "    By reusing an existing filename you overwrite it.",
        "    Write and press <enter>"]
    xprint(message, 8)
    # set the keyboard
    basename = input("")+".txt"
    FILE.layout = os.path.join(FILE.keyboard, basename)
    stats = {}
    fileRead(FILE.stats,stats)
    stats["selected_keyboard"] = [basename]
    fileWrite(FILE.stats,stats)

    message = ["",
        "    Filename set to: "+basename,
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    input("\x1b[0K")

    # write the keyboard file
    dict = {}

    message = ["",
        "    Write all lower case letters",
        "    of the left half of the middle line.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["ml"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all lower case letters",
        "    of the right half of the middle line.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["mr"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all lower case letters",
        "    of the left half of the upper line.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["ul"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all lower case letters",
        "    of the right half of the upper line.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["ur"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all lower case letters",
        "    of the left half of the lower line.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["dl"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all lower case letters",
        "    of the right half of the lower line.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["dr"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all lower case letters",
        "    of the left half of the numbers line.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["nl"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all lower case letters",
        "    of the right half of the numbers line.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["nr"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all Upper case letters",
        "    of the middle line.",
        "    Do not forget to press <Shift>!",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["MM"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all Upper case letters",
        "    of the upper line.",
        "    Do not forget to press <Shift>!",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["UU"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all Upper case letters",
        "    of the lower line.",
        "    Do not forget to press <Shift>!",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["DD"][0]=[input("\x1b[0K")]

    message = ["",
        "    Write all Upper case letters",
        "    of the number line.",
        "    Do not forget to press <Shift>!",
        "    for accents press <space>.",
        "    Write and press <enter> to continue."]
    xprint(message, 8)
    dict["NN"][0]=[input("\x1b[0K")]

    message = ["",
        "    Now you can add some other important characters.",
        "    for accents press <space>.",
        "    Write and press <enter> to continue",
        "    or just press <enter> if no chars have to be added."]
    xprint(message, 8)
    dict["AA"][0]=[input("\x1b[0K")]

    fileWrite(FILE.layout, dict)

    message = ["",
        "    Done.",
        "    Press <enter> to finish."]
    xprint(message, 8)
    input("\x1b[0K")

# submenu for keyboards
def keyboards():
    """Keyboard selecting function, allows to select keyboards"""
    # loop initialisation
    names_list = ["< NEW KEYBOARD LAYOUT >"]
    names_list += list(map(os.path.basename, os.listdir(FILE.keyboard)))
    cursor = 6
    offset = 0
    names_length = len(names_list)
    while True:
        print_data = toListData(offset, names_length, names_list, 7)
        # get correct height
        n = names_length
        if names_length > 7:
            n = 7
        # print level
        sprint(cursor, print_data)
        # action
        key = getkey()
        if key == keys.UP:
            if cursor == 6:
                offset = (offset - 1)%names_length
            else:
                cursor += 1
        elif key == keys.DOWN:
            if cursor == 7-n:
                offset = (offset + 1)%names_length
            else:
                cursor -= 1
        elif key == keys.ENTER:
            if print_data[(6-cursor)%7]=="< NEW KEYBOARD LAYOUT >":
                # SET NEW KEYBOARD
                setKeyboard()
                break
            else:
                # SET from old keyboard
                basename = print_data[(6-cursor)%7]
                FILE.layout = os.path.join(FILE.keyboard, basename)
                stats = {}
                fileRead(FILE.stats,stats)
                stats["selected_keyboard"] = [basename]
                fileWrite(FILE.stats,stats)
                break
        elif key == keys.ESCAPE:
            break

# Submenu for levels
def levels():
    """File input selecting function, allows to select levels"""
    # loop initialisation
    # fix dict To level
    cursor = 4
    offset = 0
    while True:
        dict = {}
        fileRead(FILE.levels, dict)
        lines_list = dictToList(dict, 4)
        lines_length = len(lines_list)
        print_data = toListData(offset, lines_length, lines_list, 5)
        # print levels
        lprint(cursor, colorLevel(print_data))
        # action
        key = getkey()
        if key == keys.UP:
            if cursor == 4:
                offset = (offset - 1)%lines_length
            else:
                cursor += 1
        elif key == keys.DOWN:
            if cursor == 0:
                offset = (offset + 1)%lines_length
            else:
                cursor -= 1
        elif key == keys.ENTER:
            # if no keyboard layout given set it
            dict = {}
            fileRead(FILE.stats, dict)
            if dict["selected_keyboard"][0] == "NOT_GIVEN":
                keyboards()
            # run training level
            dict = {}
            fileRead(FILE.levels, dict)
            level = print_data[(4-cursor)%5].split("\t")[0]
            if (dict[level][3]=="False"):
                print("\x1b[0K"+"You haven't unlocked this level yet!", end = "", flush = True)
            else:
                print("\x1b[0K", end = "", flush = True)
                train(level)
            # update levels
            updateUnlocked()
            updateStats()
            # move cursor to next level
            if cursor == 0:
                offset = (offset + 1)%lines_length
            else:
                cursor -= 1
        elif key == keys.ESCAPE:
            break

# submenu for selecting files
def fileInput():
    """File input selecting function, allows to select levels"""
    # loop initialisation
    names_list = list(map(os.path.basename, os.listdir(FILE.files)))
    cursor = 6
    offset = 0
    names_length = len(names_list)
    while True:
        print_data = toListData(offset, names_length, names_list, 7)

        # if no file error message
        if names_length == 0:
            message = ["",
                "    No File available!",
                "    Use the following command: python3 keys.py <file_path>",
                "    Press <enter> to continue"]
            xprint(message, 8)
            input("")
            break

        # get correct height
        n = names_length
        if names_length > 7:
            n = 7
        # print files
        sprint(cursor, print_data)
        # action
        key = getkey()
        if key == keys.UP:
            if cursor == 6:
                offset = (offset - 1)%names_length
            else:
                 cursor += 1
        elif key == keys.DOWN:
            if cursor == 7-n:
                offset = (offset + 1)%names_length
            else:
                cursor -= 1
        elif key == keys.ENTER:
            # run training level for that file
            basename = print_data[(6-cursor)%7]
            FILE.input = os.path.join(FILE.files, basename)
            stats = {}
            fileRead(FILE.stats,stats)
            stats["selected_file    "] = [basename]
            fileWrite(FILE.stats,stats)
            trainFile(FILE.input)
            break
        elif key == keys.ESCAPE:
            break

# submenu for  stats
def stats():
    """File input selecting function, allows to wiev statistics"""
    # loop initialisation
    dict = {}
    fileRead(FILE.stats, dict)
    names_list = dictToList(dict,1)
    cursor = 6
    offset = 0
    leng   = len(names_list)
    while True:
        print_data = toListData(offset, leng, names_list, 7)
        # print stats
        sprint(cursor, print_data)
        # action
        key = getkey()
        if key == keys.UP:
            if cursor == 6:
                offset = (offset - 1)%leng
            else:
                cursor += 1
        elif key == keys.DOWN:
            if cursor == 0:
                offset = (offset + 1)%leng
            else:
                 cursor -= 1
        elif key == keys.ESCAPE:
            break

# returns data for menu
def toMdata():
    # get stats for main function
    stats = {}
    fileRead(FILE.stats,stats)
    return([
        stats["selected_keyboard"][0],
        stats["levels_completed "][0],
        stats["selected_file    "][0],
        stats["correctness      "][0],
        stats["WPM              "][0]
        ])

# main menu
def main():
    """Menu function, allows to select program"""
    # loop initialisation
    cursor = 3
    while True:
        # function body
        print_data = toMdata()
        # print menu
        mprint(cursor, print_data)
        # action
        key = getkey()
        if key == keys.UP:
            cursor = (cursor+1)%4
        elif key == keys.DOWN:
            cursor = (cursor-1)%4
        elif key == keys.ENTER:
            # case stats
            if cursor == 0:
                stats()
            # case file
            if cursor == 1:
                fileInput()
            # case levels
            if cursor == 2:
                levels()
            # case key layout
            if cursor == 3:
                keyboards()
        elif key == keys.ESCAPE:
            break
        # exit condition

# initialize filesistem
def init():
    """Function called to initialize all directories and check existence."""
    """Returns home folder path and filename"""
    # print printing padding
    print("\n"*8)
    # OS = sys.platform
    # Get the home folder
    FILE.home     = os.path.expanduser("~")
    FILE.main     = os.path.join(FILE.home,".keyTouch")
    FILE.keyboard = os.path.join(FILE.main,"keyboard")
    FILE.files    = os.path.join(FILE.main,"files")
    FILE.levels   = os.path.join(FILE.main,"levels.txt")
    FILE.stats    = os.path.join(FILE.main,"stats.txt")
    # check if folder used in this script existst else create it
    if not os.path.isdir(FILE.main):
        os.mkdir(FILE.main)
    # check if subfiles existing otherways create them
    if not os.path.isdir(FILE.keyboard):
        os.mkdir(FILE.keyboard)
    if not os.path.isdir(FILE.files):
        os.mkdir(FILE.files)
    if not os.path.exists(FILE.levels):
        fileWrite(FILE.levels, {
        # 20 40 60
        # ml
        "ml.00":["0","1000","0","True"],
        "ml.01":["0","1000","0","False"],
        "ml.02":["0","1000","0","False"],
        # mr / m(l+r)
        "mr.00":["0","1000","0","True"],
        "mr.01":["0","1000","0","False"],
        "mr.02":["0","1000","0","False"],
        "mr.03":["0","1000","0","False"],
        "mr.04":["0","1000","0","False"],
        "mr.05":["0","1000","0","False"],
        # ul / u(l+r)      / u(l+r) + m(l+r)
        "ul.00":["0","1000","0","True"],
        "ul.01":["0","1000","0","False"],
        "ul.02":["0","1000","0","False"],
        "ul.03":["0","1000","0","False"],
        "ul.04":["0","1000","0","False"],
        "ul.05":["0","1000","0","False"],
        # ur / ur + m(l+r)
        "ur.00":["0","1000","0","True"],
        "ur.01":["0","1000","0","False"],
        "ur.02":["0","1000","0","False"],
        "ur.03":["0","1000","0","False"],
        "ur.04":["0","1000","0","False"],
        "ur.05":["0","1000","0","False"],
        "ur.06":["0","1000","0","False"],
        "ur.07":["0","1000","0","False"],
        "ur.08":["0","1000","0","False"],
        # dl / dl + m(l+r) / dl + all
        "dl.00":["0","1000","0","True"],
        "dl.01":["0","1000","0","False"],
        "dl.02":["0","1000","0","False"],
        "dl.03":["0","1000","0","False"],
        "dl.04":["0","1000","0","False"],
        "dl.05":["0","1000","0","False"],
        "dl.06":["0","1000","0","False"],
        "dl.07":["0","1000","0","False"],
        "dl.08":["0","1000","0","False"],
        # dr / d(l+r)      / d(l+r) + m(l+r) / all
        "dr.00":["0","1000","0","True"],
        "dr.01":["0","1000","0","False"],
        "dr.02":["0","1000","0","False"],
        "dr.03":["0","1000","0","False"],
        "dr.04":["0","1000","0","False"],
        "dr.05":["0","1000","0","False"],
        "dr.06":["0","1000","0","False"],
        "dr.07":["0","1000","0","False"],
        "dr.08":["0","1000","0","False"],
        "dr.09":["0","1000","0","False"],
        "dr.10":["0","1000","0","False"],
        "dr.11":["0","1000","0","False"],
        # nl / nl + all
        "nl.00":["0","1000","0","True"],
        "nl.01":["0","1000","0","False"],
        "nl.02":["0","1000","0","False"],
        "nl.03":["0","1000","0","False"],
        "nl.04":["0","1000","0","False"],
        "nl.05":["0","1000","0","False"],
        # nr / n(r+l) / n(l+r) + all
        "nr.00":["0","1000","0","True"],
        "nr.01":["0","1000","0","False"],
        "nr.02":["0","1000","0","False"],
        "nr.03":["0","1000","0","False"],
        "nr.04":["0","1000","0","False"],
        "nr.05":["0","1000","0","False"],
        "nr.06":["0","1000","0","False"],
        "nr.07":["0","1000","0","False"],
        "nr.08":["0","1000","0","False"],
        # M  / M + all / M + alln
        "MM.00":["0","1000","0","False"],
        "MM.01":["0","1000","0","False"],
        "MM.02":["0","1000","0","False"],
        "MM.03":["0","1000","0","False"],
        "MM.04":["0","1000","0","False"],
        "MM.05":["0","1000","0","False"],
        "MM.06":["0","1000","0","False"],
        "MM.07":["0","1000","0","False"],
        "MM.08":["0","1000","0","False"],
        # U / U + M / U + M + all / U + M + alln
        "UU.00":["0","1000","0","False"],
        "UU.01":["0","1000","0","False"],
        "UU.02":["0","1000","0","False"],
        "UU.03":["0","1000","0","False"],
        "UU.04":["0","1000","0","False"],
        "UU.05":["0","1000","0","False"],
        "UU.06":["0","1000","0","False"],
        "UU.07":["0","1000","0","False"],
        "UU.08":["0","1000","0","False"],
        "UU.09":["0","1000","0","False"],
        "UU.10":["0","1000","0","False"],
        "UU.11":["0","1000","0","False"],
        # D / D + M / U + M + D + all / U + M + alln
        "DD.00":["0","1000","0","False"],
        "DD.01":["0","1000","0","False"],
        "DD.02":["0","1000","0","False"],
        "DD.03":["0","1000","0","False"],
        "DD.04":["0","1000","0","False"],
        "DD.05":["0","1000","0","False"],
        "DD.06":["0","1000","0","False"],
        "DD.07":["0","1000","0","False"],
        "DD.08":["0","1000","0","False"],
        "DD.09":["0","1000","0","False"],
        "DD.10":["0","1000","0","False"],
        "DD.11":["0","1000","0","False"],
        # N / N + ALL / N + all+ ALL / N + ALL + alln
        "NN.00":["0","1000","0","False"],
        "NN.01":["0","1000","0","False"],
        "NN.02":["0","1000","0","False"],
        "NN.03":["0","1000","0","False"],
        "NN.04":["0","1000","0","False"],
        "NN.05":["0","1000","0","False"],
        "NN.06":["0","1000","0","False"],
        "NN.07":["0","1000","0","False"],
        "NN.08":["0","1000","0","False"],
        "NN.09":["0","1000","0","False"],
        "NN.10":["0","1000","0","False"],
        "NN.11":["0","1000","0","False"],
        # ALL
        "AA.00":["0","1000","0","True"],
        "AA.01":["0","1000","0","False"],
        "AA.02":["0","1000","0","False"],
        "AA.03":["0","1000","0","False"],
        "AA.04":["0","1000","0","False"],
        "AA.05":["0","1000","0","False"]
        })
    if not os.path.exists(FILE.stats):
        fileWrite(FILE.stats, {
        "selected_keyboard":["NOT_GIVEN"],
        "selected_file    ":["NOT_GIVEN"],
        "levels_completed ":["0"],
        "correctness      ":["0"],
        "average_time     ":["0"],
        "WPM              ":["0"]
        })
    # TODO attempts level x
    # check for given filename as parameter
    if len(sys.argv) > 1:
        filename   = sys.argv[1]
        basename   = os.path.basename(filename)
        FILE.input = os.path.join(FILE.files, basename)
        shutil.copyfile(filename, FILE.input)
    else:
        basename = "NOT_GIVEN"
    # store new given filename
    stats  = {}
    fileRead(FILE.stats,stats)
    stats["selected_file    "] = [basename]
    fileWrite(FILE.stats,stats)
    # check for selected keyboard
    FILE.layout = os.path.join(FILE.keyboard,stats["selected_keyboard"][0])

# init the env
init()

# call main loop
main()
