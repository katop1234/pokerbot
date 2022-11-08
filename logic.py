# Backend
from helpers import *
import time

test_hand = Hand(Card("A", "spades"),
                 Card("10", "spades"))

print("MY CARDS", test_hand)
print("--------")

test_cards_on_board = []

print("CARDS ON BOARD", test_cards_on_board)
print("--------")

a = time.time()
NUM_ITERATIONS = 100000

print(
    "Probability of having the best hand:",
    monte_carlo_winning_chance_estimator(hand=test_hand,
                                         num_opponents=6,
                                         cards_on_board=test_cards_on_board,
                                         iterations=NUM_ITERATIONS,
                                         verbose=False)
)

print("iterations per second", NUM_ITERATIONS / (time.time() - a))
