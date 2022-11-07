from helpers import *

# variables that i'll use later
does_not_exist = RankObject()
NUM_ITERATIONS = 10000
epsilon = 0.015

''''''
### TEST SUITE ###
''''''

def test_is_royal_flush():
    cards_to_test_royal_flush = [
        Card("K", "spades"),
        Card("10", "spades"),
        Card("J", "spades"),
        Card("A", "spades"),
        Card("Q", "spades"),
        Card("A", "hearts"),
        Card("10", "hearts")
    ]

    assert royal_flush_value(cards_to_test_royal_flush) != does_not_exist

    bad_cards_to_test_royal_flush = [
        Card("K", "spades"),
        Card("10", "spades"),
        Card("J", "spades"),
        Card("9", "spades"),
        Card("Q", "spades"),
        Card("A", "hearts"),
        Card("10", "hearts")
    ]

    assert royal_flush_value(bad_cards_to_test_royal_flush) == does_not_exist

test_is_royal_flush()

def test_monte_carlo_estimator():

    test_hand = Hand(Card("A", "spades"),
                     Card("K", "diamonds"))

    test_cards_on_board = [Card("A", "hearts"),
                           Card("4", "clubs"),
                           Card("10", "diamonds")]

    p_hat = monte_carlo_winning_chance_estimator(hand=test_hand,
                                         num_opponents=4,
                                         cards_on_board=test_cards_on_board,
                                         iterations=NUM_ITERATIONS,
                                         verbose=False)

    p = 0.61
    q = 1 - p
    n = NUM_ITERATIONS
    _2_sd = 2 * (n * p * q) ** 0.5
    assert p - _2_sd <= p <= p + _2_sd, "this should fail 0.3% of the time"

test_monte_carlo_estimator()

def test_monte_carlo_estimator2():
    test_hand = Hand(Card("A", "spades"),
                     Card("A", "diamonds"))

    test_cards_on_board = [Card("A", "hearts"),
                           Card("4", "clubs"),
                           Card("10", "diamonds")]

    p = monte_carlo_winning_chance_estimator(hand=test_hand,
                                             num_opponents=6,
                                             cards_on_board=test_cards_on_board,
                                             iterations=NUM_ITERATIONS,
                                             verbose=False)

    p = 0.822
    q = 1 - p
    n = NUM_ITERATIONS
    _2_sd = 2 * (n * p * q) ** 0.5
    assert p - _2_sd <= p <= p + _2_sd, "this should fail 0.3% of the time"

test_monte_carlo_estimator2()

def test_monte_carlo_estimator3():
    test_hand = Hand(Card("A", "spades"),
                     Card("2", "spades"))

    test_cards_on_board = []

    p = monte_carlo_winning_chance_estimator(hand=test_hand,
                                             num_opponents=8,
                                             cards_on_board=test_cards_on_board,
                                             iterations=NUM_ITERATIONS,
                                             verbose=False)

    p = 0.166
    q = 1 - p
    n = NUM_ITERATIONS
    _2_sd = 2 * (n * p * q) ** 0.5
    assert p - _2_sd <= p <= p + _2_sd, "this should fail 0.3% of the time"


test_monte_carlo_estimator3()

def test_monte_carlo_estimator3():
    test_hand = Hand(Card("7", "spades"),
                     Card("2", "diamonds"))

    test_cards_on_board = []

    p = monte_carlo_winning_chance_estimator(hand=test_hand,
                                             num_opponents=3,
                                             cards_on_board=test_cards_on_board,
                                             iterations=NUM_ITERATIONS,
                                             verbose=False)

    p = 0.159
    q = 1 - p
    n = NUM_ITERATIONS
    _2_sd = 2 * (n * p * q) ** 0.5
    assert p - _2_sd <= p <= p + _2_sd, "this should fail 0.3% of the time"

test_monte_carlo_estimator3()

def test_monte_carlo_estimator4():
    test_hand = Hand(Card("5", "spades"),
                     Card("5", "diamonds"))

    test_cards_on_board = []

    p1 = monte_carlo_winning_chance_estimator(hand=test_hand,
                                             num_opponents=4,
                                             cards_on_board=test_cards_on_board,
                                             iterations=NUM_ITERATIONS,
                                             verbose=False)

    p2 = monte_carlo_winning_chance_estimator(hand=test_hand,
                                              num_opponents=4,
                                              cards_on_board=test_cards_on_board,
                                              iterations=NUM_ITERATIONS,
                                              verbose=False)

    q1 = 1 - p1
    n = NUM_ITERATIONS
    _2_sd = 2 * (n * p1 * q1) ** 0.5
    assert p1 - _2_sd <= p2 <= p1 + _2_sd, "this should fail 0.3% of the time. " \
                                           "the probabilities should not change" \
                                           "significantly between two estimates" \
                                           " of the same parameter."

test_monte_carlo_estimator3()

print("All tests passed ✅")
