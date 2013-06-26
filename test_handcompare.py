#!/usr/bin/env python

"""
test_handcompare

Unit testing module for the poker hand comparison application

Jake Billo <jake@jakebillo.com>
"""

import unittest
import handcompare
import card
import hand

# Specifically import other test cases and inside classes
from test_cardvalue import *
from test_hand import *

import sys

class TestHandCompare(unittest.TestCase):
    def setUp(self):
        self.hc = handcompare.HandCompare()
        self.hand = hand.Hand()
        self.card = card.Card(2, "C")

    def tearDown(self):
        del self.hc
        del self.hand
        del self.card

    def test_check_argcount(self):
        # check argument count for 0, 1 and 2 parameters
        basic_pass = ["app_name", "hand1", "hand2"]

        # for sys.argv is None, the function should fail preemptively
        self.assertRaises(TypeError, self.hc.check_argcount)

        # pass lists of 1 and 2 length
        self.assertRaises(handcompare.MissingArgumentError, self.hc.check_argcount, [0])
        self.assertRaises(
                          handcompare.MissingArgumentError,
                          self.hc.check_argcount,
                          [0, 1]
                          )

        # with valid parameters, ensure function returns properly
        self.assertTrue(self.hc.check_argcount(basic_pass))

    def test_parse_hand_string(self):
        # ensure that the hands are valid strings with appropriate content:

        # check for None and empty string cases,
        # padded strings that compress down to nothing
        # and strings that don't contain enough commas (== 4)

        for invalid_hand in [None, "", "    ", ",,,"]:
            self.assertRaises(handcompare.InvalidHandError, self.hc.parse_hand_string,
                              invalid_hand)

        # check for a legitimate hand object
        result = self.hc.parse_hand_string("2C,3H,4D,5C,6H")
        self.assertIsInstance(result, hand.Hand)

    def test_parse_card_string(self):
        # ensure the card is a valid string with appropriate content
        invalid_cards = [
            None,
            "",
            " ",
            "0H",
            "000H",
            "0X",
            "000X",
            "1H",
            "1 H",
            "1X",
            "11H",
            "12X",
            "99H",
            "99X",
            "100H",
            "100X",
            "--",
            "0-",
        ]

        for invalid_card in invalid_cards:
            self.assertRaises(card.InvalidCardError, self.hc.parse_card_string, invalid_card)

        valid_cards = ["2H", "5S", "10C", "JC", "QD", "KH", "AS"]
        for valid_card in valid_cards:
            self.assertTrue(self.hc.parse_card_string(valid_card))

    def test_hand_sanity(self):
        hand1 = hand.Hand()
        hand2 = hand.Hand()

        # Given two hands, ensure an InvalidHandError is thrown if they contain
        # any of the exact same cards
        for value in range(2, 7):
            hand1.add_card(card.Card(value, "D"))

        hand2.add_card(card.Card(2, "D"))
        # At this point H1 has 2-6 of diamonds and hand2 has 2 of diamonds
        self.assertRaises(handcompare.InvalidHandError, self.hc.hand_sanity, hand1, hand2)

    def load_default_hand(self, hand):
        # Return a Hand object for comparison purposes.
        import default_hands
        return self.hc.parse_hand_string(default_hands.DEFAULT_HANDS[hand])

    def test_hand_compare(self):
        """
        First block of standard hand comparisons. These should not throw exceptions or
        errors, but be an example of when one hand would win out over another.
        """

        # Check equality operators for sampling of hands
        hand1 = self.load_default_hand("royal_flush")
        hand2 = self.load_default_hand("royal_flush_2")
        self.assertEqual(hand1, hand2)

        hand1 = self.load_default_hand("straight_flush")
        hand2 = self.load_default_hand("straight_flush_2")
        self.assertEqual(hand1, hand2)

        # Check gt operator for sampling of hands
        # Also test comparisons we know to be false to exercise early exits
        hand1 = self.load_default_hand("royal_flush")
        hand2 = self.load_default_hand("straight_flush")
        self.assertGreater(hand1, hand2)
        self.assertFalse(hand1 < hand2)

        hand1 = self.load_default_hand("four_of_a_kind")
        hand2 = self.load_default_hand("three_of_a_kind")
        self.assertGreater(hand1, hand2)
        self.assertFalse(hand1 < hand2)

        # Check le operator for sampling of hands
        # Also test comparisons we know to be false to exercise early exits
        hand1 = self.load_default_hand("full_house")
        hand2 = self.load_default_hand("four_of_a_kind")
        self.assertLess(hand1, hand2)
        self.assertFalse(hand1 > hand2)

        hand1 = self.load_default_hand("high_card")
        hand2 = self.load_default_hand("pair")
        self.assertLess(hand1, hand2)
        self.assertFalse(hand1 > hand2)

        hand1 = self.load_default_hand("high_card_less")
        hand2 = self.load_default_hand("high_card")
        self.assertLess(hand1, hand2)
        self.assertFalse(hand1 > hand2)


    def test_hand_compare_wikipedia(self):
        # TODO: Use specific testcases from Wikipedia article

        hand1 = self.load_default_hand("wp_straight_flush_1")
        hand2 = self.load_default_hand("wp_straight_flush_2")
        self.assertGreater(hand1, hand2)

        hand1 = self.load_default_hand("wp_straight_flush_3")
        hand2 = self.load_default_hand("wp_straight_flush_4")
        self.assertEqual(hand1, hand2)

        hand1 = self.load_default_hand("wp_four_of_a_kind_1")
        hand2 = self.load_default_hand("wp_four_of_a_kind_2")
        self.assertGreater(hand1, hand2)

        hand1 = self.load_default_hand("wp_four_of_a_kind_3")
        hand2 = self.load_default_hand("wp_four_of_a_kind_4")
        self.assertGreater(hand1, hand2)


if __name__ == '__main__':
    # Empty sys.argv in case this application is accidentally run with hand strings
    # or other arguments specified - Python's unit testing mechanism will attempt to
    # run specific test cases
    sys.argv = [sys.argv[0]]
    unittest.main()

