from bj.Player import Player

class blackjack(object):
    #-------------------------------------------------------------
    def __init__(self, deck, dealer, player):
        #Arguments:
        #    deck: a valid deck of cards (Class type Deck)
        #    players: A list of the players that play the game.
        self.deck = deck
        self.dealer = dealer
        self.player = player
        isinstance(self.dealer, Player)
        isinstance(self.player, Player)

        if (self.deck is not self.player.deck) or (self.deck is not self.dealer.deck):
            raise Exception("The Deck should be the same for self.deck, self.dealer.deck, self.player.deck")

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player):
        if not self._is_player_role(player, Player.ROLE.PLAYER):
            raise("The active player's role must be Player.ROLE.PLAYER")
        self._player = player

    @player.deleter
    def player(self):
        del self._player

    @property
    def dealer(self):
        return self._dealer

    @dealer.setter
    def dealer(self, dealer):
        if not self._is_player_role(dealer, Player.ROLE.DEALER):
            raise("The active player's role must be Player.ROLE.DEALER")
        self._dealer = dealer

    @dealer.deleter
    def dealer(self):
        del self._dealer

    #-------------------------------------------------------------
    def _is_player_role(self, player, role):
        """
        Function to make a boolean check if a 'player's role is 'role'
        """
        if player.role == role:
            return True
        else:
            return False

    #-------------------------------------------------------------
    def initPick(self):
        """
        Makes an initial pick (draws two cards) for all the players.
        """
        self.player.pickCard()
        self.dealer.pickCard()
        self.player.pickCard()
        self.dealer.pickCard()

    #-------------------------------------------------------------
    def print_cards(self):
        """
        Prints the cards for all players
        """
        # Get the length of the longest name for alignment
        max_name_len = max(len(self.player.name), len(self.dealer.name))

        print("{:>{}}: {} (Total: {})".format(self.dealer.name,
                                              max_name_len,
                                              ", ".join(self.dealer.hand),
                                              self.dealer.total_score()))
        print("{:>{}}: {} (Total: {})".format(self.player.name,
                                              max_name_len,
                                              ", ".join(self.player.hand),
                                              self.player.total_score()))

    #-------------------------------------------------------------
    def find_winner(self):
        """
        The find_winner function will return a dict with the following information:
        {'winner':Person or None, 'who_draws':None or Person}
        If there is a winner, the winner key will hold the Person class of the winner
        (dealer or player), otherwise it will be empty. Similary, if there is no winner
        yet (thus, the winner is None) the 'who_draws' key will hold the Person class
        of the person that has to pick a card next.
        """
        # If both players pick 21, players wins
        if self.dealer.total_score() == self.player.total_score() == 21:
            return {'winner': self.player, 'who_draws': None}
        # If both players pick 22, dealer wins
        elif self.dealer.total_score() == self.player.total_score() == 22:
            return {'winner': self.dealer, 'who_draws': None}
        # If the dealer has 21,but not the player, the dealer wins
        elif self.dealer.total_score() == 21:
            return {'winner': self.dealer, 'who_draws': None}
        # If the player has 21,but not the dealer, the player wins
        elif self.player.total_score() == 21:
            return {'winner': self.player, 'who_draws': None}
        # If the players goes over 21, the dealer wins
        elif self.player.total_score() > 21:
            return {'winner': self.dealer, 'who_draws': None}
        # If the dealer goes over 21, the player wins
        elif self.dealer.total_score() > 21:
            return {'winner': self.player, 'who_draws': None}
        # If the player has less than 17, the player draws card
        elif self.player.total_score() < 17:
            return {'winner': None, 'who_draws': self.player}
        # If the player has >= 17 and dealer has less than player, the dealer picks
        elif self.player.total_score() >= 17 and self.dealer.total_score() <= self.player.total_score():
            return {'winner': None, 'who_draws': self.dealer}
        else:
            return {'winner': self.dealer, 'who_draws': None}

    #-------------------------------------------------------------
    def autoplay(self, rounds = 1):
        """
        The game will autoplay as many rounds have been told to play
        by the 'rounds' argument.

        Arguments:
         rounds: The number of rounds to play
        """
        # Initial pick for all players

        self.initPick()

        # Print the results and the winner
        res = self.find_winner()
        while not res['winner']:
            res['who_draws'].pickCard()
            res = self.find_winner()

        print(res['winner'].name)
        self.print_cards()
