#!/usr/bin/env python3

from bj.Deck import Deck
from bj.Player import Player
from bj.BlackJack import blackjack

if __name__ == "__main__":
    # Use a single deck
    deck = Deck()
    # Shuffle the deck (The deck is shuffled once on each shoe
    # initialization, but reshuffling doesn't hurt)
    deck.shuffle_shoe()


    # Just use two players. The dealer and one normal player
    dealer = Player('dealer', deck, Player.ROLE.DEALER)
    player = Player('sam', deck)

    bj = blackjack(deck, dealer, player)

    bj.autoplay()
