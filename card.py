"""
This script is not directly executable and forms part of the objects for
the handcompare application.
"""

# Card: Represents a single card.


class InvalidCardError(Exception):
    """Thrown when a Card object cannot be parsed or created properly."""
    pass


class Card(object):
    # Suit definitions. Provided as a dict for potential future text output.
    SUITS = {
        "H": "hearts",
        "C": "clubs",
        "S": "spades",
        "D": "diamonds",
    }

    # Assign integer values to Jack through Ace. In this code, Ace is considered high
    # and dealt with specially when considering a A-5 straight.
    LETTER_CARD_VALUES = {
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    # Local properties for card value and suit.
    value = 0
    suit = ""

    def __repr__(self):
        """For sorting purposes, always use value first and then suit; return a tuple"""
        return repr((self.value, self.suit))

    def __eq__(self, other):
        """Equality operator. Check if value and suit match."""
        return (self.value == other.get_value() and self.suit == other.get_suit())

    def _map_card_value(self, card):
        """
        Internal mapping function. Check if card is an integer.
        If not, catch exception and return predefined value.
        Can throw a ValueError if the specified value is not between 2-A.
        """

        try:
            card = int(card)
        except (ValueError, TypeError):
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
        """Internal card suit validation function."""
        return suit in self.SUITS

    def __init__(self, card_value, card_suit):
        """
        Constructor. Set up a new object with specified value and suit.
        Can throw an InvalidCardError if parsing the given value or suit fails.
        """

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
        """Accessor method for card value"""
        return int(self.value)

    def get_suit(self):
        """Accessor method for card suit"""
        return self.suit
