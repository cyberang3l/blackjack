import unittest
from bj.Deck import Deck

# Most of the counting and card validation is happening in the Deck
# class, so here we implement some tests to test the correct generation
# of card label, convertion of card to numeric values etc.

class deckTests(unittest.TestCase):

    #---------------------------------------------------------------------
    def test_suit_generation(self):
        #              A , 2, 3, 4, 5, 6, 7, 8, 9, 10, J , Q , K
        card_values = [11, 2, 3, 4 ,5 ,6 ,7 ,8 ,9 ,10, 10, 10, 10]

        SPADES_suit_cards = ["SPADES-A", "SPADES-2", "SPADES-3", "SPADES-4",
                             "SPADES-5", "SPADES-6", "SPADES-7", "SPADES-8",
                             "SPADES-9", "SPADES-10", "SPADES-J", "SPADES-Q", "SPADES-K"]

        C_suit_cards = ["CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK"]
        D_suit_cards = ["DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK"]
        H_suit_cards = ["HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", 'HK']
        S_suit_cards = ["SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK"]

        deck = Deck()

        for label in ["SPADES-", "C", "D", "H", "S"]:
            with self.subTest("The label '{}' introduced some problems!".format(label)):
                suit = deck._generate_suit(label)
                # First test if correct labels are getting generated
                if (label == "SPADES-"):
                    self.assertListEqual(suit, SPADES_suit_cards)
                elif (label == "C"):
                    self.assertListEqual(suit, C_suit_cards)
                elif (label == "D"):
                    self.assertListEqual(suit, D_suit_cards)
                elif (label == "H"):
                    self.assertListEqual(suit, H_suit_cards)
                elif (label == "S"):
                    self.assertListEqual(suit, S_suit_cards)

                self.assertEqual(len(suit), 13)

                # Then check if the extracted numeric value from each of the generated
                # cards is correct
                self.assertListEqual(card_values, [deck.get_card_value(card) for card in suit])

    #---------------------------------------------------------------------
    def test_deck_generation(self):
        deck = Deck(num_decks=1, suit_prefixes=["C", "D", "H", "S"])

        all_cards_single_deck = ["CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK",
                                 "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK",
                                 "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK",
                                 "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK"]

        # Now test the deck generation
        cards_in_deck = 52

        # One deck must be having 52 cards.
        deck_1 = deck._generate_deck()
        self.assertEqual(len(deck_1), cards_in_deck)
        self.assertListEqual(deck_1, all_cards_single_deck)

        playing_deck_1 = deck.generate_playing_deck()
        self.assertEqual(len(playing_deck_1), cards_in_deck)
        self.assertListEqual(playing_deck_1, all_cards_single_deck)

        # Two decks must be having 104 cards
        playing_deck_2 = deck.generate_playing_deck(2)
        self.assertEqual(len(playing_deck_2), 104)
        self.assertListEqual(playing_deck_2, all_cards_single_deck * 2)

        # Six decks must be having 312 cards
        playing_deck_6 = deck.generate_playing_deck(6)
        self.assertEqual(len(playing_deck_6), 312)
        self.assertListEqual(playing_deck_6, all_cards_single_deck * 6)

    #---------------------------------------------------------------------
    def test_shoe_setup(self):
        # Initial show
        shoe = ["CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK",
                "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK",
                "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK",
                "SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK"]

        # The cards to feed the shoe with (set it up)
        card_feed = ['C6', 'H8', 'S5', 'CA', 'DJ']

        # How the shoe should look after the setup
        shoe_set = ["C2", "C3", "C4", "C5", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK",
                    "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DQ", "DK",
                    "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H9", "H10", "HJ", "HQ", "HK",
                    "SA", "S2", "S3", "S4", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK",
                    'DJ', 'CA', 'S5', 'H8', 'C6']

        deck = Deck(num_decks = 1, suit_prefixes=["C", "D", "H", "S"])

        # Ensure the original shoe looks like the well known shoe from this test case
        deck.shoe = shoe[:]

        deck.setup_the_shoe(card_feed)

        self.assertListEqual(shoe_set, deck.shoe)

    #---------------------------------------------------------------------
    def test_card_pick(self):
        shoe = ["C2", "C3", "C4", "C5", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK",
                "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DQ", "DK",
                "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H9", "H10", "HJ", "HQ", "HK",
                "SA", "S2", "S3", "S4", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK",
                'DJ', 'CA', 'S5', 'H8', 'C6']

        deck = Deck(num_decks=1, suit_prefixes=["C", "D", "H", "S"])

        deck.shoe = shoe[:]
        self.assertListEqual(shoe, deck.shoe)

        self.assertEqual(deck.pick_card(), 'C6')
        self.assertEqual(deck.pick_card(), 'H8')
        self.assertEqual(deck.pick_card(), 'S5')
        self.assertEqual(deck.pick_card(), 'CA')
        self.assertEqual(deck.pick_card(), 'DJ')

        shoe_after_picks = ["C2", "C3", "C4", "C5", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK",
                            "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DQ", "DK",
                            "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H9", "H10", "HJ", "HQ", "HK",
                            "SA", "S2", "S3", "S4", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK"]

        self.assertListEqual(deck.shoe, shoe_after_picks)
