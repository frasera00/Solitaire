
# The Card class represents a single playing card with a suit and value.
# It also tracks whether the card is face up or face down.
class Card:
    def __init__(self, suit, value):
        # The suit of the card (e.g., 'Hearts', 'Spades')
        self.suit = suit
        # The value of the card (1 = Ace, 11 = Jack, 12 = Queen, 13 = King)
        self.value = value
        # Whether the card is face up (visible) or face down
        self.face_up = False

    def __str__(self):
        # If the card is face down, show a hidden card symbol
        if not self.face_up:
            return "[X]"

        # Map special values to their display characters (A, J, Q, K)
        value_map = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        display_value = value_map.get(self.value, str(self.value))

        # Use colored suit symbols for display (ANSI escape codes)
        suit_symbols = {
            'Hearts': '\033[91m♥\033[0m',    # Red heart
            'Diamonds': '\033[91m♦\033[0m',  # Red diamond
            'Spades': '\033[30m♠\033[0m',    # Black spade
            'Clubs': '\033[30m♣\033[0m'      # Black club
        }
        # Return the card as a string, e.g., [A♥] or [10♣]
        return f"[{display_value}{suit_symbols[self.suit]}]"

    def color(self):
        # Return the color of the card ('red' or 'black') based on its suit
        if self.suit in ['Hearts', 'Diamonds']:
            return 'red'
        else:
            return 'black'

    def flip(self):
        # Flip the card: if face down, turn face up; if face up, turn face down
        self.face_up = not self.face_up