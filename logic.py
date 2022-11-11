# Backend
from classes import Hand, Card
from gameplay_helpers import *
from monte_carlo_helpers import get_probability_of_winning

test_hand = Hand(Card("A", "spades"),
                 Card("K", "spades"))

print("MY CARDS", test_hand)
print("--------")

test_cards_on_board = [
]

print("CARDS ON BOARD", test_cards_on_board)
print("--------")

print(
    "Probability of having the best hand:",
    get_probability_of_winning(hand=test_hand, num_opponents=5, cards_on_board=test_cards_on_board, verbose=False)
)

exit(0)

### ACTUAL GAME LOGIC ###
num_games_to_play = 20 # todo change this if you want

start_a_session()
num_games_played = 0
while num_games_played < num_games_to_play:
    wait_until_game_is_loaded()

    my_hand = get_my_hand()
    num_opponents = get_number_of_opponents()

    for betting_round in ["pre-flop", "flop", "turn", "river"]:
        wait_until_betting_round_is_loaded(betting_round)
        cards_on_board = get_cards_on_board()

        # todo add assert statements everywhere to make sure the code reads each step properly

        my_balance = get_my_balance()

        p_winning = get_probability_of_winning(hand=my_hand, num_opponents=num_opponents, cards_on_board=cards_on_board)

        wait_until_my_turn()

        num_of_villains = get_num_of_opponents_still_in()

        pot_size = get_pot_size()

        make_betting_decision(p_winning, pot_size, num_opponents, my_balance)

    num_games_played += 1
quit_session()

'''
1. only play preflop when ur hand has 90% chance of winning. otherwise fold. never bluff (zone poker).

preflop
if 90 < chance of winning < 96:
- raise up to 1-3 big blinds.
if chance of winning> 96:
- check

flop turn river
- if chance of winning ever drops below 51%, just fold
- round this to some nice big blind multiple

**randomly check some % of the time also
** replace each constant number above with an RV so its not detectable
'''


