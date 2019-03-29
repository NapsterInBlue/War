from war.game import Game
import time

if __name__ == '__main__':
    t = time.time()
    for i in range(100):
        g = Game(i)
        while not g.table.game_over:
            g.run_turn()

    print(time.time() - t)
