"""
This script is not directly executable and forms part of the test suite for
the handcompare application.
"""

# TestCardValue: Test cases to deal with checking individual card values.

import unittest

import handcompare
import card

class TestCardValue(unittest.TestCase):
    def setUp(self):
        """Designate shared objects for all test cases."""
        self.hc = handcompare.HandCompare()
        self.card = card.Card(2, "C")

    def tearDown(self):
        """Explicitly delete objects during class destruction."""
        del self.hc
        del self.card

    def test_map_card_value(self):
        """Check for known card values so jack through ace are treated properly."""
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
        """Check valid and invalid suits for cards."""
        # check for known suit values
        for valid_suit in ["C", "D", "H", "S"]:
            self.assertTrue(self.card._check_card_suit(valid_suit))

        # check for unknown suit values
        for invalid_suit in ["X", " ", "", 0, None]:
            self.assertFalse(self.card._check_card_suit(invalid_suit))

        # check that constructing a card is successful and fails appropriately:

        # check card value failure
        self.assertRaises(card.InvalidCardError, card.Card, 20, "C")

        # check card value success
        self.assertTrue(card.Card(10, "C"))

        # check card suit failure
        self.assertRaises(card.InvalidCardError, card.Card, 10, "X")

        # check card suit failure
        self.assertTrue(card.Card(10, "H"))

    def test_check_card_equal(self):
        """Check card equivalency - whether they are the exact same card or not."""
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
