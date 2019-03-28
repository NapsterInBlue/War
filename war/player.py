from .pile import DiscardPile


class Player:
    def __init__(self, pile, table):
        self.cards = pile
        self.discard = DiscardPile()
        self.table = table

    def play_card(self):
        return self.cards.serve_card()
