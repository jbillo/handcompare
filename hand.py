import card

class Hand():

    cards = []
    rank = 0

    def add_card(self, card_obj):
        # This is not conventional Python; we could check attributes instead
        # (philosophy of duck typing) and only error if needed properties not found
        if not isinstance(card_obj, card.Card):
            raise ValueError("Must provide Card object to Hand")

        self.cards.append(card_obj)
        return True



