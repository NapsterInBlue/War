from war.game import Game

if __name__ == '__main__':
    g = Game()

    print(g.player_a.cards)

    g.run_turn()
    g.run_turn()
    g.run_turn()
    g.run_turn()

    print(g.table.a_cards)
    print(g.table.b_cards)