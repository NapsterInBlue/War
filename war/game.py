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

    def start_game(self) -> tuple:
        random.shuffle(self.all_cards)

        player_a_cards = self.all_cards[:26]
        player_a_pile = PlayerPile(player_a_cards)
        player_a = Player(player_a_pile)

        player_b_cards = self.all_cards[26:]
        player_b_pile = PlayerPile(player_b_cards)
        player_b = Player(player_b_pile)

        return player_a, player_b
