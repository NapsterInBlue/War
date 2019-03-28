import random


class Pile:
    def __init__(self, cards=None):
        self.cards = cards

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return str(sorted([card for card in self.cards]))

    def count_card(self, value: int):
        return sum(card.value == value for card in self.cards)


class PlayerPile(Pile):
    def serve_card(self):
        return self.cards.pop()


class DiscardPile(Pile):
    def __init__(self, cards=None, player_pile=None):
        self.cards = cards
        self.playerPile = player_pile

    def shuffle_reload_deck(self):
        random.shuffle(self.cards)
        self.playerPile.cards = self.cards
        self.cards = []
