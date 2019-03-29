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

        self.first_round = True  # updated on first shuffle in Player

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


class Turn:
    def __init__(self, game):
        self.game_num = game.game_num

        self.num_player_a_cards = game.player_a.total_card_count
        self.num_player_b_cards = game.player_b.total_card_count

        self.num_player_a_aces = (game.player_a.cards.count_card(12)
                                  + game.player_a.discard.count_card(12))
        self.num_player_b_aces = (game.player_b.cards.count_card(12)
                                  + game.player_b.discard.count_card(12))

        self.num_player_a_kings = (game.player_a.cards.count_card(11)
                                   + game.player_a.discard.count_card(11))
        self.num_player_b_kings = (game.player_b.cards.count_card(11)
                                   + game.player_b.discard.count_card(11))

        self.num_wars = 0
        self.a_won_first_round = game.a_won_first_round

    def write_data(self):
        game_num = self.game_num
        with open('data/data{}.txt'.format(game_num), 'a') as f:
            f.write(' '.join([str(self.num_player_a_cards),
                              str(self.num_player_b_cards),
                              str(self.num_player_a_aces),
                              str(self.num_player_b_aces),
                              str(self.num_player_a_kings),
                              str(self.num_player_b_kings),
                              str(self.a_won_first_round),
                              str(self.num_wars)]))
            f.write('\n')


class Game:
    def __init__(self, game_num):
        self.game_num = game_num

        self.table = Table()
        self.all_cards = Deck().all_cards
        random.shuffle(self.all_cards)

        player_a_cards = self.all_cards[:26]
        player_a_pile = PlayerPile(player_a_cards)
        self.player_a = Player(player_a_pile, self.table)

        player_b_cards = self.all_cards[26:]
        player_b_pile = PlayerPile(player_b_cards)
        self.player_b = Player(player_b_pile, self.table)

        self.a_won_first_round = None

    def run_turn(self):
        if self.a_won_first_round is None and not self.table.first_round:
            self.a_won_first_round = (self.player_a.total_card_count
                                      > self.player_b.total_card_count)

        turn = Turn(self)
        available_cards = min(self.player_a.total_card_count, self.player_b.total_card_count)
        available_cards = min(available_cards, 3)

        if available_cards <= 1:
            self.table.game_over = True
            self.table.flush_cards()
            return None
        else:
            a_card = self.player_a.play_card()
            b_card = self.player_b.play_card()

        self.table.a_cards.append(a_card)
        self.table.b_cards.append(b_card)

        in_war = True

        while in_war:
            if self.table.a_last_card == self.table.b_last_card:
                # print('\nwar happened')
                turn.num_wars += 1

                available_cards = min(self.player_a.total_card_count, self.player_b.total_card_count)
                available_cards = min(available_cards, 3)

                if available_cards == 0:
                    self.table.game_over = True
                    if self.player_a.total_card_count > self.player_b.total_card_count:
                        self.player_a.discard.cards.extend(self.table.all_cards)
                        in_war = False

                    else:
                        self.player_b.discard.cards.extend(self.table.all_cards)
                        in_war = False

                for _ in range(available_cards):
                    self.table.a_cards.append(self.player_a.play_card())
                    self.table.b_cards.append(self.player_b.play_card())

            if self.table.a_last_card > self.table.b_last_card:
                self.player_a.discard.cards.extend(self.table.all_cards)
                in_war = False
            else:
                self.player_b.discard.cards.extend(self.table.all_cards)
                in_war = False

        self.table.flush_cards()
        turn.write_data()
