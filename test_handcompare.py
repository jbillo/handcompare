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
        ]

        for invalid_card in invalid_cards:
            self.assertRaises(card.InvalidCardError, self.hc.parse_card_string, invalid_card)

        valid_cards = ["2H", "10C", "JC", "QD", "KH", "AS"]
        for valid_card in valid_cards:
            self.assertTrue(self.hc.parse_card_string(valid_card))


class TestCardValue(unittest.TestCase):
    def setUp(self):
        self.hc = handcompare.HandCompare()
        self.card = card.Card(2, "C")

    def tearDown(self):
        del self.hc
        del self.card

    def test_map_card_value(self):
        # check for known card values so jack through ace are treated properly
        known_values = [
            ["J", 11],
            ["Q", 12],
            ["K", 13],
            ["A", 14],
        ]

        for check_value in known_values:
            self.assertEqual(self.card._map_card_value(check_value[0]), check_value[1])

        # check that invalid cards don't get a value and have an exception thrown
        for invalid_value in ["X", 1, -1, 0, -50, "", None]:
            self.assertRaises(ValueError, self.card._map_card_value, invalid_value)

    def test_check_card_suit(self):
        # check for known suit values
        for valid_suit in ["C", "D", "H", "S"]:
            self.assertTrue(self.card._check_card_suit(valid_suit))

        # check for unknown suit values
        for invalid_suit in ["X", " ", "", 0, None]:
            self.assertFalse(self.card._check_card_suit(invalid_suit))


class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = hand.Hand()

    def tearDown(self):
        del self.hand

    def test_clear(self):
        # ensure there are no cards in the hand after a clear operation
        self.hand.clear()
        self.assertEqual(len(self.hand.get_cards()), 0)

    def test_clear_sort(self):
        # check that the sort function returns false after a clear operation
        self.hand.clear()
        self.assertFalse(self.hand.sort_cards())

    def test_sort_cards(self):
        # check that the sort function returns true when one or more cards are in hand
        self.hand.clear()
        self.hand.add_card(card.Card(3, "H"))
        self.hand.add_card(card.Card(2, "C"))

        # while cards should already be sorted at this point, make sure result is true
        self.assertTrue(self.hand.sort_cards())

        # check that the sorting actually worked: compare card values/suits
        # can't compare objects directly since they are technically not the same object
        # possible improvement: comparator function
        test_hand = self.hand.get_cards()
        proper_sort = [card.Card(2, "C"), card.Card(3, "H")]

        self.assertEqual(test_hand[0].get_value(), proper_sort[0].get_value())
        self.assertEqual(test_hand[0].get_suit(), proper_sort[0].get_suit())
        self.assertEqual(test_hand[1].get_value(), proper_sort[1].get_value())
        self.assertEqual(test_hand[1].get_suit(), proper_sort[1].get_suit())

    def test_add_card(self):
        # try adding a non-card object
        self.assertRaises(ValueError, self.hand.add_card, "2C")

        # try adding a valid card
        valid_card = card.Card(2, "C")
        self.assertTrue(self.hand.add_card(valid_card))

        # try adding an invalid card
        #try:
        #invalid_card = card.Card(15, "C")
        #self.assertRaises(self.card.InvalidCardError, self.hand.add_card, invalid_card)

    def test_hand_type(self):
        # try with no cards and 1 card
        self.hand.clear()
        self.assertRaises(hand.MissingCardError, self.hand.get_hand_type)

    def test_straight_flush(self):
        self.hand.clear()

        # check that no cards create a straight flush
        self.assertFalse(self.hand.check_straight_flush())

if __name__ == '__main__':
    unittest.main()

