#!/usr/bin/env python3

from bj.Deck import Deck
from bj.Player import Player
from bj.BlackJack import blackjack
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",
                    type = argparse.FileType('r', encoding='UTF-8'),
                    help = "File containing a deck of cards in the following format: CA, D4, H7, SJ,..., S5, S9, D10")

args = parser.parse_args()

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

    bj.autoplay()
