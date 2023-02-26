# Contains all functions to display in the terminal
# Objective: adabtive window size with minimal 24x80.

from utils import *
from ansi import *

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
