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

if __name__ == "__main__":
    deck = Deck() # Use a single deck with the default card labels

    # Reads and extracts a comma separated list of cards from a file.
    # Doesn't bother making any format checks (if the file is not comma
    # separated, or having junk etc) because the Deck class makes thorough
    # card checks. If the format is not good and garbage is passed, the
    # issue will be captured by the deck validation code.
    input_cards = ''
    if args.file:
        with args.file as f:
            input_cards = [card.strip() for card in f.read().split(",")]

        if isinstance(input_cards, list):
            # Remove blank entries that may be inserted from trailing commas
            input_cards = list(filter(None, input_cards))


    if input_cards:
        # If input_cards have been provided by the user, make sure that
        # these cards will be picked first from the shoe in the given order.
        deck.setup_the_shoe(input_cards)
    else:
        # Shuffle the deck
        deck.shuffle_shoe()


    # Just use two players. The dealer and one normal player
    dealer = Player('dealer', deck, Player.ROLE.DEALER)
    player = Player('sam', deck)

    bj = blackjack(deck, dealer, player)

    if args.batch:
        bj.init_stats()
        bj.autoplay(args.batch, True)
        bj.print_stats()
    else:
        bj.autoplay()
