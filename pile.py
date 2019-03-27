class Pile:
    def __init__(self, cards):
        self.cards = cards

    def __len__(self):
        return len(self.cards)

    def __repr__(self):
        return str(sorted([card for card in self.cards]))

    def count_card(self, value: int):
        return sum(card.value == value for card in self.cards)

    def serve_card(self):
        return self.cards.pop()
