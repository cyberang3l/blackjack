import unittest
from bj.Player import Player
from bj.Deck import Deck

# The Player class is mostly a wrapper class that calls functions
# from the Deck class in order to pick cards, convert the cards to
# numeric values etc. All of these are tested in the test_deck.py.
#
# In this test we only the counting and sum based on some given cards.

class cardCountingTests(unittest.TestCase):

    def test_card_counting(self):
        deck = Deck(num_decks = 1, suit_prefixes = ["C", "D", "H", "S"])
        player = Player('sam', deck)

        # Determine score of hand
        player.hand = ['SA', 'S10']
        self.assertListEqual(player.score(), [11, 10])
        self.assertEqual(player.total_score(), 21)

        player.hand = ['SA', 'HA']
        self.assertListEqual(player.score(), [11, 11])
        self.assertEqual(player.total_score(), 22)

        player.hand = ['S2', 'S7', 'S6', 'S3']
        self.assertListEqual(player.score(), [2, 7, 6, 3])
        self.assertEqual(player.total_score(), 18)
