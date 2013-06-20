class InvalidCardError(Exception):
    pass

class Card():
    SUITS = {
        "H": "hearts",
        "C": "clubs",
        "S": "spades",
        "D": "diamonds",
    }

    LETTER_CARD_VALUES = {
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    value = 0
    suit = ""

    def __repr__(self):
        # For sorting purposes, always use value first and then suit; return a tuple
        return repr((self.value, self.suit))

    def _map_card_value(self, card):
        # check if card is an integer; if not, catch exception and return predefined value
        try:
            card = int(card)
        except (ValueError, TypeError) as e:
            # TypeError occurs when card cannot be converted to integer (None)
            # ValueError occurs when card is letter; try and retrieve it from dict
            try:
                return self.LETTER_CARD_VALUES[card]
            except KeyError:
                raise ValueError("Card value must be between 2 and A")

        # Check if card falls outside range 2-10 (11+ have already been returned)
        if card < 2 or card > 10:
            raise ValueError("Card value must be between 2 and 10 if numeric")

        # Enforce integer on return.
        return card

    def _check_card_suit(self, suit):
        return suit in self.SUITS

    def __init__(self, card_value, card_suit):
        self.value = card_value
        self.suit = card_suit

        # try to map card value with appropriate table
        try:
            self.value = self._map_card_value(self.value)
        except ValueError:
            # raise custom exception
            raise InvalidCardError("Value of card could not be parsed")

        if not self._check_card_suit(self.suit):
            raise InvalidCardError("Value of suit could not be parsed")

    def get_value(self):
        return int(self.value)

    def get_suit(self):
        return self.suit
