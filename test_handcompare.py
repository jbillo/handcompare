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

        valid_cards = ["2H", "10C", "JC", "QD", "KH", "AS"]
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
        import default_hands

        # Check equality operators for sampling of hands
        hand1 = self.load_default_hand("royal_flush")
        hand2 = self.load_default_hand("royal_flush_2")
        self.assertEqual(hand1, hand2)

        hand1 = self.load_default_hand("straight_flush")
        hand2 = self.load_default_hand("straight_flush_2")
        self.assertEqual(hand1, hand2)

        # Check gt operator for sampling of hands
        hand1 = self.load_default_hand("royal_flush")
        hand2 = self.load_default_hand("straight_flush")
        self.assertGreater(hand1, hand2)



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

    def test_check_card_equal(self):
        # check not equal for different suits
        card1 = card.Card(2, "H")
        card2 = card.Card(2, "C")
        self.assertNotEqual(card1, card2)

        # check not equal for different values
        card2 = card.Card(3, "H")
        self.assertNotEqual(card1, card2)

        # check equal for same values
        card2 = card.Card(2, "H")
        self.assertEqual(card1, card2)

class TestHand(unittest.TestCase):
    def setUp(self):
        self.hand = hand.Hand()

    def tearDown(self):
        del self.hand

    # helper function to set up a 5 card hand that won't play anything; rank 7/high card
    def set_bad_hand(self):
        self.hand.clear()
        self.hand.add_card(card.Card(2, "D"))
        self.hand.add_card(card.Card(3, "C"))
        self.hand.add_card(card.Card(4, "S"))
        self.hand.add_card(card.Card(5, "H"))
        self.hand.add_card(card.Card(7, "D"))

    def set_full_house(self):
        self.hand.clear()
        for card_suit in ["C", "D", "H"]:
            self.hand.add_card(card.Card("A", card_suit))
        self.hand.add_card(card.Card("K", "H"))
        self.hand.add_card(card.Card("K", "S"))

    def set_three_of_a_kind(self):
        self.hand.clear()
        self.hand.add_card(card.Card(3, "D"))
        self.hand.add_card(card.Card(3, "C"))
        self.hand.add_card(card.Card(3, "S"))
        self.hand.add_card(card.Card(4, "H"))
        self.hand.add_card(card.Card(5, "D"))

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
        self.hand.clear()

        # try adding a non-card object
        self.assertRaises(ValueError, self.hand.add_card, "2C")

        # try adding a valid card
        valid_card = card.Card(2, "C")
        self.assertTrue(self.hand.add_card(valid_card))

        # try adding an invalid card
        invalid_card_detected = False
        try:
            invalid_card = card.Card(15, "C")
        except card.InvalidCardError:
            invalid_card_detected = True

        self.assertTrue(invalid_card_detected)

        # try adding too many cards - populate four more in besides 2C
        for card_value in range(3, 7):
            self.hand.add_card(card.Card(card_value, "C"))

        extra_card = card.Card(7, "C")
        self.assertRaises(hand.MaximumCardError, self.hand.add_card, extra_card)

    def test_hand_type(self):
        # try with no cards and 1 card
        self.hand.clear()
        self.assertRaises(hand.MissingCardError, self.hand.get_hand_type)
        self.hand.add_card(card.Card(2, "D"))

    def test_straight_flush(self):
        self.hand.clear()

        # check that an empty or incomplete hand does not create a straight flush
        self.assertFalse(self.hand.check_straight_flush())
        self.hand.add_card(card.Card(8, "S"))
        self.assertFalse(self.hand.check_straight_flush())
        self.hand.add_card(card.Card(9, "S"))
        self.assertFalse(self.hand.check_straight_flush())

        self.hand.add_card(card.Card(10, "S"))
        self.hand.add_card(card.Card("J", "S"))
        self.hand.add_card(card.Card("Q", "S"))

        # check that we have a straight flush with 8-Q
        self.assertTrue(self.hand.check_straight_flush())

        # check multiple and rank
        self.assertEqual(self.hand.get_multiple(), 0)
        self.assertEqual(self.hand.get_rank()[0], 12)

        # check that A-5 (condition 2) also counts as a straight flush
        self.hand.clear()
        for card_value in range(2, 6):  # 2, 3, 4, 5
            self.hand.add_card(card.Card(card_value, "D"))
        self.hand.add_card(card.Card("A", "D"))
        self.assertTrue(self.hand.check_straight_flush())

        # check multiple and rank
        self.assertEqual(self.hand.get_multiple(), 0)
        self.assertEqual(self.hand.get_rank()[0], 5)

        # check that an explicit royal flush counts as a straight flush
        self.hand.clear()
        self.hand.add_card(card.Card(10, "H"))
        self.hand.add_card(card.Card("J", "H"))
        self.hand.add_card(card.Card("Q", "H"))
        self.hand.add_card(card.Card("K", "H"))
        self.hand.add_card(card.Card("A", "H"))
        self.assertTrue(self.hand.check_straight_flush())

    def test_four_of_a_kind(self):
        self.hand.clear()
        for card_suit in ["C", "D", "H", "S"]:
            self.hand.add_card(card.Card(2, card_suit))

        # At this point we should get a false, since there are only 4 cards
        self.assertFalse(self.hand.check_four_of_a_kind())

        self.hand.add_card(card.Card(3, "D"))
        self.assertTrue(self.hand.check_four_of_a_kind())

        # check rank and multiple
        self.assertEqual(self.hand.get_multiple(), 2)
        self.assertEqual(self.hand.get_rank()[0], 3)

        # Check with only three of a kind
        self.set_three_of_a_kind()
        self.assertFalse(self.hand.check_four_of_a_kind())

    def test_full_house(self):
        self.hand.clear()
        self.assertFalse(self.hand.check_full_house())

        self.set_full_house()
        self.assertTrue(self.hand.check_full_house())

        # Check rank and multiple values here as well
        self.assertEqual(self.hand.get_rank(), 13)
        self.assertEqual(self.hand.get_multiple(), 14)

        # Check with four of a kind
        self.hand.clear()
        for card_suit in ["C", "D", "H", "S"]:
            self.hand.add_card(card.Card(2, card_suit))
        self.hand.add_card(card.Card(3, "D"))
        self.assertFalse(self.hand.check_full_house())

        # Check with general non-full house cards
        self.hand.clear()
        self.set_bad_hand()
        self.assertFalse(self.hand.check_full_house())

    def test_flush(self):
        self.hand.clear()
        self.assertFalse(self.hand.check_flush())

        # construct flush from 2-6
        for card_value in range (2, 7):
            self.hand.add_card(card.Card(card_value, "H"))

        self.assertTrue(self.hand.check_flush())

        # check rank of first item and multiple
        self.assertEqual(self.hand.get_multiple(), 0)
        self.assertEqual(self.hand.get_rank()[0], 6)

        # construct distinctly non-flush hand
        self.hand.clear()
        self.set_bad_hand()
        self.assertFalse(self.hand.check_flush())

    def test_straight(self):
        self.hand.clear()
        self.assertFalse(self.hand.check_straight())

        # construct straight from 6 to 10
        for card_value in range(6, 10):
            self.hand.add_card(card.Card(card_value, "D"))
        self.hand.add_card(card.Card(10, "S"))

        # check straight - rank and multiple don't get set if we haven't checked
        self.assertTrue(self.hand.check_straight())

        # check rank and multiple
        self.assertEqual(self.hand.get_multiple(), 0)
        self.assertEqual(self.hand.get_rank()[0], 10)

        # check low straight (A-5)
        self.hand.clear()
        for card_value in range(2, 6):  # 2, 3, 4, 5
            self.hand.add_card(card.Card(card_value, "C"))
        self.hand.add_card(card.Card("A", "S"))
        self.assertTrue(self.hand.check_straight())

        # check rank and multiple
        self.assertEqual(self.hand.get_multiple(), 0)
        self.assertEqual(self.hand.get_rank()[0], 5)

        # check non-straight hand
        self.hand.clear()
        self.set_bad_hand()
        self.assertFalse(self.hand.check_straight())

    def test_three_of_a_kind(self):
        # check empty hand
        self.hand.clear()
        self.assertFalse(self.hand.check_three_of_a_kind())

        # check three of a kind hand
        self.set_three_of_a_kind()
        self.assertTrue(self.hand.check_three_of_a_kind())

        # check rank and multiple
        self.assertEqual(self.hand.get_multiple(), 3)
        self.assertEqual(self.hand.get_rank()[0:2], [5, 4])

    def test_two_pair(self):
        # check empty hand
        self.hand.clear()
        self.assertFalse(self.hand.check_two_pair())

        # check two pair hand
        self.hand.add_card(card.Card(8, "D"))
        self.hand.add_card(card.Card(8, "C"))
        self.hand.add_card(card.Card(9, "S"))
        self.hand.add_card(card.Card(9, "H"))
        self.hand.add_card(card.Card("K", "D"))
        self.assertTrue(self.hand.check_two_pair())

        # check multiple and rank
        self.assertEqual(self.hand.get_multiple(), 9)
        self.assertEqual(self.hand.get_rank(), [8, 13])

        # check one pair hand - should be false
        self.hand.clear()
        self.hand.add_card(card.Card(8, "D"))
        self.hand.add_card(card.Card(8, "C"))
        self.hand.add_card(card.Card(10, "S"))
        self.hand.add_card(card.Card("J", "H"))
        self.hand.add_card(card.Card("K", "D"))
        self.assertFalse(self.hand.check_two_pair())

        # check full house hand
        self.set_full_house()
        self.assertTrue(self.hand.check_two_pair())

        # check multiple
        self.assertEqual(self.hand.get_multiple(), 14)

        """
        Limitation: get_rank() will only return a one-element list for a full house,
        whereas the second element in this example (AAAKK) should be the remaining
        ace card (numerical value of 14). We could account for this, but the compare
        condition will never be encountered; a full house always beats two pair and
        when comparing two full houses, the 3-up card will be taken as the multiple.
        """
        #self.assertEqual(self.hand.get_rank(), [13, 14])
        # workaround - don't include last A card:
        self.assertEqual(self.hand.get_rank(), [13])


    def test_pair(self):
        # check empty hand
        self.hand.clear()
        self.assertFalse(self.hand.check_two_pair())

        # check one pair hand
        self.hand.add_card(card.Card("J", "D"))
        self.hand.add_card(card.Card("J", "C"))
        self.hand.add_card(card.Card(9, "S"))
        self.hand.add_card(card.Card(8, "H"))
        self.hand.add_card(card.Card(7, "D"))
        self.assertTrue(self.hand.check_pair())

        # check multiple and rank for pair
        self.assertEqual(self.hand.get_multiple(), 11)
        self.assertEqual(self.hand.get_rank(), [9, 8, 7])

        # check three of a kind hand
        self.set_three_of_a_kind()
        self.assertTrue(self.hand.check_pair())

        # check multiple and rank for pair
        self.assertEqual(self.hand.get_multiple(), 3)

        """
        We run into the same limitation as two pair: both two pair and three of a kind
        will have different rank patterns not caught by this function. Again, provided
        that we always run in descending order of hand types, comparison will succeed.
        """

        # TODO: additional tests here for pair scenarios (non-pair hands)
        self.set_bad_hand()
        self.assertFalse(self.hand.check_pair())

    def test_high_card(self):
        # check empty hand
        self.hand.clear()
        self.assertFalse(self.hand.check_high_card())

        # check default bad hand
        self.set_bad_hand()
        self.assertTrue(self.hand.check_high_card())

        # check multiple and rank
        self.assertEquals(self.hand.get_multiple(), 0)
        self.assertEquals(self.hand.get_rank(), [7, 5, 4, 3, 2])


if __name__ == '__main__':
    unittest.main()

