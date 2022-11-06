# Backend
from classes import Card, Hand, Opponents
from helpers import *
import itertools
import random

all_hands = get_all_hands()
game_stages = ["pre_flop", "flop", "turn", "river"]

for num_opponents in range(1, 5+1):
    for stage in game_stages:
        for hand in all_hands:
            if stage == "pre_flop":
                pass
            elif stage == "flop":
                pass
            elif stage == "turn":
                pass
            elif stage == "river":
                pass

def monte_carlo_winning_chance_estimator(hand, num_opponents, cards_on_board, iterations=1000):
    assert type(hand) is Hand
    assert num_opponents >= 1 and num_opponents <= 10
    assert len(cards_on_board) <= 5

    valid_cards = get_remaining_cards(hand, cards_on_board)

    wins = 0
    for _ in range(iterations):
        num_cards_from_opponents = num_opponents * 2
        num_cards_left_to_reveal = 5 - len(cards_on_board)
        num_of_cards_to_sample = num_cards_left_to_reveal + num_cards_from_opponents

        cards_sampled = random.sample(valid_cards, num_of_cards_to_sample)

        simulated_opps = get_simulated_opponents_hands(cards_sampled, num_opponents)
        simulated_remaining_cards_on_board = get_simulated_cards_on_board(cards_sampled, num_cards_left_to_reveal)

        print("RANDOM CARDS TO PICK FROM", cards_sampled)
        print("OPPS", simulated_opps)
        print("REMAINING CARDS ON BOARD", simulated_remaining_cards_on_board)

        board = cards_on_board + simulated_remaining_cards_on_board

        win = 1
        for opp_hand in simulated_opps.opp_hands:
            if not my_hand_is_better(hand, opp_hand, board):
                win = 0
                break

        wins += win

        break

    return wins / iterations

test_hand = Hand(Card("A", "spades"), Card("A", "diamonds"))
test_cards_on_board = [Card("J", "hearts"), Card("3", "clubs"), Card("10", "diamonds")]
print(
    monte_carlo_winning_chance_estimator(hand=test_hand, num_opponents=3, cards_on_board=test_cards_on_board)
)