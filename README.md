# handcompare

A Python application for comparing two sets of cards, as well as demonstrating
test-driven development principles.

## Contact

Jake Billo (<jake@jakebillo.com>)

Other work and contributions available at <http://github.com/jbillo>

# Requirements

* Python 2.7.x (not compatible with Python3)
    * Tested on OS X 10.8.3/Python 2.7.2

# Usage

From a terminal, run:

    python /path/to/handcompare/handcompare.py [hand1] [hand2] <options>

`hand1` and `hand2` are each comma-separated strings representing a hand of 5 cards. Cards are given as a number from 2 to 10, or the character J/Q/K/A for Jack/Queen/King/Ace, followed by a suit character (*C*lubs, *D*iamonds, *H*earts or *S*pades.) For example, the following hand:

    2C,3H,4D,5S,10C

would represent the two of clubs, three of hearts, four of diamonds, five of spades and ten of clubs.

A complete command line could look like the following:

    python /path/to/handcompare/handcompare.py 2C,3H,4D,5S,10C 10D,JD,QD,KD,AD

and would return

    Hand 2 is the winning hand

Any input or other errors encountered at runtime will be output to `stderr` as a typical exception trace. In a production or completely headless system, I would use a Python logging class. That enhancement would offer the ability to redirect these exceptions to file, a syslog server or database for further analysis and troubleshooting.

Current options include:

    --no-sanity     Disable sanity checking. Hand 2 may contain some or all
                    of the same cards (suit and value) as Hand 1.
                    In a real-world scenario, this would be as if two players
                    were drawing from each of their own 52 card decks.
                    This option is exposed for consistency as the test suite does
                    not enforce the "unique cards" restriction when comparing hands.

For an example use of the `--no-sanity` parameter to check two straight flushes:

    python /path/to/handcompare/handcompare.py 10C,JC,QC,KC,AC 10H,JH,QH,KH,AH

Output:

    Hand 1 and 2 draw

# Testing and integration with build system

Run the following command:

    python /path/to/handcompare/test_handcompare.py

Output will be in standard Python `unittest` format, with the last output line as the string `OK` if all tests passed.

# Assumptions

* In a traditional five-card draw or Texas Hold-Em poker game, the game is played with only one deck of 52 cards. This choice is made to preserve other elements (odds calculation changes with multiple decks.) Thus, duplicate cards are rejected and are considered invalid input. Each hand may not have the same card repeated twice or more.
    * In normal execution, Hand 2 may not contain any of the same cards as in Hand 1.  There is a sanity check that will fail during normal execution. Some of the test case scenarios exercised to confirm proper hand ranking behaviour rely on the same cards being in Hand 1 and Hand 2. This option can be disabled at runtime with a `--no-sanity` parameter passed after the hand strings.
    * Possible improvement: allow for multi-deck play, relaxing these restrictions - although in real life scenarios, these games are casino variants, not traditional poker and would have different rules (wild cards) that would affect the hand ranking process.

# Background information and methodology

As my main focus of work with BlackBerry is not specifically software development, some of the concepts in this application were recently learned - especially test-driven development practices. My resources and references are provided below; I hope they are helpful in providing additional clarity on choices and program structure.

Most Python scripts I write for internal usage have no traditional development methodology or a formal testing framework. I am typically the sole maintainer of scripts in our prerelease infrastructure environments, so change control is mostly used as a rollback mechanism in the event a new script catastrophically fails. Change requests come in alongside new infrastructure products from official development teams, so they are easily scheduled and accounted for.

Traditionally my team employs SVN for change control. I have been the main team member leading the charge to move these scripts and internal documentation to a GitHub Enterprise installation.

## Resources

* Python `.gitignore` file copied from GitHub: <https://github.com/github/gitignore/blob/master/Python.gitignore>
* Wikipedia articles <http://en.wikipedia.org/wiki/Five-card_draw> and <http://en.wikipedia.org/wiki/Poker_probabilities> for background information
* Python `unittest` library documentation: <http://docs.python.org/2/library/unittest.html>
* Python `unittest` examples: <http://docs.python.org/release/2.5.2/lib/minimal-example.html>
* Python sorting reference: <http://wiki.python.org/moin/HowTo/Sorting/>
* SickBeard: <https://github.com/midgetspy/Sick-Beard/> Python application on GitHub - module construction, common initialization paradigms, general reference
* Various Pythonic language idioms/references on StackOverflow; no code was directly copied from any resource, but used mainly as a reference
* Google Python style guide for influence: <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>
    * Specific use of `pychecker` to detect potential issues with code <http://pychecker.sourceforge.net/>
* PEP-0257 for preferred docstring syntax: <http://www.python.org/dev/peps/pep-0257/>

