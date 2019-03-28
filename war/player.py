from .pile import DiscardPile


class Player:
    def __init__(self, pile, table):
        self.cards = pile
        self.discard = DiscardPile(self.cards)
        self.table = table

    @property
    def total_card_count(self):
        return len(self.cards) + len(self.discard)

    def play_card(self):
        if len(self.cards):
            card = self.cards.serve_card()
        elif len(self.discard):
            self.discard.shuffle_reload_deck()
            card = self.cards.serve_card()

        return card
