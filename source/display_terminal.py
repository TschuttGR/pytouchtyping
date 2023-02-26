# ----------------------------------------------------------------
# Contains only functions to display in the terminal
# ----------------------------------------------------------------

import os
import time # temporary

from utils import *
from ansi import * # TODO remove ansi dependency

# returns the maximum line size in function of terminal width
def max_line_length():
    return max(os.get_terminal_size().columns-16,64)

# returns the maximum line numbers in function of terminal height
def max_line_length():
    return max(os.get_terminal_size().lines-4,20)

# general pretty print for terminal
def display(
    title="HELLO WORLD", 
    lines = [],
    cursor=-1
    ):
    """Cursor: position of cursor from top to bottom, -1 = no cursor"""
    """Title is centered"""
    """Data is an array of lines, OF CORRECT SIZE"""
    print('\033[?25l', end="") # hide cursor
    len_title = len(title)
    len_lines = len(lines)
    rows = os.get_terminal_size().lines
    cols = os.get_terminal_size().columns

    # move cursor up
    print("\033["+str(rows)+"A",end="")
    print("\033["+str(cols)+"D",end="")
    for i in range(rows-1):
        print(" "*cols)
    # Print title
    offset = (cols - len_title)//2
    print("\033["+str(rows-2)+"A",end="")
    print("\033["+str(offset)+"C"+title)
    print("")
    # print remaing lines
    for i in range(len_lines):
        offset = "     >  "
        if i != cursor:
            offset = " "*8
        print(offset+lines[i])

    print("\033["+str(rows)+"A",end="")
    print("\033["+str(cols)+"D",end="")

display("TITLE",["Some","random","text."],0)
time.sleep(5)

# ----------------------------------------------------------------
# From here on comes the crap

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
		line += ANSI.RESET
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
