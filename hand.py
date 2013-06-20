import card

class DuplicateCardError(Exception):
    pass

class MissingCardError(Exception):
    pass

class MaximumCardError(Exception):
    pass

class Hand():
    cards = []
    type = 0
    rank = 0

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

    # helper to clear hand of all cards
    def clear(self):
        self.cards = []
        self.rank = 0

    def get_cards(self):
        return self.cards

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
        return True


    def get_hand_type(self):
        if not self.cards or not len(self.cards) == 5:
            raise MissingCardError("Must have exactly five cards in hand")

        # Dynamically check hand types based on dictionary definitions
        for hand_type in keys(self.HAND_TYPES):
            if getattr(self, "check_%s" % hand_type)():
                self.type = self.HAND_TYPES[hand_type]
                break

        # TODO: account for situations where getattr() call fails to get function
        pass

    def check_straight_flush(self):
        # definition: five cards in sequence, all of same suit
        if not self.cards or not len(self.cards) == 5:
            return False

        current_suit = self.cards[0].get_suit()

        # check if all cards are same suit
        for card in self.cards[1:]:
            if card.get_suit() != current_suit:
                return False

        # all cards are the same suit; check if they form a sequence
        # condition 1: ace low (A = 1) - will appear as exactly 2, 3, 4, 5, 14 in values
        # condition 2: normal, no aces or ace high (A = 14)

        # we can test explicitly for condition 1:
        ace_low = True
        ace_low_values = [2, 3, 4, 5, 14]
        for card_index in range(0, len(self.cards)):
            if ace_low_values[card_index] != self.cards[card_index].get_value():
                ace_low = False
                break

        # if we have an ace low condition, rank is always 5
        # and type will be straight flush
        if ace_low:
            self.rank = 5
            return True

        prev_value = self.cards[0].get_value()
        # for each card from 2-5,
        # check if its value is exactly 1 more than its predecessor

        for card in self.cards[1:]:
            if card.get_value() != (prev_value + 1):
                return False
            prev_value = card.get_value()

        # This is a straight. The rank is the last element in the list (highest card)
        # Royal flush will bubble to the top - the ace will be in there as card[4]
        self.rank = self.cards[4].get_value()
        return True

    def check_four_of_a_kind(self):
        pass
