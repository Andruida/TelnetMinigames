# \u001b[1;4;202;42m

RESET =           "\x1b[0m"
# Special formatting
BOLD =            "\x1b[1m"
DIM =             "\x1b[2m"
ITALICS =         "\x1b[3m"
UNDERLINED =      "\x1b[4m"
BLINK =           "\x1b[5m"
REVERSE =         "\x1b[7m"
HIDDEN =          "\x1b[8m"
STRIKEOUT =       "\x1b[9m"
# Foreground
FG_DEFAULT =      "\x1b[39m"
FG_BLACK =        "\x1b[30m"
FG_RED =          "\x1b[31m"
FG_GREEN =        "\x1b[32m"
FG_YELLOW =       "\x1b[33m"
FG_BLUE =         "\x1b[34m"
FG_MAGENTA =      "\x1b[35m"
FG_CYAN =         "\x1b[36m"
FG_LIGHT_GRAY =   "\x1b[37m"
FG_DARK_GRAY =    "\x1b[90m"
FG_LIGHT_RED =    "\x1b[91m"
FG_LIGHT_GREEN =  "\x1b[92m"
FG_LIGHT_YELLOW = "\x1b[93m"
FG_LIGHT_BLUE =   "\x1b[94m"
FG_LIGHT_MAGENTA ="\x1b[95m"
FG_LIGHT_CYAN =   "\x1b[96m"
FG_WHITE =        "\x1b[97m"
# Background
BG_DEFAULT =      "\x1b[49m"
BG_BLACK =        "\x1b[40m"
BG_RED =          "\x1b[41m"
BG_GREEN =        "\x1b[42m"
BG_YELLOW =       "\x1b[43m"
BG_BLUE =         "\x1b[44m"
BG_MAGENTA =      "\x1b[45m"
BG_CYAN =         "\x1b[46m"
BG_LIGHT_GRAY =   "\x1b[47m"
BG_DARK_GRAY =    "\x1b[100m"
BG_LIGHT_RED =    "\x1b[101m"
BG_LIGHT_GREEN =  "\x1b[102m"
BG_LIGHT_YELLOW = "\x1b[103m"
BG_LIGHT_BLUE =   "\x1b[104m"
BG_LIGHT_MAGENTA ="\x1b[105m"
BG_LIGHT_CYAN =   "\x1b[106m"
BG_WHITE =        "\x1b[107m"

if __name__ == '__main__':
    text = """

BOLD =              \x1b[1mSome text here\x1b[0m
DIM =               \x1b[2mSome text here\x1b[0m
ITALICS =           \x1b[3mSome text here\x1b[0m
UNDERLINED =        \x1b[4mSome text here\x1b[0m
BLINK =             \x1b[5mSome text here\x1b[0m
REVERSE =           \x1b[7mSome text here\x1b[0m
HIDDEN =            \x1b[8mSome text here\x1b[0m
STRIKEOUT =         \x1b[9mSome text here\x1b[0m

FG_DEFAULT =        \x1b[39mSome text here\x1b[0m
FG_BLACK =          \x1b[30mSome text here\x1b[0m
FG_RED =            \x1b[31mSome text here\x1b[0m
FG_GREEN =          \x1b[32mSome text here\x1b[0m
FG_YELLOW =         \x1b[33mSome text here\x1b[0m
FG_BLUE =           \x1b[34mSome text here\x1b[0m
FG_MAGENTA =        \x1b[35mSome text here\x1b[0m
FG_CYAN =           \x1b[36mSome text here\x1b[0m
FG_LIGHT_GRAY =     \x1b[37mSome text here\x1b[0m
FG_DARK_GRAY =      \x1b[90mSome text here\x1b[0m
FG_LIGHT_RED =      \x1b[91mSome text here\x1b[0m
FG_LIGHT_GREEN =    \x1b[92mSome text here\x1b[0m
FG_LIGHT_YELLOW =   \x1b[93mSome text here\x1b[0m
FG_LIGHT_BLUE =     \x1b[94mSome text here\x1b[0m
FG_LIGHT_MAGENTA =  \x1b[95mSome text here\x1b[0m
FG_LIGHT_CYAN =     \x1b[96mSome text here\x1b[0m
FG_WHITE =          \x1b[97mSome text here\x1b[0m

BG_DEFAULT =        \x1b[49mSome text here\x1b[0m
BG_BLACK =          \x1b[40mSome text here\x1b[0m
BG_RED =            \x1b[41mSome text here\x1b[0m
BG_GREEN =          \x1b[42mSome text here\x1b[0m
BG_YELLOW =         \x1b[43mSome text here\x1b[0m
BG_BLUE =           \x1b[44mSome text here\x1b[0m
BG_MAGENTA =        \x1b[45mSome text here\x1b[0m
BG_CYAN =           \x1b[46mSome text here\x1b[0m
BG_LIGHT_GRAY =     \x1b[47mSome text here\x1b[0m
BG_DARK_GRAY =      \x1b[100mSome text here\x1b[0m
BG_LIGHT_RED =      \x1b[101mSome text here\x1b[0m
BG_LIGHT_GREEN =    \x1b[102mSome text here\x1b[0m
BG_LIGHT_YELLOW =   \x1b[103mSome text here\x1b[0m
BG_LIGHT_BLUE =     \x1b[104mSome text here\x1b[0m
BG_LIGHT_MAGENTA =  \x1b[105mSome text here\x1b[0m
BG_LIGHT_CYAN =     \x1b[106mSome text here\x1b[0m
BG_WHITE =          \x1b[107mSome text here\x1b[0m
"""
    print(text)
