#!/usr/bin/env python

"""
handcompare - application for comparing poker hands
Jake Billo <jake@jakebillo.com>
"""

import card
import hand

# define custom exception classes
class MissingArgumentError(Exception):
    pass

class InvalidHandError(Exception):
    pass

class HandCompare():

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

    HAND_RANKS = [
        "royal_flush",
        "straight_flush",
        "four_of_a_kind",
        "full_house",
        "flush",
        "straight",
        "three_of_a_kind",
        "two_pair",
        "pair",
        "high_card",
    ]

    def check_argcount(self, system_args):
        # if the number of arguments < 3, raise exception
        # this includes application executable, hand1, hand2
        if not system_args or len(system_args) < 3:
            raise MissingArgumentError("Provide at least two hands to compare")

        return True

    def parse_hand_string(self, hand_string):
        if not hand_string or not hand_string.strip():
            raise InvalidHandError("Specified hand was None or empty")

        if hand_string.count(",") != 4:
            raise InvalidHandError("Hand did not contain enough comma-separated cards")

        # FIXME check if we can split this and the resulting list has enough elements



        return [1,2,3,4,5]

    def map_card_value(self, card):
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

    def check_card_suit(self, suit):
        return suit in self.SUITS

    def start(self):
        pass



if __name__ == '__main__':
    hc = HandCompare()
    hc.start()
