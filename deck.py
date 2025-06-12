
# Import the Card class and random module for shuffling
from card import Card
import random

# The Deck class represents a standard deck of 52 playing cards.
class Deck:
    def __init__(self):
        # List to hold Card objects
        self.cards = []
        # Build a new deck of 52 cards
        self.build()

    def build(self):
        # Define the four suits and card values (1 = Ace, 13 = King)
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        values = range(1, 14)  # 1 (Ace) to 13 (King)

        # Create one card for each suit and value combination
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        # Shuffle the deck randomly in place
        random.shuffle(self.cards)

    def deal(self):
        # Deal (remove and return) the top card from the deck, if any remain
        if len(self.cards) > 0:
            return self.cards.pop()
        # If the deck is empty, return None
        return None