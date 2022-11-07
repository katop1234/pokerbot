# Backend
from helpers import *

test_hand = Hand(Card("A", "spades"),
                 Card("K", "diamonds"))

print("MY CARDS", test_hand)
print("--------")

test_cards_on_board = [Card("A", "hearts"),
                       Card("4", "clubs"),
                       Card("10", "diamonds")]

print(
    monte_carlo_winning_chance_estimator(hand=test_hand,
                                         num_opponents=4,
                                         cards_on_board=test_cards_on_board,
                                         iterations=1000)
)
