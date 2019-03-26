import random

from card import Card
from pile import Pile


class Deck:
    def __init__(self):
        self.all_cards = []
        for i in range(13):
            for _ in range(4):
                self.all_cards.append(Card(i))

    def start_game(self):
        random.shuffle(self.all_cards)
        player_a = self.all_cards[:26]
        player_a = Pile(player_a)
        player_b = self.all_cards[26:]
        player_b = Pile(player_b)

        return player_a, player_b


if __name__ == '__main__':
    d = Deck()

    a, b = d.start_game()

    print(a)
