# ----------------------------------------------------------------
# This file contains all functions to setup the environment for 
# the program to run correctly
# ----------------------------------------------------------------

import os
import sys
import shutil

from utils import *

def setup(FILES):
    """Function called to initialize all directories and check existence of folders/files."""
    """Returns home folder, paths and filenames"""

    # Get the path of folder and files
    FILES.home      = os.path.expanduser("~")
    FILES.main      = os.path.join(FILES.home, ".keyTouch")

    FILES.levels    = os.path.join(FILES.main, "levels.json")

    FILES.settings  = os.path.join(FILES.main, "settings.json")
    FILES.keyboards = os.path.join(FILES.main, "keyboards")
    FILES.languages = os.path.join(FILES.main, "languages")

    FILES.stats     = os.path.join(FILES.main, "stats.txt")

    # check if folder/files exists
    if not os.path.isdir(FILES.main):
        os.mkdir(FILES.main)
    if not os.path.isdir(FILES.keyboards):
        os.mkdir(FILES.keyboards)
    if not os.path.isdir(FILES.languages):
        os.mkdir(FILES.languages)

    # check if subfiles existing otherways alert user
    if not os.path.exists(FILES.settings):
        # TODO fix this
        print("NO SETTINGS AVAILABLE PLEASE REINSTALL PROGRAM")
    # TODO read settings and check if all files exist
    # TODO if empty keyboard or language make user select 
    # TODO if no keyboard or language available make reinstall

    # TODO TEMPORARY
    FILES.keyboard = os.path.join(FILES.main,"keyboard")
    FILES.files    = os.path.join(FILES.main,"files")
        # check if subfiles existing otherways create them
    if not os.path.isdir(FILES.keyboard):
        os.mkdir(FILES.keyboard)
    if not os.path.isdir(FILES.files):
        os.mkdir(FILES.files)
    if not os.path.exists(FILES.levels):
        fileWrite(FILES.levels, {
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
    if not os.path.exists(FILES.stats):
        fileWrite(FILES.stats, {
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
        FILES.input = os.path.join(FILES.files, basename)
        shutil.copyfile(filename, FILES.input)
    else:
        basename = "NOT_GIVEN"
    # store new given filename
    stats  = {}
    fileRead(FILES.stats,stats)
    stats["selected_file    "] = [basename]
    fileWrite(FILES.stats,stats)
    # check for selected keyboard
    FILES.layout = os.path.join(FILES.keyboard,stats["selected_keyboard"][0])