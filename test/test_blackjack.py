import unittest
from bj.Player import Player
from bj.Deck import Deck
from bj.BlackJack import blackjack

# The main blackjack class is responsible for rules of the
# game and coordination (who picks a card, who wins etc).
# So in this test we test the rules.

def extract_winner_and_whoDraws(d):
    assert('winner' in d.keys())
    assert('who_draws' in d.keys())

    return d['winner'], d['who_draws']

class blackjackRuleTests(unittest.TestCase):

    def test_rules(self):
        deck = Deck(num_decks = 1, suit_prefixes = ["C", "D", "H", "S"])
        player = Player('sam', deck)
        dealer = Player('dealer', deck, Player.ROLE.DEALER)
        bj = blackjack(deck, dealer, player)

        #---------------------------------------------------------------------
        # Check if both players have 21 at start (with two cards). Player wins.
        player.hand = ['SA', 'SJ']
        dealer.hand = ['HA', 'HK']
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, player, "Dealer won? Something is wrong")
        self.assertEqual(who_draws, None)

        #---------------------------------------------------------------------
        # Check if both players have 22 at start (with two cards). Dealer wins.
        player.hand = ['SA', 'CA']
        dealer.hand = ['HA', 'DA']
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, dealer, "Player won? Something is wrong")
        self.assertEqual(who_draws, None)

        #---------------------------------------------------------------------
        # In any case that the player has 21 and dealer anything else,
        # player wins then.
        player.hand = ['SA', 'S10']
        dealer.hand = ['HA', 'SA'] # dealer 22 with first pick
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, player, "Dealer won? Something is wrong")
        self.assertEqual(who_draws, None)

        player.hand = ['SA', 'S10']
        dealer.hand = ['HA', 'H9'] # dealer less than 21
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, player, "Dealer won? Something is wrong")
        self.assertEqual(who_draws, None)

        player.hand = ['SA', 'S10']
        dealer.hand = ['H10', 'H10', 'H2'] # dealer more than 21
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, player, "Dealer won? Something is wrong")
        self.assertEqual(who_draws, None)

        #---------------------------------------------------------------------
        # If dealer has 21 and the player has anything else other than 21.
        # Dealer wins.
        player.hand = ['SA', 'S10', 'S5']
        dealer.hand = ['HA', 'H10']
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, dealer, "Player won? Something is wrong")
        self.assertEqual(who_draws, None)

        #---------------------------------------------------------------------
        # If dealer has higher than player, but not 21, dealer wins.
        player.hand = ['S10', 'S3', 'S5']
        dealer.hand = ['H10', 'H4', "H6"]
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, dealer, "Player won? Something is wrong")
        self.assertEqual(who_draws, None)

        #---------------------------------------------------------------------
        # If player has less than 17, player draws card
        player.hand = ['S10', 'S3', 'S2']
        dealer.hand = ['H10', 'H4', "H6"]
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, None)
        self.assertEqual(who_draws, player)

        #---------------------------------------------------------------------
        # If the dealer has less than the player, dealer draws card
        player.hand = ['S10', 'S3', 'S6']
        dealer.hand = ['H10', 'H4', "H2"]
        winner, who_draws = extract_winner_and_whoDraws(bj.find_winner())
        self.assertEqual(winner, None)
        self.assertEqual(who_draws, dealer)

        # TODO:
        # Define what happens if at the initial pick Dealer starts with 22 (two aces)
        # and player starts with less than 21 in this simplified version of the game?
        # At the moment the dealer loses (but probably this is unfair since this
        # is the first pick anyway)
