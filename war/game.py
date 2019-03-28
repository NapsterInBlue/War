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
        self.game_over = False

    @property
    def a_last_card(self):
        return self.a_cards[-1]

    @property
    def b_last_card(self):
        return self.b_cards[-1]

    @property
    def all_cards(self):
        return [*self.a_cards, *self.b_cards]

    def flush_cards(self):
        self.a_cards = []
        self.b_cards = []


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
        try:
            a_card = self.player_a.play_card()
            b_card = self.player_b.play_card()
        except UnboundLocalError:
            self.table.game_over = True
            return None

        print('a:', a_card)
        print('b:', b_card)
        self.table.a_cards.append(a_card)
        self.table.b_cards.append(b_card)

        in_war = False

        while not in_war:
            if self.table.a_last_card == self.table.b_last_card:
                print('war happened')
                try:
                    self.table.a_cards.append(self.player_a.play_card())
                    self.table.a_cards.append(self.player_a.play_card())
                except:
                    continue
                try:
                    self.table.a_cards.append(self.player_a.play_card())
                    self.table.b_cards.append(self.player_b.play_card())
                except:
                    continue
                try:
                    self.table.b_cards.append(self.player_b.play_card())
                    self.table.b_cards.append(self.player_b.play_card())
                except:
                    continue
                print('a:', self.table.a_last_card)
                print('b:', self.table.b_last_card)
            elif self.table.a_last_card > self.table.b_last_card:
                self.player_a.discard.cards.extend(self.table.all_cards)
                in_war = True
            else:
                self.player_b.discard.cards.extend(self.table.all_cards)
                in_war = True

        self.table.flush_cards()