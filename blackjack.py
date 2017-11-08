#!/usr/bin/env python3

from bj.Deck import Deck
from bj.Player import Player
from bj.BlackJack import blackjack
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--batch-play",
                    dest = 'batch',
                    metavar = "NUM",
                    default = 0,
                    type = int, help = "Execute in batch mode and return the statistics."
                    " The NUM defines the number of times to play before returning the stats.")
parser.add_argument("-f", "--file",
                    dest = 'file',
                    type = argparse.FileType('r', encoding='UTF-8'),
                    help = "File containing a deck of cards in the following format: CA, D4, H7, SJ,..., S5, S9, D10")

args = parser.parse_args()

def print_stats(stats, total_played):
    """
    A function to print some statistics
    """
    print("Played {} rounds\n"
          "-------------------------------------------------".format(total_played))

    rows = list(stats.keys())
    columns = list(stats['winner'].keys())

    row_format ="{:>15}" * (len(columns) + 1)

    rows.sort()
    columns.sort()

    print(row_format.format("", *columns))
    for stat in rows:
        p = [stats[stat][name] for name in columns]
        print(row_format.format(stat, *p))

if __name__ == "__main__":
    input_cards = ''
    if args.file:
        with args.file as f:
            input_cards = [card.strip() for card in f.read().split(",")]

    deck = Deck() # Use a single deck
    if input_cards:
        # If input_cards have been provided by the user, make sure that
        # these cards will be picked first from the shoe in the given order.
        #
        # We always pop() from the shoe when a player picks a card, so we need
        # to append the cards in reverse order.
        deck.setup_the_shoe(input_cards)
    else:
        # Shuffle the deck
        deck.shuffle_shoe()


    # Just use two players. The dealer and one normal player
    dealer = Player('dealer', deck, Player.ROLE.DEALER)
    player = Player('sam', deck)

    bj = blackjack(deck, dealer, player)

    if args.batch:
        stats = bj.autoplay(args.batch, True)
        print_stats(stats, args.batch)
    else:
        bj.autoplay()
