from classes import Card, Hand, Opponents
import itertools

def get_all_cards():
    raw_cards = list(itertools.product(Card.card_values, Card.suits))
    all_cards = []
    for card in raw_cards:
        card = list(card)
        all_cards.append(Card(card[0], card[1]))
    return all_cards

def get_all_hands():
    hands = []
    all_cards = get_all_cards()

    for i1 in range(len(all_cards) - 1):
        for i2 in range(i1 + 1, len(all_cards)):
            card1 = all_cards[i1]
            card2 = all_cards[i2]
            hand = Hand(card1, card2)
            hands.append(hand)

    return hands

def get_remaining_cards(hand, cards_on_board):
    # remove cards in my hand

    all_cards = get_all_cards()

    all_cards.remove(hand.card1)
    all_cards.remove(hand.card2)

    # remove cards on board
    for card in cards_on_board:
        all_cards.remove(card)
    valid_cards = all_cards

    return valid_cards

def get_simulated_opponents_hands(cards_sampled, num_opponents):
    return Opponents(cards_sampled, num_opponents)

def get_simulated_cards_on_board(cards_sampled, num_cards_left_to_reveal):
    return cards_sampled[-num_cards_left_to_reveal:]

def royal_flush_value(cards):
    values_per_suit = dict()
    for suit in Card.suits:
        values_per_suit[suit] = []

    valid_values = ["A", "K", "Q", "J", "10"]
    for card in cards:
        if card.value in valid_values:
            values_per_suit[card.suit].append(card.value)
        if len(values_per_suit[card.suit]) == 5:
            return RankObject("royal_flush", "10")

    return RankObject(None, None)

def isStraight(cards):
    assert len(cards) == 5
    cards_values = [card.value_for_sorting() for card in cards]
    cards_values.sort()
    return cards_values == list(range(min(cards_values), min(cards_values) + 5))

def get_top_card_from_five_cards(cards):
    top_card_num_value = -float('inf')
    curr_top_card = None

    for card in cards:
        if top_card_map[card.value] > top_card_num_value:
            curr_top_card = card
            top_card_num_value = card.value

    return card.value

def hasSameSuits(cards):
    cards_suits = [c.suit for c in cards]
    return all([c.suit == cards_suits[0].suit for c in cards])

def straight_flush_value(cards):
    cards.sort(key=lambda c: c.value)
    cards.sort(key=lambda c: c.suit)

    for i in range(len(cards) - 5):
        five_cards = cards[i:i+5]
        if isStraight(five_cards):
            if hasSameSuits(five_cards):
                top_card = get_top_card_from_five_cards(five_cards)
                return RankObject("straight_flush", top_card)

    return RankObject(None, None)

def four_of_a_kind_value(cards):
    cards.sort(key=lambda c: c.suit)


def get_hand_ranking(hand, board):
    cards_from_hand = [hand.card1, hand.card2]
    seven_cards = cards_from_hand + board

    assert len(seven_cards) == 7, "there must be 2 cards in the hand and 5 on the board"

    does_not_exist = RankObject(None, None)

    if royal_flush_value(seven_cards) != does_not_exist:
        return royal_flush_value(seven_cards)
    elif straight_flush_value(seven_cards) != does_not_exist:
        return straight_flush_value(seven_cards)
    elif four_of_a_kind_value(seven_cards) != does_not_exist:
        return four_of_a_kind_value(seven_cards)
    elif is_full_house(seven_cards):
        return FullHouse(seven_cards)
    elif is_flush(seven_cards):
        return Flush(seven_cards)
    elif is_straight(seven_cards):
        return Straight(seven_cards)
    elif is_three_of_a_kind(seven_cards):
        return ThreeOfAKind(seven_cards)
    elif is_two_pair(seven_cards):
        return TwoPair(seven_cards)
    elif is_pair(seven_cards):
        return Pair(seven_cards)
    else:
        return HighCard(seven_cards)

def my_hand_is_better(my_hand, opp_hand, board):
    my_hand_ranking = get_hand_ranking(my_hand, board)
    opp_hand_ranking = get_hand_ranking(opp_hand, board)

    if my_win_condition >= opp_win_condition: # ties are counted as wins
        return True
    else:
        return False




