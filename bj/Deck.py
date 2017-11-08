from random import shuffle

class Deck(object):
    """
    The Deck object handles card and deck generation.
    """
    CARDS_PER_SINGLE_DECK = 52

    def __init__(self, num_decks = 1, suit_prefixes = ["C", "D", "H", "S"]):
        self.playing_deck = self.generate_playing_deck(num_decks, suit_prefixes)
        self._suit_prefixes = suit_prefixes
        self._decks_in_playing_deck = num_decks

    # The playing_deck property holds a list of all the cards in the deck.
    # Note that you should only initialize the playing_deck once, and then
    # modify and play (shuffle, draw cards from etc) with the shoe. You should only
    # change the playing_deck if you want to increase the number of card (by using more
    # decks) or change the suit labels of your cards. An update in the playing_deck
    # will reinitialize the shoe so if you modify the playing_deck in the middle of
    # the game, you will ruin your game.
    @property
    def playing_deck(self):
        return self._playing_deck

    @playing_deck.setter
    def playing_deck(self, playing_deck):
        failed_reason = self.validate_playing_deck(playing_deck)
        if failed_reason:
            raise Exception("\n\n{}.\nPlease use the generate_playing_deck() "
                            "function to generate your deck correctly.".format(failed_reason))

        self._playing_deck = playing_deck
        self.init_shoe_from_playing_deck()

    @playing_deck.deleter
    def playing_deck(self):
        del self._playing_deck

    # The shoe property holds a list of the cards that haven't been picked
    # while playing.
    @property
    def shoe(self):
        return self._shoe

    @shoe.setter
    def shoe(self, shoe):
        failed_reason = self.validate_shoe(shoe)
        if failed_reason:
            raise Exception("\n\n{}.\nPlease ensure that the shoe contains cards"
                            "that already exist in your initial (full) playing_deck".format(failed_reason))
        self._shoe = shoe

    @shoe.deleter
    def shoe(self):
        del self._shoe

    #-------------------------------------------------------------
    def _generate_suit(self, suit_string):
        """
        Generate the card labels for a complete suit (13 labels, no joker).

        Arguments:
         suit_string: The string of the suite to generate.

        Returns:
         A list with 13 labels.
        """
        suit = []
        for card in range(1, 14):
            if card == 1: suit.append("{}A".format(suit_string))
            elif card == 11: suit.append("{}J".format(suit_string))
            elif card == 12: suit.append("{}Q".format(suit_string))
            elif card == 13: suit.append("{}K".format(suit_string))
            else: suit.append("{}{}".format(suit_string, card))

        return suit

    #-------------------------------------------------------------
    def _generate_deck(self, suit_labels = ["C", "D", "H", "S"]):
        """
        Generate a single deck with four suits and 52 cards

        Arguments:
         suit_labels: The labels for each suit. All the decks will use the same
                        set of suit labels.

        Returns:
         A list that represents a single deck with 52 cards
        """
        assert isinstance(suit_labels, list), "The number of decks must be an integer."
        assert (len(suit_labels) == 4), "A suit must be having 4 labels and no duplicates. {} provided:\n   {}".format(len(suit_labels), ', '.join(suit_labels))

        deck = []
        for label in suit_labels:
            deck.extend(self._generate_suit(label))

        return deck

    #-------------------------------------------------------------
    def get_card_value(self, card):
        """
        Return the numeric (int) value of each card.

        Arguments:
         card: A card that has been generated by the generate_suit() function.

        Returns:
         An integer value. The value of the card.
        """
        value = card[-1]

        if value == "A": return 11
        elif value in ["J", "Q", "K", "0"]: return 10
        elif value == '1': raise Exception("\n\nThe card '{}' is invalid. If you need an Ace,\n"
                                           "change the label of your card to '{}A'".format(card, card[:-1]))

        return int(value)

    #-------------------------------------------------------------
    def generate_playing_deck(self, number_of_decks = 1, suit_labels = ["C", "D", "H", "S"]):
        """
        Many games require more than one playing decks.
        This function will generate a playing deck with as many decks as needed.

        Arguments:
         number_of_decks: The number of decks that the playing deck will be using.
             suit_labels: The labels for each suit. All the decks will use the same
                            set of suit labels.

        Returns:
         A list with all the cards of the playing deck.
        """
        assert isinstance(number_of_decks, int), "The number of decks must be an integer."

        playing_deck = self._generate_deck(suit_labels)
        self._decks_in_playing_deck = number_of_decks

        return playing_deck * number_of_decks

    #-------------------------------------------------------------
    def validate_playing_deck(self, deck = None):
        """
        Function to validate that all the expected cards exist in the given deck
        Note that this function validates the full set of cards. If you want to
        validate the shoe, use the validate_shoe() function.

        Arguments:
         deck: The deck to validate (a python list)

        Returns:
         An empty string if the validation passes, or a string that explains what
         went wrong with the validation otherwise.
        """
        if deck == None:
            deck = self.playing_deck

        if not isinstance(deck, list): return False
        if not (len(deck) % type(self).CARDS_PER_SINGLE_DECK == 0): return False

        full_decks_in_deck = int(len(deck) / type(self).CARDS_PER_SINGLE_DECK)

        # Count that all 13 cards from all suits exist in the deck.
        card_count = [0] * 13

        # Check the suit labels and ensure that there are exactly 4,
        # and all of them have the same number of cards
        suit_count = {}

        for card in deck:
            if not isinstance(card, str): return False
            # First check that we can extract the value from a card
            value = card[-1]
            suit = ''
            if value == "A": card_count[0] += 1
            elif value == "0": card_count[9] += 1
            elif value == "J": card_count[10] += 1
            elif value == "Q": card_count[11] += 1
            elif value == "K": card_count[12] += 1
            else:
                try:
                    i = int(value)
                    if (i == 1):
                        return "The card '{}' is invalid. If you need an Ace,\nchange the label your card to '{}A'".format(card, card[:-1])
                except ValueError:
                    return "The card '{}' is invalid".format(card)

                card_count[i-1] += 1

            if value == "0":
                suit = card[:-2]
            else:
                suit = card[:-1]

            if suit in suit_count.keys():
                suit_count[suit] += 1
            else:
                suit_count[suit] = 1

        # Some cards are missing
        if len(set(card_count)) != 1: return "Cards are missing from some suits"
        if len(set(suit_count.values())) != 1: return "Cards are missing from some suits"

        # Each deck has four suits, so since we have already counted how many individual cards
        # were found in the deck, divide by 4 to see if the cards we counted match the number of
        # decks.
        if (card_count[0] / 4 != full_decks_in_deck): return "The deck is not complete"
        if (len(suit_count.keys())) != 4: return "You must be having exactly 4 suits in a deck. No more, no less. {} found".format(len(suit_count.values()))

        return ''

    #-------------------------------------------------------------
    def validate_shoe(self, shoe = None, deck = None):
        """
        Validates the shoe against a deck. The shoe will usually not hold a
        complete set of playing_deck (because players pick cards from the shoe),
        but all the cards in the shoe should exist in the playing deck.

        Arguments:
         shoe: The shoe to validate (A list of cards)
         deck: A deck (another list of cards) to validate the shoe against.

        Returns:
         True if the validation passes, or False otherwise.
        """
        if shoe == None:
            shoe = self.shoe
        if deck == None:
            deck = self.playing_deck

        for card in shoe:
            if shoe.count(card) == 0:
                return "Card '{}' in shoe not in deck".format(card)
            elif shoe.count(card) > deck.count(card):
                return "Card '{}' in shoe exists more times than what it exists in the deck".format(card)

        return ''

    #-------------------------------------------------------------
    def setup_the_shoe(self, setup_card_list):
        """
        Cheater... This function will setup the shoe.
        Just provide a list of cards in the setup_card_list and
        they will be put on top of the shoe.

        Arguments:
         setup_card_list: The list of cards to setup the shoe
        """
        # We always pop() from the shoe when a player picks a card, so we need
        # to append the cards in reverse order.
        setup_card_list.reverse()
        for card in setup_card_list:
            try:
                self.shoe.remove(card)
            except ValueError:
                raise Exception("\n\nThat's too obvious cheating!\n"
                                "You provided a non-existing card for the deck setup: '{}'\n"
                                "A list of all possible cards follows:\n"
                                "   {}\n   {}\n   {}\n   {}".format(
                                    card, ", ".join(self._generate_suit(self._suit_prefixes[0])),
                                    ", ".join(self._generate_suit(self._suit_prefixes[1])),
                                    ", ".join(self._generate_suit(self._suit_prefixes[2])),
                                    ", ".join(self._generate_suit(self._suit_prefixes[3]))
                                ))

            self.shoe.append(card)

    #-------------------------------------------------------------
    def init_shoe_from_playing_deck(self, shuffle = False):
        """
        Copies the playing_deck in the shoe and shuffles the shoe.
        Use this function when the shoe doesn't have enough cards to pick from.
        """
        self.shoe = self.playing_deck[:]
        if shuffle:
            self.shuffle_shoe()

    #-------------------------------------------------------------
    def shuffle_shoe(self):
        """
        Shuffles the shoe
        """
        shuffle(self.shoe)

    #-------------------------------------------------------------
    def pick_card(self):
        """
        Picks one card from the shoe. If the shoe is empty, the
        shoe is reinitialized and shuffled.
        """
        if not len(self.shoe):
            self.init_shoe_from_playing_deck(True)

        return self.shoe.pop()
