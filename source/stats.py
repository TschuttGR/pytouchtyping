# ----------------------------------------------------------------
# Contains only functions in relation with statistics
# ----------------------------------------------------------------

# submenu for  stats

from utils import *
from display_terminal import *

from getkey import getkey, keys # TODO replace with from sshkeyboard import listen_keyboard


def stats(FILES):
    """File input selecting function, allows to wiev statistics"""
    # loop initialisation
    dict = {}
    fileRead(FILES.stats, dict)
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
        
