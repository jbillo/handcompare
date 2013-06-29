"""
This script is not directly executable and forms part of the test suite for
the handcompare application.
"""

# TestCoreApp: Test cases to deal with operations in the core application.

import unittest
import sys
import os

import handcompare

class TestCoreApp(unittest.TestCase):
    def setUp(self):
        """Create local objects used in all testcases."""
        self.hc = handcompare.HandCompare()

        # Suppress sys.stdout and sys.stderr until this test case cleans up.
        # Can't just set sys.stdout/err to None because it needs to be writable.
        # Create a /dev/null object and clean up on tearDown().
        self.devnull = open(os.devnull, 'w')
        self.stdout = sys.stdout
        sys.stdout = self.devnull
        self.stderr = sys.stderr
        sys.stderr = self.devnull

    def tearDown(self):
        """Remove locally generated objects and reset stdout/err."""
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.devnull.close()

    def test_main(self):
        """Test the main entry point to the application."""

        # Remove optional parameters from sys.argv and ensure application terminates.
        old_argv = sys.argv
        sys.argv = [sys.argv[0]]

        # Ensure that when we run this application without parameters, we get an exit.
        # Catch this exit and don't actually terminate the program.
        self.assertRaises(SystemExit, self.hc.main)

        # Test invalid hands - too short/invalid cards
        sys.argv = ("handcompare.py", "5X", "6X")
        self.assertRaises(SystemExit, self.hc.main)

        # Check for duplicate cards in a hand
        sys.argv = ("handcompare.py", "5C,5C,6C,7C,8C", "4D,5D,6D,7D,8D")
        self.assertRaises(SystemExit, self.hc.main)

        # By default we enforce sanity checking - confirm that same card across hands
        # exits the application
        sys.argv = ("handcompare.py", "5C,6C,7C,8C,9C", "5C,4H,5H,6H,7H")
        self.assertRaises(SystemExit, self.hc.main)

        # Check result for hand 1 winning
        sys.argv = ("handcompare.py", "5D,6D,7D,8D,9D", "4C,5C,6C,7C,8C")
        self.assertEqual(self.hc.main(), handcompare.HAND1_WINS)

        # Check result for hand 2 winning
        sys.argv = ("handcompare.py", "JC,JD,JH,4S,5S", "KC,KS,KD,AS,AC")
        self.assertEqual(self.hc.main(), handcompare.HAND2_WINS)

        # Check result for hands drawing
        sys.argv = ("handcompare.py", "5C,6C,7C,8H,9H", "9S,8S,7D,6D,5D")
        self.assertEqual(self.hc.main(), handcompare.HANDS_DRAW)
        self.assertEqual(self.hc.main(), handcompare.HANDS_DRAW)

        # Reset sys.argv as all tests are done
        sys.argv = old_argv
