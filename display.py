
def print_win_screen(game=None):
    """
    Print a fancy ASCII art and colored win screen.
    """
    clear_screen()
    art = """
\033[92m
 __     __          __          ___       _ 
 \ \   / /          \ \        / (_)     | |
  \ \_/ /__  _   _   \ \  /\  / / _ _ __ | |
   \   / _ \| | | |   \ \/  \/ / | | '_ \| |
    | | (_) | |_| |    \  /\  /  | | | | |_|
    |_|\___/ \__,_|     \/  \/   |_|_| |_(_)
\033[0m
"""
    print(art)
    print("\033[93mCongratulations! You won Solitaire!\033[0m")
    if game is not None:
        print(f"\033[96mReserve recycled {game.reserve_recycles} time(s).\033[0m")
    print("\nPress Enter to play again or 'q' to quit.")

import re

# Regex to match ANSI escape codes (for colored output)
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')

def pad_ansi(s, width):
    """
    Pad string s to a given width, ignoring ANSI escape codes.
    This ensures columns align even when using colored output.
    """
    real_len = len(ANSI_ESCAPE.sub('', s))
    return s + ' ' * (width - real_len)

# Suit symbols with ANSI color codes for display
suit_symbols = {
    'Hearts': '\033[91m♥\033[0m',    # Red heart
    'Diamonds': '\033[91m♦\033[0m',  # Red diamond
    'Spades': '\033[37m♠\033[0m',    # Black spade
    'Clubs': '\033[37m♣\033[0m'      # Black club
}

def clear_screen():
    """
    Clear the terminal screen using an ANSI escape code.
    """
    print("\033c", end="")

def colored_card(card):
    """
    Return a string representation of a card, with color for suits and face-down cards.
    """
    if not card.face_up:
        return "\033[30m[X]\033[0m"  # Gray for face-down
    value_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
    display_value = value_map.get(card.value, str(card.value))
    card_str = f"{display_value}{suit_symbols[card.suit]}"
    if card.suit in ['Hearts', 'Diamonds']:
        return f"[\033[91m{card_str}\033[0m]"  # Red for hearts/diamonds
    else:
        return f"[\033[37m{card_str}\033[0m]"  # White for spades/clubs

def display_game(game):
    """
    Display the current state of the game, including foundations, waste, reserve, and tableau columns.
    """
    clear_screen()
    print("=== SOLITAIRE ===")

    # Display foundations (top card of each suit's pile)
    print("\nFoundations:")
    for suit, foundation in game.foundations.items():
        if foundation:
            print(f"{suit_symbols[suit]}: {colored_card(foundation[-1])}", end=" ")
        else:
            print(f"{suit_symbols[suit]}: [  ]", end=" ")
    print("\n")

    # Display the waste pile (top card of waste)
    print("Waste:", end=" ")
    if game.waste:
        print(colored_card(game.waste[-1]), end=" ")
    else:
        print("[  ]", end=" ")
    print(f"(Remaining: {len(game.reserve)} cards in reserve)\n")

    # Display compact column headers (C1, C2, ...)
    col_width = 6
    print("".join(pad_ansi(f"C{i+1}", col_width) for i in range(7)))

    # Display tableau columns with fixed width, left-aligned
    max_height = max(len(col) for col in game.columns)
    for row in range(max_height):
        for col in range(7):
            if row < len(game.columns[col]):
                card_display = colored_card(game.columns[col][row])
                print(pad_ansi(card_display, col_width), end="")
            else:
                print(" " * col_width, end="")
        print()  # New line after each row

    # Print controls for the user
    print("\nControls:")
    print("d - draw from reserve")
    print("m<source><target> - move between columns (e.g., m13 moves from C1 to C3)")
    print("mw<column> - move from waste to column (e.g., mw3 moves waste to C3)")
    print("f<column> - move to foundation (e.g., f1 moves from C1 to foundation)")
    print("fw - move from waste to foundation")
    print("r - restart game")
    print("q - quit")