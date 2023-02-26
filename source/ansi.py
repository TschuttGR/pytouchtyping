# Constains all colors needed to display in terminal
class ANSI:
    # Reset
    Color_Off='\033[0m'       # Text Reset
    Clear_Line='\033[0K'      # Clear line

    # Cursor moves
    N=0                         # Variable distance 
    Up='\033['+str(N)+'A'       # Up
    Down='\033['+str(N)+'B'     # Down
    Forward='\033['+str(N)+'C'  # Forward
    Backward='\033['+str(N)+'D' # Backward

    # colors
    # text colors with 3 from 0 to 7 KRGYBPCW
    # background colors with 4 from 0 to 7 KRGYBPCW
    # decorators : 0, 1, 4, 7: neutral, bold, underline, reversed
    RESET   = "\033[0;0m"
    NORMAL  = "\033[0;37;40m"
    CORRECT = "\033[0;37;42m"
    WRONG   = "\033[0;37;41m"
    PERFECT = "\033[96m"
    GOOD    = "\033[92m"
    MEDIUM  = "\033[93m"
    BAD     = "\033[91m"