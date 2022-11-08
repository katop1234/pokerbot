from helpers import *
import inspect

# variables that i'll use later
does_not_exist = RankObject()
NUM_ITERATIONS = 10000
# todo add functionality to just plug in confidence value instead of raw SD

''''''
### TEST SUITE ###
''''''

def test_royal_flush_value():
    cards_to_test_royal_flush = [
        Card("K", "spades"),
        Card("10", "spades"),
        Card("J", "spades"),
        Card("A", "spades"),
        Card("Q", "spades"),
        Card("A", "hearts"),
        Card("10", "hearts")
    ]

    assert royal_flush_value(cards_to_test_royal_flush) == RankObject("royal_flush", "A")

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


test_royal_flush_value()

def test_straight_value():
    cards_to_test = [
        Card("2", "clubs"),
        Card("5", "diamonds"),
        Card("4", "spades"),
        Card("A", "diamonds"),
        Card("3", "spades"),
        Card("6", "hearts"),
        Card("K", "hearts")
    ]

    assert straight_value(cards_to_test) == RankObject("straight", "6")

    cards_to_test = [
        Card("A", "spades"),
        Card("2", "spades"),
        Card("3", "spades"),
        Card("4", "spades"),
        Card("6", "spades"),
        Card("7", "hearts"),
        Card("8", "hearts")
    ]

    assert straight_value(cards_to_test) == does_not_exist

test_straight_value()

def test_four_of_a_kind_value():
    cards_to_test = [
        Card("2", "clubs"),
        Card("2", "diamonds"),
        Card("4", "spades"),
        Card("A", "diamonds"),
        Card("2", "spades"),
        Card("6", "hearts"),
        Card("2", "hearts")
    ]

    assert four_of_a_kind_value(cards_to_test) == RankObject("four_of_a_kind", "2", "A")

    cards_to_test = [
        Card("2", "spades"),
        Card("2", "diamonds"),
        Card("2", "clubs"),
        Card("3", "spades"),
        Card("3", "diamonds"),
        Card("3", "clubs"),
        Card("4", "hearts")
    ]

    assert four_of_a_kind_value(cards_to_test) == does_not_exist

test_four_of_a_kind_value()

def test_full_house_value():
    cards_to_test = [
        Card("A", "clubs"),
        Card("A", "diamonds"),
        Card("A", "spades"),
        Card("2", "diamonds"),
        Card("2", "spades"),
        Card("2", "hearts"),
        Card("3", "hearts")
    ]

    assert full_house_value(cards_to_test) == RankObject("full_house", "A", "2")

    cards_to_test = [
        Card("A", "clubs"),
        Card("3", "diamonds"),
        Card("A", "spades"),
        Card("2", "diamonds"),
        Card("2", "spades"),
        Card("2", "hearts"),
        Card("3", "hearts")
    ]

    assert full_house_value(cards_to_test) == RankObject("full_house", "2", "A")

    cards_to_test = [
        Card("A", "clubs"),
        Card("A", "diamonds"),
        Card("A", "spades"),
        Card("K", "diamonds"),
        Card("K", "spades"),
        Card("K", "hearts"),
        Card("3", "hearts")
    ]

    assert full_house_value(cards_to_test) == RankObject("full_house", "A", "K")

    cards_to_test = [
        Card("A", "spades"),
        Card("A", "diamonds"),
        Card("A", "clubs"),
        Card("A", "hearts"),
        Card("2", "diamonds"),
        Card("3", "clubs"),
        Card("4", "hearts")
    ]
    assert full_house_value(cards_to_test) == does_not_exist

test_full_house_value()

def test_flush_value():
    cards_to_test = [
        Card("2", "clubs"),
        Card("3", "clubs"),
        Card("4", "clubs"),
        Card("5", "clubs"),
        Card("6", "clubs"),
        Card("7", "clubs"),
        Card("A", "clubs")
    ]

    assert flush_value(cards_to_test) == RankObject("flush", "A")

    cards_to_test = [
        Card("2", "spades"),
        Card("3", "spades"),
        Card("4", "spades"),
        Card("5", "spades"),
        Card("6", "diamonds"),
        Card("7", "diamonds"),
        Card("8", "diamonds")
    ]

    assert flush_value(cards_to_test) == does_not_exist

test_flush_value()
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
    _2_sd = 2 * (p * q / n) ** 0.5
    if not p - _2_sd <= p_hat <= p + _2_sd:
        print("expected value between", p - _2_sd, "and", p + _2_sd, "got", p_hat)

test_monte_carlo_estimator()

def test_monte_carlo_estimator2():
    test_hand = Hand(Card("A", "spades"),
                     Card("A", "diamonds"))

    test_cards_on_board = [Card("A", "hearts"),
                           Card("4", "clubs"),
                           Card("10", "diamonds")]

    p_hat = monte_carlo_winning_chance_estimator(hand=test_hand,
                                             num_opponents=6,
                                             cards_on_board=test_cards_on_board,
                                             iterations=NUM_ITERATIONS,
                                             verbose=False)

    p = 0.822
    q = 1 - p
    n = NUM_ITERATIONS
    _2_sd = 2 * (n * p * q) ** 0.5
    if not p - _2_sd <= p_hat <= p + _2_sd:
        print("expected value between", p - _2_sd, "and", p + _2_sd, "got", p_hat)
        print("FAILED", inspect.stack()[0][3])

test_monte_carlo_estimator2()

def test_monte_carlo_estimator3():
    test_hand = Hand(Card("A", "spades"),
                     Card("2", "spades"))

    test_cards_on_board = []

    p_hat = monte_carlo_winning_chance_estimator(hand=test_hand,
                                             num_opponents=8,
                                             cards_on_board=test_cards_on_board,
                                             iterations=NUM_ITERATIONS,
                                             verbose=False)

    p = 0.166
    q = 1 - p
    n = NUM_ITERATIONS
    _2_sd = 2 * (p * q / n) ** 0.5
    if not p - _2_sd <= p_hat <= p + _2_sd:
        print("expected value between", p - _2_sd, "and", p + _2_sd, "got", p_hat)
        print("FAILED", inspect.stack()[0][3])

test_monte_carlo_estimator3()

def test_monte_carlo_estimator4():
    test_hand = Hand(Card("7", "spades"),
                     Card("2", "diamonds"))

    test_cards_on_board = []

    p_hat = monte_carlo_winning_chance_estimator(hand=test_hand,
                                             num_opponents=3,
                                             cards_on_board=test_cards_on_board,
                                             iterations=NUM_ITERATIONS,
                                             verbose=False)

    p = 0.159
    q = 1 - p
    n = NUM_ITERATIONS
    _2_sd = 2 * (p * q / n) ** 0.5
    if not p - _2_sd <= p_hat <= p + _2_sd:
        print("expected value between", p - _2_sd, "and", p + _2_sd, "got", p_hat)
        print("FAILED", inspect.stack()[0][3])

test_monte_carlo_estimator4()

def test_monte_carlo_estimator5():
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
    _2_sd = 2 * (p1 * q1 / n) ** 0.5
    if not p1 - _2_sd <= p2 <= p1 + _2_sd:
        print("expected value between", p1 - _2_sd, "and", p1 + _2_sd, "got", p2)
        print("FAILED", inspect.stack()[0][3])
        print( "this should fail 0.3% of the time. " \
               "the probabilities should not change " \
               "significantly between two estimates" \
               " of the same parameter.")

test_monte_carlo_estimator5()

print("All tests passed ✅")
