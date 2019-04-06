from war.game import Game
import time

import os
import glob


if __name__ == '__main__':
    t = time.time()

    files = glob.glob('/data/*')
    for f in files:
        os.remove(f)

    for i in range(100000):
        g = Game(i)
        while not g.table.game_over:
            g.run_turn()

    print(time.time() - t)
