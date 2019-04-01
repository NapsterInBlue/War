import os
from itertools import islice

import pandas as pd


def load_whole_games(num_files=None):
    files = [x for x in os.listdir('data') if not x.startswith('.git')]
    li = []

    for i, file in islice(enumerate(files), num_files):
        with open('data/' + file, 'r') as f:
            df = pd.read_csv(f, delimiter=' ', header=None,
                             names=['num_a', 'num_b', 'num_aces_a', 'num_aces_b', 
                                    'num_kings_a', 'num_kings_b', 'win_first_round', 'wars'],
                             na_values='None')
            df['game'] = i

            li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    df['game'] = pd.to_numeric(df['game'])

    del df['win_first_round']
    
    return df



def parse_header_footer(header, footer):
    _, _, aces, _, kings, *_ = header.split()
    num_a, num_b, _, _, _, _, won_first_round, *_ = footer.split()
    
    a_won = int(num_a) > int(num_b)
    
    return (int(aces), int(kings), a_won, bool(won_first_round))



def get_game_summaries(num_files=None):
    files = [x for x in os.listdir('data') if not x.startswith('.git')]
    li = []

    for i, file in islice(enumerate(files), num_files):
        with open('data/' + file, 'rb') as f:
            first = f.readline()
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
            last = f.readline()
            
            result = parse_header_footer(first, last)
            li.append([i, *result])
            
    df = pd.DataFrame(li, columns=['game', 'a_starting_aces',
                                   'a_starting_kings',
                                   'a_won', 'a_won_first_round'])

    return df


def get_game_lengths(num_files=None):
    files = [x for x in os.listdir('data') if not x.startswith('.git')]
    li = []

    for i, file in islice(enumerate(files), num_files):
        with open('data/' + file, 'rb') as f:
            for j, line in enumerate(f):
                pass

            li.append((i, j+1))

    df = pd.DataFrame(li, columns=['game', 'turns'])
    return df


def plot_game_history(game_number):
    game = whole_games[whole_games['game'] == game_number].reset_index()
    wars = game[game['wars'] == 1].index

    fig, ax = plt.subplots(figsize=(18, 10))
    ax.plot(game['num_a'])

    ax2 = ax.twinx()
    loc = matplotlib.ticker.MultipleLocator(1)
    ax2.yaxis.set_major_locator(loc)
    
    ax2.plot(game['num_aces_a'], linewidth=3, c='g', label='Aces')
    ax2.plot(game['num_kings_a'], linewidth=1, c='k', label='Kings')

    for war in wars:
        ax.axvline(war, color='red', alpha=.5, dashes=(1, 1))

    for war in islice(wars, 1):
        ax2.axvline(war, color='red', alpha=.5, dashes=(1, 1), label='WAR!')
        
    ax.set_ylabel('Card Count', fontsize=12)
    ax.set_xlabel('Turn Count', fontsize=16)
    ax2.set_ylabel('King/Ace Count', fontsize=12)
        
    ax2.legend(fontsize=16, loc=3)
    return ax2
