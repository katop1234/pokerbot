# Backend
from helpers import *
import time

test_hand = Hand(Card("A", "spades"),
                 Card("K", "diamonds"))

print("MY CARDS", test_hand)
print("--------")

test_cards_on_board = [Card("A", "hearts"),
                       Card("4", "clubs"),
                       Card("10", "diamonds")]

print("CARDS ON BOARD", test_hand)
print("--------")

a = time.time()
NUM_ITERATIONS = 3500

print(
    "Probability of having the best hand:",
    monte_carlo_winning_chance_estimator(hand=test_hand,
                                         num_opponents=4,
                                         cards_on_board=test_cards_on_board,
                                         iterations=NUM_ITERATIONS,
                                         verbose=False)
)

print("iterations per second", NUM_ITERATIONS / (time.time() - a))