from .pile import Pile


class Player:
    def __init__(self, pile):
        self.cards = pile
        self.discard = Pile()