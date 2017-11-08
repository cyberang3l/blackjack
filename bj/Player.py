from enum import Enum
from bj.Deck import Deck

class Player(object):
    """
    An object that identifies a player and keeps track
    of the cards in a hand
    """
    class ROLE(Enum):
        PLAYER = 0
        DEALER = 1

    def __init__(self, name, deck, role = ROLE.PLAYER):
        self.name = name
        self.role = role
        self.deck = deck
        self.hand = []

    # The role property indicates the type of the player:
    #  normal player or dealer.
    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        if role not in type(self).ROLE:
            raise Exception("\n\nThe player 'role' should get a valid role from the ROLE enum\n"
                            "'{}' passed.".format(role))
        self._role = role

    @role.getter
    def role(self):
        return self._role

    # The deck is the deck where the player is picking cards from
    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, deck):
        if not isinstance(deck, Deck):
            raise Exception("The deck for each player must be of class type Deck")
        self._deck = deck

    @deck.deleter
    def deck(self):
        del self._deck

    # The cards property holds a list with the cards of the player
    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, cards):
        self._hand = cards

    @hand.deleter
    def hand(self):
        del self._hand

    #-------------------------------------------------------------
    def clearHand(self):
        """
        We call this function in the beginning of each round in order to
        discard existing cards.
        """
        self.hand = []

    #-------------------------------------------------------------
    def pickCard(self):
        """
        Picks a card from the shoe in the deck and adds the card in the player's
        self.cards list
        """
        self.hand.append(self.deck.pick_card())

    #-------------------------------------------------------------
    def score(self):
        """
        Returns a list with the score for each card that the player
        is currently holding
        """
        return [self.deck.get_card_value(card) for card in self.hand]

    def total_score(self):
        """
        Returns the total score of the cards that the player
        is currently holding
        """
        return sum(self.score())
