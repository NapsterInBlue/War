import os
import re
import itertools
from itertools import islice

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd


def get_game_number(fname):
    number = int(re.findall('data(\d+)\.txt', fname)[0])
    return number


def load_whole_games(num_files=None):
    files = [x for x in os.listdir('data') if not x.startswith('.git')]
    li = []

    for file in islice(files, num_files):
        with open('data/' + file, 'r') as f:
            game_num = get_game_number(file)

            df = pd.read_csv(f, delimiter=' ', header=None,
                             names=['num_a', 'num_b', 'num_aces_a', 'num_aces_b',
                                    'num_kings_a', 'num_kings_b', 'win_first_round', 'wars'],
                             na_values='None')
            df['game'] = game_num

            li.append(df)

    df = pd.concat(li, axis=0, ignore_index=True)
    df['game'] = pd.to_numeric(df['game'])

    del df['win_first_round']

    return df



def parse_header_footer(header, footer):
    _, _, aces, _, kings, *_ = header.split()
    num_a, num_b, *_ = footer.split()

    a_won = int(num_a) > int(num_b)

    return (int(aces), int(kings), a_won)



def get_game_summaries(num_files=None):
    files = [x for x in os.listdir('data') if not x.startswith('.git')]
    li = []

    for file in islice(files, num_files):
        with open('data/' + file, 'rb') as f:
            first = f.readline()

            game_num = get_game_number(file)

            ## pesky bit of code to get a_won_first_round
            found_val = False
            while not found_val:
                line = f.readline()
                vals = str(line).split(' ')
                try:
                    if vals[-2] == 'True':
                        found_val = True
                        a_won_first = True
                    if vals[-2] == 'False':
                        found_val = True
                        a_won_first = False
                    a, b, *_ = vals
                except IndexError:
                    a_won_first = a > b
                    break


            f.seek(-2, os.SEEK_END)
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)
            last = f.readline()

            result = parse_header_footer(first, last)
            li.append([game_num, *result, a_won_first])

    df = pd.DataFrame(li, columns=['game', 'a_starting_aces',
                                   'a_starting_kings',
                                   'a_won', 'a_won_first_round'])

    return df


def get_game_lengths(num_files=None):
    files = [x for x in os.listdir('data') if not x.startswith('.git')]
    li = []

    for file in islice(files, num_files):
        with open('data/' + file, 'rb') as f:
            game_num = get_game_number(file)
            for j, line in enumerate(f):
                pass

            li.append((game_num, j))

    df = pd.DataFrame(li, columns=['game', 'turns'])
    return df



def load_one_game(game_number):
    with open('data/data' + str(game_number) + '.txt') as f:
        df = pd.read_csv(f, delimiter=' ', header=None,
                         names=['num_a', 'num_b', 'num_aces_a', 'num_aces_b',
                                'num_kings_a', 'num_kings_b',
                                'win_first_round', 'wars'],
                         na_values='None')
        del df['win_first_round']

    return df


def plot_game_history(game_number, aces_and_kings=False):
    game = load_one_game(game_number).reset_index()
    wars = game[game['wars'] != 0].index

    fig, ax = plt.subplots(figsize=(18, 10))
    ax.plot(game['num_a'])

    ax2 = ax.twinx()
    if aces_and_kings:
        loc = matplotlib.ticker.MultipleLocator(1)
        ax2.yaxis.set_major_locator(loc)

        ax2.plot(game['num_aces_a'], linewidth=3, c='g', label='Aces')
        ax2.plot(game['num_kings_a'], linewidth=1, c='k', label='Kings')




        ax.set_ylabel('Card Count', fontsize=12)
        ax.set_xlabel('Turn Count', fontsize=16)
        ax2.set_ylabel('King/Ace Count', fontsize=12)

    for war in wars:
        ax.axvline(war, color='red', alpha=.5, dashes=(1, 1))

    for war in islice(wars, 1):
        ax2.axvline(war, color='red', alpha=.5, dashes=(1, 1), label='WAR!')
    ax2.legend(fontsize=16, loc=3)

    return ax2


def starting_cards_heatmap(df):
    fig, ax = plt.subplots(figsize=(10, 10))
    cax = ax.matshow(df.values)
    fig.colorbar(cax);
    ax.set_xlabel('Starting Kings', fontsize=24)
    ax.set_ylabel('Starting Aces', fontsize=24);
    plt.tight_layout()
    return ax


def plot_wins_vs_losses(whole_games, num_games, linealpha, markeralpha=1,
                        xlim=None, additional_title=''):
    fig, ax = plt.subplots(figsize=(18, 10))

    color_dict = {True: 'g', False: 'r'}

    gb = whole_games.groupby('game')
    for name, group in itertools.islice(gb, num_games):
        num_turns = len(group)
        last_turn = group.tail(1)
        result = group['a_won'].iloc[0]

        ax.plot(range(num_turns), group['num_a'], color=color_dict[result], alpha=linealpha)
        ax.plot(num_turns, last_turn['num_a'], color=color_dict[result], marker='o',
                alpha=markeralpha)


    ax.set_ylabel("Cards in Player A's hand", fontsize=16)
    ax.set_xlabel("Number of Turns", fontsize=16)

    title = f"{num_games} Games of War " + str(additional_title)
    ax.set_title(title, fontsize=24)

    custom_lines = [matplotlib.lines.Line2D([0], [0], color='r', lw=2),
                    matplotlib.lines.Line2D([0], [0], color='g', lw=2)]
    ax.legend(custom_lines, ['Loss', 'Win'], fontsize=16, loc='best')

    ax.set_xlim(xlim)

    return ax
