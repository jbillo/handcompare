class Card():
    value = 0
    suit = ""

    def __init__(self, card_value, card_suit):
        self.value = card_value
        self.suit = card_suit

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit
