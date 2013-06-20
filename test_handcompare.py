#!/usr/bin/env python

"""
test_handcompare
"""

import unittest
import handcompare
import card
import hand

import sys

class TestHandCompare(unittest.TestCase):

    def setUp(self):
        self.hc = handcompare.HandCompare()
        self.hand = hand.Hand()

    def tearDown(self):
        del self.hc
        del self.hand

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

        # check for a legitimate hand and list response
        result = self.hc.parse_hand_string("2C,3H,4D,5C,6H")
        self.assertEqual(len(result), 5)

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
        ]

        for invalid_card in invalid_cards:
            self.assertRaises(handcompare.InvalidCardError, self.hc.parse_card_string, invalid_card)

        valid_cards = ["2H", "10C", "JC", "QD", "KH", "AS"]
        for valid_card in valid_cards:
            self.assertTrue(self.hc.parse_card_string(valid_card))


class TestCardValue(unittest.TestCase):
    def setUp(self):
        self.hc = handcompare.HandCompare()

    def tearDown(self):
        del self.hc

    def test_map_card_value(self):
        # check for known card values so jack through ace are treated properly
        known_values = [
            ["J", 11],
            ["Q", 12],
            ["K", 13],
            ["A", 14],
        ]

        for check_value in known_values:
            self.assertEqual(self.hc.map_card_value(check_value[0]), check_value[1])

        # check that invalid cards don't get a value and have an exception thrown
        for invalid_value in ["X", 1, -1, 0, -50, "", None]:
            self.assertRaises(ValueError, self.hc.map_card_value, invalid_value)

    def test_check_card_suit(self):
        # check for known suit values
        for valid_suit in ["C", "D", "H", "S"]:
            self.assertTrue(self.hc.check_card_suit(valid_suit))

        # check for unknown suit values
        for invalid_suit in ["X", " ", "", 0, None]:
            self.assertFalse(self.hc.check_card_suit(invalid_suit))


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = hand.Hand()

    def tearDown(self):
        del self.hand

    def test_add_card(self):
        # try adding a non-card object
        self.assertRaises(ValueError, self.hand.add_card, "2C")

        # try adding a valid card
        valid_card = card.Card(2, "C")
        self.assertTrue(self.hand.add_card(valid_card))

if __name__ == '__main__':
    unittest.main()

