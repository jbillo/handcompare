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

class InvalidCardError(Exception):
    pass

class HandCompare():
    CARDS_IN_HAND = 5

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

    def parse_card_string(self, card_string):
        # check if string is None
        if not card_string or not card_string.strip():
            raise InvalidCardError("Specified card was None or empty")

        # try parsing provided string as a card
        # enforce maximum length of two digits and one letter and min length of 2 chars
        if len(card_string) < 2 or len(card_string) > 3:
            raise InvalidCardError("Specified card was too short or long")

        # split card out into digit(s) and suits
        if len(card_string) == 2:
            card_value = card_string[0:1]   # length 1
        else:
            card_value = card_string[0:2]   # length 2

        # suit defined as last character
        card_suit = card_string[-1]

        # try to map card value with appropriate table
        try:
            card_value = self.map_card_value(card_value)
        except ValueError:
            # raise custom exception
            raise InvalidCardError("Value of card could not be parsed")

        if not self.check_card_suit(card_suit):
            raise InvalidCardError("Value of suit could not be parsed")

        create_card = card.Card(card_value, card_suit)

        print "%s%s" % (create_card.get_value(), create_card.get_suit())

        return create_card


    def parse_hand_string(self, hand_string):
        if not hand_string or not hand_string.strip():
            raise InvalidHandError("Specified hand was None or empty")

        if hand_string.count(",") != (self.CARDS_IN_HAND - 1):
            raise InvalidHandError("Hand did not contain correct number of  comma-separated cards")

        # check if we can split this and the resulting list has enough elements
        split_cards = hand_string.split(",")
        if len(split_cards) != self.CARDS_IN_HAND:
            raise InvalidHandError("Resulting split hand did not contain correct number of cards: {0}".format(len(split_cards)))

        # create Hand object and populate it with cards
        create_hand = hand.Hand()
        for card_string in split_cards:
            create_hand.add_card(self.parse_card_string(card_string))

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
