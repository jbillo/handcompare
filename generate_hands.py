#!/usr/bin/env python

# This script generates command lines appropriate for

import default_hands
import handcompare

if __name__ == '__main__':
    hand_values = default_hands.DEFAULT_HANDS.values()
    for i in range(0, len(hand_values) - 1):
        print "./handcompare.py {0} {1} --verbose --no-sanity".format(
            hand_values[i], hand_values[i+1])
        i = i+1
