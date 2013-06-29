"""
This script is not directly executable and forms part of the test suite for
the handcompare application.
"""

# TestHand: Test cases to deal with checking hand ranks, multipliers and types.

import unittest

import hand
import card


class TestHand(unittest.TestCase):
    def setUp(self):
        """Construct shared objects for all testcases in this suite."""
        self.hand = hand.Hand()

    def tearDown(self):
        """Destroy all shared objects from this suite."""
        del self.hand

    def set_bad_hand(self):
        """
        Helper function to set up a 5 card hand that won't beat anything; rank 7/high card
        """
        self.hand.clear()
        self.hand.add_card(card.Card(2, "D"))
        self.hand.add_card(card.Card(3, "C"))
        self.hand.add_card(card.Card(4, "S"))
        self.hand.add_card(card.Card(5, "H"))
        self.hand.add_card(card.Card(7, "D"))

    def set_full_house(self):
        """Helper function to construct an AAAKK full house"""
        self.hand.clear()
        for card_suit in ["C", "D", "H"]:
            self.hand.add_card(card.Card("A", card_suit))
        self.hand.add_card(card.Card("K", "H"))
        self.hand.add_card(card.Card("K", "S"))

    def set_three_of_a_kind(self):
        """Helper function to construct a 3-of-a-kind hand, 33345"""
        self.hand.clear()
        self.hand.add_card(card.Card(3, "D"))
        self.hand.add_card(card.Card(3, "C"))
        self.hand.add_card(card.Card(3, "S"))
        self.hand.add_card(card.Card(4, "H"))
        self.hand.add_card(card.Card(5, "D"))

    def test_clear(self):
        """Ensure there are no cards in the hand after a clear operation"""
        self.hand.clear()
        self.assertEqual(len(self.hand.get_cards()), 0)

    def test_clear_sort(self):
        """Check that the sort function returns false after a clear operation"""
        self.hand.clear()
        self.assertFalse(self.hand.sort_cards())

    def test_sort_cards(self):
        """Check that the sort function returns true when one or more cards are in hand"""
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
        """
        Check that adding a card works,
        as well as rejecting invalid or too many cards
        """
        self.hand.clear()

        # try adding a non-card object
        self.assertRaises(ValueError, self.hand.add_card, "2C")

        # try adding a valid card
        valid_card = card.Card(2, "C")
        self.assertTrue(self.hand.add_card(valid_card))

        # try adding an invalid card
        invalid_card_detected = False
        try:
            card.Card(15, "C")
        except card.InvalidCardError:
            invalid_card_detected = True

        self.assertTrue(invalid_card_detected)

        # try adding too many cards - populate four more in besides 2C
        for card_value in range(3, 7):
            self.hand.add_card(card.Card(card_value, "C"))

        extra_card = card.Card(7, "C")
        self.assertRaises(hand.MaximumCardError, self.hand.add_card, extra_card)

        # try adding a duplicate card and checking for exception
        self.hand.clear()
        self.hand.add_card(card.Card(2, "C"))
        self.assertRaises(hand.DuplicateCardError, self.hand.add_card, card.Card(2, "C"))

    def test_hand_type(self):
        """Check that get_hand_type returns the proper value"""
        # try with no cards and 1 card
        self.hand.clear()
        self.assertRaises(hand.MissingCardError, self.hand.get_hand_type)
        self.hand.add_card(card.Card(2, "D"))

        # Test specific hand types - this will help if someone changes values
        self.set_three_of_a_kind()
        self.assertEqual(self.hand.get_hand_type(), 3)
        self.set_full_house()
        self.assertEqual(self.hand.get_hand_type(), 6)
        self.set_bad_hand()
        self.assertEqual(self.hand.get_hand_type(), 0)

    def test_type_text(self):
        """Check that get_hand_type_text() returns the proper value."""

        # Override the hand - check for a non-existent key
        self.hand.clear()
        self.hand.type = -1
        self.assertFalse(self.hand.get_type_text())

        # Check hand text for three of a kind
        self.set_three_of_a_kind()
        self.assertEqual(self.hand.get_type_text(), "three_of_a_kind")

    def test_hand_repr(self):
        """Check that the string representation of the hand matches expected value"""
        self.set_bad_hand()
        self.assertEqual(str(self.hand),
                         "[(2, 'D'), (3, 'C'), (4, 'S'), (5, 'H'), (7, 'D')]")

    def test_n_of_a_kind(self):
        """Check that n-of-a-kind provides correct errors - check 4 and 3 below."""
        self.hand.clear()
        self.assertFalse(self.hand.check_n_of_a_kind(4))
        self.set_three_of_a_kind()
        self.assertFalse(self.hand.check_n_of_a_kind(5))

    def test_get_pairs(self):
        """Check that get_pairs() returns False when there are not enough cards"""
        self.hand.clear()
        self.assertFalse(self.hand.get_pairs())

    def test_straight_flush(self):
        """Check that straight flush detection functions properly"""
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

        # check that the result is a straight flush with 8-Q
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
        """Check that 4-of-a-kind detection functions properly"""
        self.hand.clear()
        for card_suit in ["C", "D", "H", "S"]:
            self.hand.add_card(card.Card(2, card_suit))

        # At this point False should be returned, since there are only 4 cards
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
        """Check that full house detection functions properly"""
        self.hand.clear()
        self.assertFalse(self.hand.check_full_house())

        self.set_full_house()
        self.assertTrue(self.hand.check_full_house())

        # Check rank and multiple values here as well
        self.assertEqual(self.hand.get_rank(), [13])
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
        """Check that flush detection functions properly"""
        self.hand.clear()
        self.assertFalse(self.hand.check_flush())

        # construct flush from 2-6
        for card_value in range(2, 7):
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
        """Check that straight detection functions properly"""
        self.hand.clear()
        self.assertFalse(self.hand.check_straight())

        # construct straight from 6 to 10
        for card_value in range(6, 10):
            self.hand.add_card(card.Card(card_value, "D"))
        self.hand.add_card(card.Card(10, "S"))

        # check straight - rank and multiple don't get set if check has not been run
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
        """Check that 3-of-a-kind detection functions properly"""
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
        """Check that two-pair detection functions properly"""
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
        # Rank will not be reverse sorted: element 2 will be the second highest pair.
        self.assertEqual(self.hand.get_rank(), [8, 13])

        # check one pair hand - should be false
        self.hand.clear()
        self.hand.add_card(card.Card(8, "D"))
        self.hand.add_card(card.Card(8, "C"))
        self.hand.add_card(card.Card(10, "S"))
        self.hand.add_card(card.Card("J", "H"))
        self.hand.add_card(card.Card("K", "D"))
        self.assertFalse(self.hand.check_two_pair())

        # check hand without at least two unique cards

        # check full house hand
        self.set_full_house()
        self.assertTrue(self.hand.check_two_pair())

        # check multiple
        self.assertEqual(self.hand.get_multiple(), 14)

        """
        Limitation: get_rank() will only return a one-element list for a full house,
        whereas the second element in this example (AAAKK) should be the remaining
        ace card (numerical value of 14). It is possible to account for this, but the
        compare condition will never be encountered. A full house always beats two pair
        and when comparing two full houses, the 3-up card will be taken as the multiple.

        For example, this will fail:
        self.assertEqual(self.hand.get_rank(), [13, 14])
        """
        # Workaround from above - don't include last A card:
        self.assertEqual(self.hand.get_rank(), [13])

    def test_pair(self):
        """Check that single pair detection is working properly"""
        # check empty hand
        self.hand.clear()
        self.assertFalse(self.hand.check_pair())

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
        This function has the same limitation as two pair: both two pair and three of a
        kind will have different rank patterns not caught by this function. Provided
        that the program always runs in descending order of hand types, comparison will
        succeed.
        """

        # Check false for non-pair scenario
        self.set_bad_hand()
        self.assertFalse(self.hand.check_pair())

    def test_high_card(self):
        """Check that high card detection is working properly"""
        # check empty hand
        self.hand.clear()
        self.assertFalse(self.hand.check_high_card())

        # check default bad hand
        self.set_bad_hand()
        self.assertTrue(self.hand.check_high_card())

        # check multiple and rank
        self.assertEquals(self.hand.get_multiple(), 0)
        self.assertEquals(self.hand.get_rank(), [7, 5, 4, 3, 2])

    def test_check_rank_consistency(self):
        # Check rank consistency with mocked up hands
        hand1 = hand.Hand()
        hand2 = hand.Hand()

        # Override ranking properties manually and check operators
        hand1.rank = [0]
        hand2.rank = [0]
        self.assertFalse(hand1.check_rank_consistency(hand2))

        # Set types and multiples equal to zero
        hand1.type = 0
        hand2.type = 0
        hand1.multiple = 0
        hand2.multiple = 0
        self.assertFalse(hand1 > hand2)
        self.assertFalse(hand1 < hand2)

        # Set ranks to different lengths and check consistency
        hand1.rank = [0, 0]
        self.assertRaises(hand.CompareError, hand1.check_rank_consistency, hand2)
