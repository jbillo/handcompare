#!/usr/bin/env python

"""
handcompare - application for comparing poker hands
Jake Billo <jake@jakebillo.com>
"""

# define custom exception classes
class MissingArgumentError(Exception):
    pass

class InvalidHandError(Exception):
    pass

class HandCompare():

    def check_argcount(self, system_args):
        # if the number of arguments < 3, raise exception
        # this includes application executable, hand1, hand2
        if not system_args or len(system_args) < 3:
            raise MissingArgumentError("Provide at least two hands to compare")

        return True

    def parse_hand_string(self, hand_string):
        if not hand_string or not hand_string.strip():
            raise InvalidHandError("Specified hand was None or empty")

        if hand_string.count(",") != 4:
            raise InvalidHandError("Hand did not contain enough comma-separated cards")

        # check if we can split this and the resulting list has enough elements


        return [1,2,3,4,5]

    def start(self):
        pass



if __name__ == '__main__':
    hc = HandCompare()
    hc.start()
