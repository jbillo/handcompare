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
    CARDS_IN_HAND = 5

    def check_argcount(self, system_args):
        # if the number of arguments < 3, raise exception
        # this includes application executable, hand1, hand2
        if not system_args or len(system_args) < 3:
            raise MissingArgumentError("Provide at least two hands to compare")

        return True

    def parse_card_string(self, card_string):
        # check if string is None
        if not card_string or not card_string.strip():
            raise card.InvalidCardError("Specified card was None or empty")

        # try parsing provided string as a card
        # enforce maximum length of two digits and one letter and min length of 2 chars
        if len(card_string) < 2 or len(card_string) > 3:
            raise card.InvalidCardError("Specified card was too short or long")

        # split card out into digit(s) and suits
        if len(card_string) == 2:
            card_value = card_string[0:1]   # length 1
        else:
            card_value = card_string[0:2]   # length 2

        # suit defined as last character
        card_suit = card_string[-1]

        # create the object/return it, which will raise exceptions as necessary
        return card.Card(card_value, card_suit)


    def parse_hand_string(self, hand_string):
        if not hand_string or not hand_string.strip():
            raise InvalidHandError("Specified hand was None or empty")

        if hand_string.count(",") != (self.CARDS_IN_HAND - 1):
            raise InvalidHandError("Hand did not contain correct number of  comma-separated cards")

        # check if we can split this and the resulting list has enough elements
        split_cards = hand_string.split(",")
        if len(split_cards) != self.CARDS_IN_HAND:
            raise InvalidHandError("Resulting split hand did not contain correct number of cards: {0}".format(len(split_cards)))

        # create Hand object and populate it with cards; this will throw exceptions
        # on any invalid conditions (duplicate cards, etc)
        create_hand = hand.Hand()
        for card_string in split_cards:
            create_hand.add_card(self.parse_card_string(card_string))

        return create_hand

    def hand_sanity(self, hand1, hand2):
        # check that hands do not contain the same cards
        # the hand itself ensures uniqueness, but compare against each other
        h1_cards = hand1.get_cards()
        h2_cards = hand2.get_cards()

        # use __eq__ method to check card equality
        for card in h1_cards:
            for comp_card in h2_cards:
                if card == comp_card:
                    raise InvalidHandError("Same card ({0}) exists in both hands".format(card))

        return True

    def start(self):
        pass



if __name__ == '__main__':
    hc = HandCompare()
    hc.start()
