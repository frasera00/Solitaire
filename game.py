from deck import Deck

class SolitaireGame:
    """
    The SolitaireGame class contains all the logic and state for a game of Solitaire.
    It manages the deck, tableau columns, foundations, reserve (stock), and waste piles.
    """

    def __init__(self):
        # Create and shuffle a new deck
        self.deck = Deck()
        self.deck.shuffle()
        # Set up 7 tableau columns (where cards are played)
        self.columns = [[] for _ in range(7)]
        # Set up 4 foundations (one for each suit)
        self.foundations = {suit: [] for suit in ['Hearts', 'Diamonds', 'Spades', 'Clubs']}
        # The reserve (stock) pile and waste (face-up discard)
        self.reserve = []
        self.waste = []
        # Counter for how many times the reserve has been recycled
        self.reserve_recycles = 0
        # Deal cards to columns and reserve
        self.setup_columns()
        self.setup_reserve()
    
    def setup_columns(self):
        """
        Deal cards to columns according to solitaire rules:
        Column 1 gets 1 card, column 2 gets 2, ..., column 7 gets 7 cards.
        Only the top card in each column is face up.
        """
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.deal()
                if card is not None:
                    if j == i:  # Last card in column is face up
                        card.flip()
                    self.columns[i].append(card)
    
    def setup_reserve(self):
        """
        All remaining cards after dealing columns go to the reserve (stock) pile.
        """
        while len(self.deck.cards) > 0:
            card = self.deck.deal()
            if card is not None:
                self.reserve.append(card)
    
    def draw_from_reserve(self):
        """
        Draw a card from the reserve (stock) to the waste pile.
        If the reserve is empty, recycle the waste pile back into the reserve.
        """
        if len(self.reserve) == 0:
            if len(self.waste) == 0:
                # No cards left to draw
                return
            # Recycle waste back to reserve and increment counter
            self.reserve = self.waste[::-1]
            self.waste = []
            for card in self.reserve:
                card.face_up = False
            self.reserve_recycles += 1
        if len(self.reserve) > 0:
            card = self.reserve.pop()
            card.flip()
            self.waste.append(card)
    
    def can_move_to_column(self, card, target_column):
        """
        Check if a card can be moved to a tableau column.
        Only Kings can be placed in empty columns. Otherwise, the card must be one less in value and of opposite color to the top card in the target column.
        """
        if not target_column:
            return card.value == 13  # Only Kings can be placed in empty columns
        top_card = target_column[-1]
        return (card.color() != top_card.color() and 
                card.value == top_card.value - 1)
    
    def can_move_to_foundation(self, card):
        """
        Check if a card can be moved to its foundation pile.
        An Ace can be placed on an empty foundation. Otherwise, the card must be one higher than the top card of the same suit.
        """
        foundation = self.foundations[card.suit]
        if card.value == 1:  # Ace
            return not foundation
        elif foundation:
            return card.value == foundation[-1].value + 1
        return False
    
    def move_card(self, source, destination):
        # Placeholder for a more general move method (not used in this implementation)
        pass

    def move_waste_to_column(self, col_idx):
        """
        Move the top card from the waste pile to a tableau column.
        :param col_idx: Index of the target column (0-6)
        :return: True if move was successful, else False
        """
        if not self.waste:
            return False
        if not (0 <= col_idx < 7):
            return False
        card = self.waste[-1]
        target_col = self.columns[col_idx]
        if not target_col:
            if card.value == 13:
                self.waste.pop()
                target_col.append(card)
                card.face_up = True
                return True
            return False
        top_card = target_col[-1]
        if card.color() != top_card.color() and card.value == top_card.value - 1:
            self.waste.pop()
            target_col.append(card)
            card.face_up = True
            return True
        return False
    
    def move_to_foundation(self, source_col):
        """
        Move the top card from a tableau column to its foundation pile.
        Only an Ace can be placed on an empty foundation. Otherwise, the card must be one higher than the top card of the same suit.
        :param source_col: Index of source column (0-6)
        :return: True if move was successful
        """
        if not 0 <= source_col < 7:
            return False
        source = self.columns[source_col]
        if not source:
            return False
        card = source[-1]
        if not card.face_up:
            return False
        foundation = self.foundations[card.suit]
        # Check if card can be placed in foundation
        if card.value == 1:  # Ace
            if not foundation:
                foundation.append(source.pop())
                # Flip next card if column isn't empty
                if source and not source[-1].face_up:
                    source[-1].flip()
                return True
        else:
            if foundation and foundation[-1].value == card.value - 1:
                foundation.append(source.pop())
                # Flip next card if column isn't empty
                if source and not source[-1].face_up:
                    source[-1].flip()
                return True
        return False
    
    def move_waste_to_foundation(self):
        """
        Move the top card from the waste pile to its foundation pile.
        Only an Ace can be placed on an empty foundation. Otherwise, the card must be one higher than the top card of the same suit.
        :return: True if move was successful
        """
        if not self.waste:
            return False
        card = self.waste[-1]
        foundation = self.foundations[card.suit]
        if card.value == 1:  # Ace
            if not foundation:
                self.foundations[card.suit].append(self.waste.pop())
                return True
        else:
            if foundation and foundation[-1].value == card.value - 1:
                self.foundations[card.suit].append(self.waste.pop())
                return True
        return False
    
    def move_between_columns(self, source_col, source_index, target_col):
        """
        Move a card or a sequence of cards from one tableau column to another.
        The sequence must be in descending order and alternating colors. Only a King can be moved to an empty column.
        :param source_col: Index of source column (0-6)
        :param source_index: Index of card in source column (0-based)
        :param target_col: Index of target column (0-6)
        :return: True if move was successful
        """
        if not (0 <= source_col < 7 and 0 <= target_col < 7):
            return False
        source = self.columns[source_col]
        target = self.columns[target_col]
        # Check if source index is valid
        if source_index < 0 or source_index >= len(source):
            return False
        # Only face-up cards can be moved
        if not source[source_index].face_up:
            return False
        # Check if moving a valid sequence (descending, alternating colors)
        moving_cards = source[source_index:]
        for i in range(len(moving_cards) - 1):
            current = moving_cards[i]
            next_card = moving_cards[i + 1]
            if (current.color() == next_card.color() or 
                current.value != next_card.value + 1):
                return False
        # Check if the move to target is valid
        if len(target) == 0:
            # Only a King can be placed in an empty column
            if moving_cards[0].value != 13:
                return False
        else:
            top_target = target[-1]
            if (moving_cards[0].color() == top_target.color() or 
                moving_cards[0].value != top_target.value - 1):
                return False
        # Perform the move
        self.columns[target_col].extend(moving_cards)
        self.columns[source_col] = source[:source_index]
        # Flip the next card in the source column if needed
        if len(self.columns[source_col]) > 0:
            last_card = self.columns[source_col][-1]
            if not last_card.face_up:
                last_card.flip()
        return True
    
    def check_win(self):
        """
        Check if the game is won (all four foundations have 13 cards).
        """
        for foundation in self.foundations.values():
            if len(foundation) != 13:
                return False
        return True