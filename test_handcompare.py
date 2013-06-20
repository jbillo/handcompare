#!/usr/bin/env python

"""
test_handcompare
"""

import unittest
import handcompare
import card

import sys

class TestHandCompare(unittest.TestCase):

    def setUp(self):
        self.hc = handcompare.HandCompare()

    def tearDown(self):
        del self.hc

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

        # check for None and empty string cases
        self.assertRaises(handcompare.InvalidHandError, self.hc.parse_hand_string,
                          None)
        self.assertRaises(handcompare.InvalidHandError, self.hc.parse_hand_string,
                          "")

        # check for padded strings that compress down to nothing
        self.assertRaises(handcompare.InvalidHandError, self.hc.parse_hand_string,
                          "     ")

        # check for strings that don't contain enough commas (== 4)
        self.assertRaises(handcompare.InvalidHandError, self.hc.parse_hand_string,
                          ",,,")

        # check for a legitimate hand and list response
        result = self.hc.parse_hand_string("2C,3H,4D,5C,6H")
        self.assertEqual(len(result), 5)


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

if __name__ == '__main__':
    unittest.main()

