from war.game import Game

if __name__ == '__main__':
    g = Game()

    # print(g.player_a.cards)

    while not g.table.game_over:
        g.run_turn()

    # print(g.player_a.total_card_count, g.player_b.total_card_count)
    # print(g.player_a.cards, sorted(g.player_a.discard.cards))
    # print(g.player_b.cards, sorted(g.player_b.discard.cards))
