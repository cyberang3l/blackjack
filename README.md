# Blackjack

This is a blackjack python program with a very simplified set of rules.

At the moment, the program only supports autoplaying with either a single shuffled deck, or a list of cards provided with the command line option `--file`. A `--batch` option has also been added that will autoplay more than one games and print some very basic statistics.

Comments with some basic explanation have been added in all the different classes and functions in the code.


### Dependencies

* Python 3.4


### How to run the program

* First clone the repository.
* Execute the unit tests: `python3 -m unittest discover -v test` (The `run_tests.sh` script will execute exactly the same command).
* Check the help page of the main program: `python3 blackjack.py --help`
* Autoplay a single game: `python3 blackjack.py`


####Different execution modes and sample output:

Execute the unit tests:
```no-highlight
$ ./run_tests.sh 
test_rules (test_blackjack.blackjackRuleTests) ... ok
test_card_pick (test_deck.deckTests) ... ok
test_deck_generation (test_deck.deckTests) ... ok
test_shoe_setup (test_deck.deckTests) ... ok
test_suit_generation (test_deck.deckTests) ... ok
test_card_counting (test_player.cardCountingTests) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.004s

OK
```

Plain execution of the main program. A single deck is generated, shuffled, and one round is played between the Dealer and Sam. The winner is printed on top:
```ruby
$ python3 blackjack.py
dealer
dealer: SQ, C10 (Total: 20)
   sam: HJ, C8 (Total: 18)
```

Setup the shoe and play. Call the program with the `--file` option and a valid `cardlist` file (check the `deck.cardlist` file included in this repository to see how a valid cardlist looks like):
```ruby
$ python3 blackjack.py --file deck.cardlist
sam
dealer: D5, HQ, S8 (Total: 23)
   sam: CA, H9 (Total: 20)
```

Batch autoplay. Call the program with the `--batch` option and provide the number of rounds that you want to play. In the following example 10 rounds are played:
```ruby
$ python3 blackjack.py --batch 10
Played 10 rounds
-------------------------------------------------
                        dealer            sam
 average_points           19.4           19.4
   total_points            194            194
         winner              5              5
```
