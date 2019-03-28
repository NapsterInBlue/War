from war.game import Game

if __name__ == '__main__':
    g = Game()

    print(g.player_a.cards)

    while not g.table.game_over:
        for i in range(10):
            # input()
            g.run_turn()

            print(g.player_a.discard)
            print(g.player_b.discard)

    print(g.player_a.total_card_count, g.player_b.total_card_count)