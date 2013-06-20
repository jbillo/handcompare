import card

class Hand():

    cards = []

    def add_card(self, card_obj):
        # TODO: This is not exactly Python style; we could check attributes instead
        # (philosophy of duck typing)
        if not isinstance(card_obj, card.Card):
            raise ValueError("Must provide Card object to Hand")

        self.cards.append(card_obj)
        return True


