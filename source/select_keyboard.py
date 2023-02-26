
import os


from utils import *
from display_terminal import *

# sets the keyboard from user input
def setKeyboard(FILES):
	message = ["",
		"    What name should your new keyboard layout have?",
		"    By reusing an existing filename you overwrite it.",
		"    Write and press <enter>"]
	xprint(message, 8)
	# set the keyboard
	basename = input("")+".txt"
	FILES.layout = os.path.join(FILES.keyboard, basename)
	stats = {}
	fileRead(FILES.stats,stats)
	stats["selected_keyboard"] = [basename]
	fileWrite(FILES.stats,stats)

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

	fileWrite(FILES.layout, dict)

	message = ["",
		"    Done.",
		"    Press <enter> to finish."]
	xprint(message, 8)
	input("\x1b[0K")