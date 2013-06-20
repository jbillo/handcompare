# handcompare

A Python application for comparing two sets of cards, as well as demonstrating
test-driven development principles.

# Requirements

* Python 2.7.x (not compatible with Python3)

# Usage

From a terminal, run:

    python /path/to/handcompare/handcompare.py [hand1] [hand2]

Where `hand1` and `hand2` are each comma-separated strings representing a hand of 5 cards. Cards are given as a number from 2 to 10, or the character J/Q/K/A for Jack/Queen/King/Ace, followed by a suit character. For example, the following hand:

    2C,3H,4D,5S,10C

would represent the two of clubs, three of hearts, four of diamonds, five of spades and ten of clubs.

A complete command line could look like the following:

    python /path/to/handcompare/handcompare.py 2C,3H,4D,5S,10C 10D,JD,QD,KD,AD

and would return

    Hand 2 is the winning hand

Any input or other errors encountered at runtime will be output to stderr.

# Testing and integration with build system

Run the following command:

    python /path/to/handcompare/test_handcompare.py

Output will be standard Python `unittest`, with the last line as the string `OK` if all tests passed.

# Assumptions

* In a traditional five-card draw or Texas Hold-Em poker game, the game is played with only one deck. This choice is made to preserve other elements (odds calculation changes with multiple decks). Thus, duplicate cards are rejected and are considered invalid input. Hand 1 may not have the same card repeated twice or more, and Hand 2 may not contain any of the same cards as in Hand 1.
    * Possible improvement: allow for multi-deck play, reducing these restrictions - although in real life scenarios, these games are casino variants, not traditional poker and would have different rules (wild cards) that would affect the hand ranking process.

# Background information and methodology

As my main focus of work with BlackBerry has not been development-related, some of the concepts in this application were recently learned. My resources are referenced below and may help to provide additional clarity on choices and

To start, most Python scripts I write for internal usage have no traditional development methodology or a formal testing framework. I am typically the sole maintainer of scripts in alpha or beta environments, and change requests come in alongside new infrastructure products from official development teams, so they are easily scheduled and accounted for.

We do, however, employ SVN for change control and I have been the main team member leading the charge to move these scripts and documentation to a GitHub Enterprise installation.


## Resources

* Python .gitignore file: <https://github.com/github/gitignore/blob/master/Python.gitignore>
* Wikipedia articles <http://en.wikipedia.org/wiki/Five-card_draw> and <http://en.wikipedia.org/wiki/Poker_probabilities> for background information
* Python `unittest` library documentation: <http://docs.python.org/2/library/unittest.html>
* Python `unittest` examples: <http://docs.python.org/release/2.5.2/lib/minimal-example.html>
* SickBeard: <https://github.com/midgetspy/Sick-Beard/> Python application on GitHub - module construction, common initialization paradigms, general reference
