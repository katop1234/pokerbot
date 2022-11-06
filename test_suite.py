from helpers import *

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

    assert is_royal_flush(cards_to_test_royal_flush)

    bad_cards_to_test_royal_flush = [
        Card("K", "spades"),
        Card("10", "spades"),
        Card("J", "spades"),
        Card("9", "spades"),
        Card("Q", "spades"),
        Card("A", "hearts"),
        Card("10", "hearts")
    ]

    assert not is_royal_flush(bad_cards_to_test_royal_flush)

test_is_royal_flush()
