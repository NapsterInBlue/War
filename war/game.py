import random

from .card import Card
from .pile import PlayerPile
from .player import Player


class Deck:
    def __init__(self):
        self.all_cards = []
        for i in range(13):
            for _ in range(4):
                self.all_cards.append(Card(i))


class Table:
    def __init__(self):
        self.a_cards = []
        self.b_cards = []

    @property
    def a_last_card(self):
        return self.a_cards[-1]

    @property
    def b_last_card(self):
        return self.b_cards[-1]


class Game:
    def __init__(self):
        self.table = Table()
        self.all_cards = Deck().all_cards
        random.shuffle(self.all_cards)

        player_a_cards = self.all_cards[:26]
        player_a_pile = PlayerPile(player_a_cards)
        self.player_a = Player(player_a_pile, self.table)

        player_b_cards = self.all_cards[26:]
        player_b_pile = PlayerPile(player_b_cards)
        self.player_b = Player(player_b_pile, self.table)

    def run_turn(self):
        a_card = self.player_a.play_card()
        b_card = self.player_b.play_card()

        print('a:', a_card)
        print('b:', b_card)
        self.table.a_cards.append(a_card)
        self.table.b_cards.append(b_card)

        if self.table.a_last_card > self.table.b_last_card:
            print('a wins')