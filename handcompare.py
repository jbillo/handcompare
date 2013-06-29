#!/usr/bin/env python

"""
handcompare

Application for comparing poker hands

Jake Billo <jake@jakebillo.com>
"""

import sys

import card
import hand

# Define return/main() exit codes for win/draw conditionals
HAND1_WINS = 2
HAND2_WINS = 3
HANDS_DRAW = 4

# define custom exception classes
class MissingArgumentError(Exception):
    """Exception thrown when command-line arguments are improperly provided."""
    pass

class InvalidHandError(Exception):
    """Exception thrown when a hand is inconsistent."""
    pass

class HandCompare(object):
    """
    Class for parsing card strings and comparing two hands.
    """

    # Define the typical/maximum number of cards in the hand.
    CARDS_IN_HAND = 5

    # Define verbose output string for verbosity testing.
    verbose_output = ""

    def check_argcount(self, system_args):
        """
        Checks the number of arguments passed on the command line.
        Throws a MissingArgumentError if two hands are not provided.
        """

        # if the number of arguments < 3, raise exception
        # this includes application executable, hand1, hand2
        if not system_args or len(system_args) < 3:
            raise MissingArgumentError("Provide at least two hands to compare")

        return True

    def parse_card_string(self, card_string):
        """
        Given a string, parses a card and returns a Card objects.
        """
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
        """
        Given a string, uses parse_card_string to turn that string into Card objects,
        and then assembles a Hand object from those cards. Can throw an InvalidHandError
        when the hand_string does not parse properly.
        """

        if not hand_string or not hand_string.strip():
            raise InvalidHandError("Specified hand was None or empty")

        if hand_string.count(",") != (self.CARDS_IN_HAND - 1):
            raise InvalidHandError("Hand did not contain correct number of comma-separated cards; original hand: {0}".format(hand_string))

        # Split hand; our count precondition ensures the result list has enough elements
        split_cards = hand_string.split(",")

        # create Hand object and populate it with cards; this will throw exceptions
        # on any invalid conditions (duplicate cards, etc)
        create_hand = hand.Hand()
        for card_string in split_cards:
            create_hand.add_card(self.parse_card_string(card_string))

        return create_hand

    def hand_sanity(self, hand1, hand2):
        """
        Perform a sanity test given two Hand objects - that they do not contain the
        same cards. The Hand object itself ensures the same card does not appear twice,
        but this optional function enforces a "52-card deck" constraint.
        """

        h1_cards = hand1.get_cards()
        h2_cards = hand2.get_cards()

        # use defined __eq__ method to check card equality
        for card in h1_cards:
            for comp_card in h2_cards:
                if card == comp_card:
                    raise InvalidHandError(
                        "Same card ({0}) exists in both hands".format(card))

        return True

    def main(self):
        """
        Main entry point to application. Requests two card hands, attempts to parse them,
        and outputs a comparison (hand 1 vs hand 2.)
        """

        # Verbosity; use integer in case multiple levels needed later (--debug, etc).
        verbosity = 0

        # Check argument count passed on command line
        try:
            self.check_argcount(sys.argv)
        except MissingArgumentError:
            print "Error: Missing argument; please specify two hands."
            self.usage()

        # Try to parse hands
        try:
            hand1 = self.parse_hand_string(sys.argv[1])
            hand2 = self.parse_hand_string(sys.argv[2])
        except InvalidHandError:
            print "Error: One or more hands was invalid."
            self.usage()
        except hand.DuplicateCardError:
            print "Error: The same card was specified more than once in a hand."
            self.usage()

        # Check options for sanity
        if not "--no-sanity" in sys.argv:
            # Perform sanity check and allow exception to bubble up/terminate
            try:
                self.hand_sanity(hand1, hand2)
            except InvalidHandError:
                print ("Error: Duplicate cards found across both hands. To disable, "
                      "use the --no-sanity option.")
                self.usage()

        # Check for verbosity level
        if "--verbose" in sys.argv:
            verbosity = 1

        # Compare hands and print output
        if hand1 > hand2:
            print "Hand 1 is the winning hand"
            self.verbose_hand_details(verbosity, hand1, hand2)
            return HAND1_WINS
        elif hand2 > hand1:
            print "Hand 2 is the winning hand"
            self.verbose_hand_details(verbosity, hand1, hand2)
            return HAND2_WINS
        else:
            print "Hand 1 and 2 draw"
            self.verbose_hand_details(verbosity, hand1, hand2)
            return HANDS_DRAW

    def verbose_hand_details(self, verbosity, hand1, hand2):
        """Print verbose information about contents (types) of hands."""
        if verbosity == 0:
            return

        # Provide user with details on hands. Don't need to know which hand
        # won in this context, just the attributes that caused a win. Also, replace
        # underscores with spaces and title case for readability.

        self.verbose_output = "Hand 1: {0}, multiple {1}, rank {2}\n".format(
              hand1.get_type_text().replace("_", " ").title(), hand1.get_multiple(),
              hand1.get_rank())

        self.verbose_output += "Hand 2: {0}, multiple {1}, rank {2}\n\n".format(
            hand2.get_type_text().replace("_", " ").title(), hand2.get_multiple(),
            hand2.get_rank())

        print self.verbose_output

    def usage(self):
        """
        Meant to be called in an error or help message. Returns usage information for
        the application, then exits with system error code 1.
        """

        print """
Usage:
{0} [hand1] [hand2] <options>

Current options include:

--no-sanity     Disable sanity checking. Hand 2 may contain some or all
                of the same cards (suit and value) as Hand 1.
                In a real-world scenario, this would be as if two players
                were drawing from each of their own 52 card decks.
                This option is exposed for consistency as the test suite does
                not enforce the "unique cards" restriction when comparing hands.

--verbose       Output details on hand comparison, including attributes,
                multiple and type for each of the hands.
        """.format(sys.argv[0])

        sys.exit(1)


# Entry point for application so this module can be imported by other applications
if __name__ == '__main__':
    hc = HandCompare()
    hc.main()
