
HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
WARNING = '\033[93m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def printcolor(color, text):
    print(f'{color}{text}{RESET}')