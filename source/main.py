# Main loop

import os
from getkey import getkey, keys # TODO replace with from sshkeyboard import listen_keyboard

from utils import *
from display_terminal import *
from setup import *
from select_keyboard import *
from learn import *
from stats import *


class FILES:
    home      = ""  # user home folder
    main      = ""  # hidden folder containing data

    levels    = ""  # levels information

    settings  = ""  # file containing all settings
    keyboards = ""  # keyboard layouts folder
    layout    = ""  # selected keyboard layout
    languages = ""  # folder containing all language files
    lang      = ""  # selected language

    stats     = ""  # statistics data

    # TEMPORARY
    keyboard = ""
    files = ""

# submenu for selecting files
def fileInput():
    """File input selecting function, allows to select levels"""
    # loop initialisation
    names_list = list(map(os.path.basename, os.listdir(FILES.files)))
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
            FILES.input = os.path.join(FILES.files, basename)
            stats = {}
            fileRead(FILES.stats,stats)
            stats["selected_file    "] = [basename]
            fileWrite(FILES.stats,stats)
            trainFile(FILES.input)
            break
        elif key == keys.ESCAPE:
            break

# submenu for keyboards
def keyboards(FILES):
	"""Keyboard selecting function, allows to select keyboards"""
	# loop initialisation
	names_list = ["< NEW KEYBOARD LAYOUT >"]
	names_list += list(map(os.path.basename, os.listdir(FILES.keyboard)))
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
				setKeyboard(FILES)
				break
			else:
				# SET from old keyboard
				basename = print_data[(6-cursor)%7]
				FILES.layout = os.path.join(FILES.keyboard, basename)
				stats = {}
				fileRead(FILES.stats,stats)
				stats["selected_keyboard"] = [basename]
				fileWrite(FILES.stats,stats)
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
		fileRead(FILES.levels, dict)
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
			fileRead(FILES.stats, dict)
			if dict["selected_keyboard"][0] == "NOT_GIVEN":
				keyboards()
			# run training level
			dict = {}
			fileRead(FILES.levels, dict)
			level = print_data[(4-cursor)%5].split("\t")[0]
			if (dict[level][3]=="False"):
				print("\x1b[0K"+"You haven't unlocked this level yet!", end = "", flush = True)
			else:
				print("\x1b[0K", end = "", flush = True)
				train(FILES,level)
			# update levels
			updateUnlocked(FILES)
			updateStats(FILES)
			# move cursor to next level
			if cursor == 0:
				offset = (offset + 1)%lines_length
			else:
				cursor -= 1
		elif key == keys.ESCAPE:
			break

# returns data for menu
def toMdata():
    # get stats for main function
    stats = {}
    fileRead(FILES.stats,stats)
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
                stats(FILES)
            # case file
            if cursor == 1:
                fileInput()
            # case levels
            if cursor == 2:
                levels()
            # case key layout
            if cursor == 3:
                keyboards(FILES)
        elif key == keys.ESCAPE:
            break
        # exit condition

# Initialize the user environment
setup(FILES)

# call main loop
main()
