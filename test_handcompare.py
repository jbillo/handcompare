#!/usr/bin/env python

"""
test_handcompare
"""

import unittest
import handcompare

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

if __name__ == '__main__':
    unittest.main()

