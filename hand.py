import card

class DuplicateCardError(Exception):
    pass

class MissingCardError(Exception):
    pass

class MaximumCardError(Exception):
    pass

class CompareError(Exception):
    pass

class Hand():
    cards = []

    # type: hand type (flush, straight, pair, etc...)
    type = 0

    # rank: rank of winning hand (straight = highest card value; could be a tuple)
    rank = 0

    # multiple: in pair+ situations, contains the value of pair+s (3x 8's = 8)
    multiple = 0

    # Perform the following technique for ranking:
    # winning hand is greater of type
    # if type is equal, winning hand is greater multiple
    # if multiple is equal, winning hand is > rank (may be list or tuple)
    # if rank is equal, hands are a draw

    MAXIMUM_CARDS = 5

    HAND_TYPES = {
        "straight_flush": 8,
        "four_of_a_kind": 7,
        "full_house": 6,
        "flush": 5,
        "straight": 4,
        "three_of_a_kind": 3,
        "two_pair": 2,
        "pair": 1,
        "high_card": 0,
    }

    # representation: return the card list
    def __repr__(self):
        return str(self.cards)

    def __init__(self):
        return self.clear()

    def __gt__(self, other):
        # check hand type first
        if self.get_type() > other.get_type():
            return True
        elif self.get_type() < other.get_type():
            return False

        # at this point hand types are equal, check multiple (single digit)
        if self.get_multiple() > other.get_multiple():
            return True
        elif self.get_multiple() < other.get_multiple():
            return False

        # at this point hand multiples are equal, check rank (list)
        self_rank = self.get_rank()
        other_rank = other.get_rank()

        # stop-gap: raise exception if the comparison functions
        # this ensures data integrity and is a good way to find problems in batch runs
        if self_rank == other_rank == 0:
            # ranks are equal at zero
            return False
        elif len(self_rank) != len(other_rank):
            raise CompareError("Length of hand rankings do not match: {0} and {1}".format(self_rank, other_rank))

        # find the first element that doesn't match
        for rank_index in range(0, len(self_rank)):
            if self_rank[rank_index] > other_rank[rank_index]:
                # self > other
                return True
            elif self_rank[rank_index] < other_rank[rank_index]:
                # other > self
                return False
            # otherwise, rank items are equal - continue loop

        # Finally, return false - they are equal in all categories
        # so self is not greater than other (but __eq__ operator should deliver True)
        return False

    def __lt__(self, other):
        # check hand type first
        if other.get_type() > self.get_type():
            return True
        elif other.get_type() < self.get_type():
            return False

        # at this point hand types are equal, check multiple (single digit)
        if other.get_multiple() > self.get_multiple():
            return True
        elif other.get_multiple() < self.get_multiple():
            return False

        # at this point hand multiples are equal, check rank (list)
        self_rank = self.get_rank()
        other_rank = other.get_rank()

        # stop-gap: raise exception if the comparison functions
        # this ensures data integrity and is a good way to find problems in batch runs
        if self_rank == other_rank == 0:
            # ranks are equal at zero
            return False
        elif len(self_rank) != len(other_rank):
            raise CompareError("Length of hand rankings do not match: {0} and {1}".format(self_rank, other_rank))

        # find the first element that doesn't match
        for rank_index in range(0, len(self_rank)):
            if other_rank[rank_index] > self_rank[rank_index]:
                # other > self
                return True
            elif other_rank[rank_index] < self_rank[rank_index]:
                # self > other
                return False
            # otherwise, rank items are equal - continue loop

        # Finally, return false - they are equal in all categories
        # so self is not greater than other (but __eq__ operator should deliver True)
        return False

    def __eq__(self, other):
        # Check type, multiple and rank separately for readability
        if self.get_type() != other.get_type():
            return False

        if self.get_multiple() != other.get_multiple():
            return False

        if self.get_rank() != other.get_rank():
            return False

        return True

    def __le__(self, other):
        # Check equality and __lt__ with inclusive or
        return (self.__eq__(other) or self.__lt__(other))

    def __ge__(self, other):
        # Check equality and __gt__ with inclusive or
        return (self.__eq__(other) or self.__gt__(other))

    def __ne__(self, other):
        # Convenience function - just return inverse of __eq__
        return not (self.__eq__(other))

    # helper to clear hand of all cards
    def clear(self):
        self.cards = []
        self.rank = 0
        self.multiple = 0

    def get_cards(self):
        return self.cards

    def get_type(self):
        return self.type

    def get_multiple(self):
        return self.multiple

    def get_rank(self):
        return self.rank

    # helper: return values of cards; list will be sorted
    def get_card_values(self):
        card_values = []
        for card in self.cards:
            card_values.append(card.get_value())

        return card_values

    # helper: return unique card values in a set
    def get_unique_card_values(self):
        return set(self.get_card_values())

    def sort_cards(self):
        # Using the object representation, Python's built in sorted() function
        # will ensure the cards get sorted by value, then suit.
        if not self.cards:
            return False

        self.cards = sorted(self.cards, key=lambda test_card: test_card.value)
        return True

    def has_exact_card(self, card_obj):
        for card in self.cards:
            if card.value == card_obj.get_value() and card.suit == card_obj.get_suit():
                return True

        return False

    def add_card(self, card_obj):
        # This is not conventional Python; we could check attributes instead
        # (philosophy of duck typing) and only error if needed properties not found
        if not isinstance(card_obj, card.Card):
            raise ValueError("Must provide Card object to Hand")

        # check if card is already in list and raise error if so
        if self.has_exact_card(card_obj):
            raise DuplicateCardError("Card already exists in this hand")

        # check if we are already at the maximum number of cards
        if len(self.cards) == self.MAXIMUM_CARDS:
            raise MaximumCardError("Already have {0} cards in this hand".format(self.MAXIMUM_CARDS))

        self.cards.append(card_obj)
        self.sort_cards()

        # if we have the maximum number of cards now, determine hand type
        # this sets ranking, multiple and
        if len(self.cards) == self.MAXIMUM_CARDS:
            self.get_hand_type()

        return True

    def get_hand_type(self):
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            raise MissingCardError("Must have exactly five cards in hand")

        # Dynamically check hand types based on dictionary definitions
        for hand_type in self.HAND_TYPES.keys():
            """
            Account for situations where getattr() call fails to get function.
            This would be in a situation where a new hand type (eg: "royal_sampler": 100)
            gets added, but the corresponding check_royal_sampler function does not exist.
            In this case, the hand will never get set to the designated type as it can't
            be checked for.
            """

            if not getattr(self, "check_%s" % hand_type):
                continue

            # Actually run the check_X function call and set hand type if True
            if getattr(self, "check_%s" % hand_type)():
                self.type = self.HAND_TYPES[hand_type]
                break

        return True

    def set_rank_by_values(self):
        card_values = self.get_card_values()

        # reverse the card values for easier forward comparison with other Hand objects
        card_values.sort(reverse=True)
        self.rank = card_values
        return True

    def check_straight_flush(self):
        # definition: five cards in sequence, all of same suit
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        # check if all cards are same suit - reuse flush code
        if not self.check_flush():
            return False

        # all cards are the same suit; check if they form a sequence - reuse straight code
        return self.check_straight()

    def check_four_of_a_kind(self):
        # definition: four cards, any suit, same value
        # use generic function to accomplish this
        return self.check_n_of_a_kind(4)

    def check_full_house(self):
        # definition: three matching cards of one value + two matching cards of another
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        card_values = self.get_card_values()

        # check that we have two unique card values only to fail quickly
        unique_values = self.get_unique_card_values()
        if len(unique_values) != 2:
            return False

        # check occurrences: 3x one value, 2x other value
        unique_value_test = list(unique_values)
        value1 = unique_value_test[0]
        value2 = unique_value_test[1]

        if (card_values.count(value1) == 3 and card_values.count(value2) == 2):
            self.multiple = value1
            self.rank = value2
            return True
        elif (card_values.count(value1) == 2 and card_values.count(value2) == 3):
            self.multiple = value2
            self.rank = value1
            return True

        return False

    def check_flush(self):
        # definition: all cards same suit, high card wins
        # this means we have to drop the entire sequence into rank
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        # drop suits into a set to enforce uniqueness
        card_suits = set()
        for card in self.cards:
            card_suits.add(card.get_suit())

        # there should only be one suit present
        if len(card_suits) != 1:
            return False

        # we know this is a flush of some type; set multiple and rank accordingly
        # ace should always act as a high card
        self.multiple = 0
        self.set_rank_by_values()

        return True

    def check_straight(self):
        # condition 1: ace low (A = 1) - will appear as exactly 2, 3, 4, 5, 14 in values
        # condition 2: normal, no aces or ace high (A = 14)
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        # we can test explicitly for condition 1:
        ace_low = True
        ace_low_values = [2, 3, 4, 5, 14]
        for card_index in range(0, len(self.cards)):
            if ace_low_values[card_index] != self.cards[card_index].get_value():
                ace_low = False
                break

        # if we have an ace low condition, rank is always 5
        # and type will be straight flush. Overwrite ace as 1.
        if ace_low:
            self.multiple = 0
            self.rank = [5, 4, 3, 2, 1]
            return True

        prev_value = self.cards[0].get_value()
        # for each card from array position 1-4,
        # check if its value is exactly 1 more than its predecessor

        for card in self.cards[1:]:
            if card.get_value() != (prev_value + 1):
                return False
            prev_value = card.get_value()

        # This is a straight; set its rank by appropriate values
        self.multiple = 0
        self.set_rank_by_values()
        return True

    def check_n_of_a_kind(self, n):
        if n > (self.MAXIMUM_CARDS - 1):
            return False

        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        card_values = self.get_card_values()
        unique_values = self.get_unique_card_values()
        for value in unique_values:
            if card_values.count(value) >= n:
                self.multiple = value
                self.set_rank_by_values()
                return True

        return False

    def check_three_of_a_kind(self):
        return self.check_n_of_a_kind(3)

    def check_two_pair(self):
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        unique_values = self.get_unique_card_values()

        if len(unique_values) < 2:
            # must have at least 2 unique values for two pair
            return False

        if len(unique_values) > (self.MAXIMUM_CARDS - 2):
            # cannot have more than 3 unique values for two pair
            return False

        # For each unique value, check that there is at least 2 of a kind for 2 of them
        pairs = self.get_pairs()

        # Can't have three pair or one pair - consistency check
        if not pairs or len(pairs) != 2:
            return False

        # Which is the highest pair? This becomes the 'multiple' property
        # Then the other pair, followed by highest card, goes into rank
        pairs.sort(reverse=True)
        self.multiple = pairs[0]
        self.rank = [pairs[1]]

        # If we have a third value (fifth card), append it to the rank
        # As there will only be one card left, we can use the unique set and just
        # add one value to the end.
        unique_values.remove(self.multiple)
        unique_values.remove(self.rank[0])
        if len(unique_values) != 0:
            self.rank.append(unique_values.pop())

        return True

    def get_pairs(self):
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        card_values = self.get_card_values()
        unique_values = self.get_unique_card_values()

        if len(unique_values) == self.MAXIMUM_CARDS:
            # must have at least one duplicate value in the hand
            return False

        pairs = []
        for value in unique_values:
            if card_values.count(value) >= 2:       # pair also satisfied by n-of-kind
                pairs.append(value)

        return pairs

    def check_pair(self):
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        unique_values = self.get_unique_card_values()
        card_values = self.get_card_values()

        pairs = self.get_pairs()
        if not pairs or len(pairs) < 1:
            return False

        # TODO: at this point, we could still have two pairs; decide how to handle
        # this has already been somewhat documented

        # Take first pair as multiple
        self.multiple = pairs[0]

        # Remove known pair from unique list of values
        unique_values.remove(self.multiple)

        # Set rank with rest of card values, sorted by reverse order
        rank_values = list(unique_values)
        rank_values.sort(reverse=True)
        self.rank = rank_values

        return True

    def check_high_card(self):
        if not self.cards or not len(self.cards) == self.MAXIMUM_CARDS:
            return False

        # We always at least have a high card in this case.
        card_values = self.get_card_values()
        card_values.sort(reverse=True)
        self.multiple = 0
        self.rank = card_values

        return True


