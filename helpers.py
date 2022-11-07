from classes import Card, Hand, RankObject, Opponents
import itertools, pickle, random

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
            return RankObject("royal_flush", "A")

    return RankObject(None, None)

def isStraight(cards):
    assert len(cards) == 5
    cards_values = [card.value_for_sorting() for card in cards]
    cards_values.sort()
    return cards_values == list(range(min(cards_values), min(cards_values) + 5))

top_card_map = pickle.load(open("serialized/top_card.map", "rb"))

def get_top_card_value(cards):
    top_card_num_value = -float('inf')
    curr_top_card = None

    for card in cards:
        if top_card_map[card.value] > top_card_num_value:
            curr_top_card = card
            top_card_num_value = top_card_map[card.value]

    return curr_top_card.value

def isFlush(cards):
    assert len(cards) == 5
    cards_suits = [c.suit for c in cards]
    return all([suit == cards_suits[0] for suit in cards_suits])

# todo test this function
def straight_value(cards, check_if_straight_flush=False):
    cards.sort(key=lambda c: c.value)
    cards.sort(key=lambda c: c.suit)

    output = RankObject(None, None)
    curr_top = -float("inf")

    for i in range(len(cards) - 5):
        five_cards = cards[i:i + 5]
        if isStraight(five_cards):
            # this if statement logic might be a little complex but it checks out on a truth table
            if not (check_if_straight_flush and not isFlush(five_cards)):
                top_card = get_top_card_value(five_cards)
                if top_card_map[top_card] > curr_top:
                    output = RankObject("straight_flush", top_card)
                    curr_top = top_card_map[top_card]

    return output
def straight_flush_value(cards):
    return straight_value(cards, check_if_straight_flush=True)

# todo test this function
def four_of_a_kind_value(cards):
    output = RankObject()
    seen = dict()
    top_card = None
    four_of_a_kind_found = False

    # find four of a kind and its value
    for card in cards:
        if card.value not in seen:
            seen[card.value] = 0
        seen[card.value] += 1
        if seen[card.value] == 4:
            four_of_a_kind_found = True
            top_card = card.value
            break

    # find best 5th card
    best_5th_card = None
    for card in cards:
        if top_card_map[card.value] > top_card_map[best_5th_card]:
            if card.value != top_card:
                best_5th_card = card.value

    if four_of_a_kind_found and top_card:
        output = RankObject("four_of_a_kind", top_card, best_5th_card)
    return output

# todo test this function
def full_house_value(cards):
    output = RankObject()

    # find the best trips
    trips = dict()
    for card in cards:
        if card.value not in trips:
            trips[card.value] = 0
        trips[card.value] += 1

    top_trips_value = None
    for card_value_seen in trips:
        if trips[card_value_seen] == 3:
            if top_card_map[card_value_seen] > top_card_map[top_trips_value]:
                top_trips_value = card_value_seen

    # find the best pair
    pairs = dict()
    for card in cards:
        if card.value not in pairs:
            pairs[card.value] = 0
        pairs[card.value] += 1

    top_pair_value = None
    for card_value_seen in pairs:
        if card_value_seen != top_trips_value and pairs[card_value_seen] >= 2:
            if top_card_map[card_value_seen] > top_card_map[top_pair_value]:
                top_pair_value = card_value_seen

    if top_trips_value and top_pair_value:
        output = RankObject("full_house", top_trips_value, top_pair_value)

    return output

def flush_value(cards):
    output = RankObject()

    # get dict to sort cards by suit
    suits = dict()
    for suit in Card.suits:
        suits[suit] = []

    # add each card to the appropriate suit
    for card in cards:
        suits[card.suit].append(card)

    # check if any has a suit
    for suit in suits:
        cards_with_given_suit = suits[suit]
        if len(cards_with_given_suit) >= 5:
            # found our flush
            top_card = get_top_card_value(cards_with_given_suit)
            output = RankObject("flush", top_card)
            break

    return output

def three_of_a_kind_value(cards):
    # todo i copied this from the fullhouse function, there might be a better way of
    # todo abstracting it so i dont have to copy code
    output = RankObject()

    # find the best trips
    trips = dict()
    for card in cards:
        if card.value not in trips:
            trips[card.value] = 0
        trips[card.value] += 1

    top_trips_value = None
    for card_value_seen in trips:
        if trips[card_value_seen] == 3:
            if top_card_map[card_value_seen] > top_card_map[top_trips_value]:
                top_trips_value = card_value_seen

    # find kicker 1
    cards_to_check = []
    for card in cards:
        if card.value != top_trips_value:
            cards_to_check.append(card)
    kicker1 = get_top_card_value(cards_to_check)

    # find kicker 2
    cards_to_check = []
    for card in cards:
        if card.value != top_trips_value and card.value != kicker1:
            cards_to_check.append(card)
    kicker2 = get_top_card_value(cards_to_check)

    if top_trips_value:
        output = RankObject("three_of_a_kind", top_trips_value, kicker1, kicker2)

    return output

def two_pair_value(cards):
    # todo i copied this from the fullhouse function, there might be a better way of
    # todo abstracting it so i dont have to copy code

    output = RankObject()

    # find the best pairs1
    pairs1 = dict()
    for card in cards:
        if card.value not in pairs1:
            pairs1[card.value] = 0
        pairs1[card.value] += 1

    top_pair1_value = None
    for card_value_seen in pairs1:
        if pairs1[card_value_seen] == 2:
            if top_card_map[card_value_seen] > top_card_map[top_pair1_value]:
                top_pair1_value = card_value_seen

    # find the best pairs2
    pairs2 = dict()
    for card in cards:
        if card.value not in pairs2:
            pairs2[card.value] = 0
        pairs2[card.value] += 1

    top_pair2_value = None
    for card_value_seen in pairs2:
        if card_value_seen != top_pair1_value and pairs2[card_value_seen] == 2:
            if top_card_map[card_value_seen] > top_card_map[top_pair2_value]:
                top_pair2_value = card_value_seen

    # find kicker 1
    cards_to_check = []
    for card in cards:
        if card.value != top_pair1_value and card.value != top_pair2_value:
            cards_to_check.append(card)
    kicker1 = get_top_card_value(cards_to_check)

    if top_pair1_value and top_pair2_value:
        output = RankObject("two_pair", top_pair1_value, top_pair2_value, kicker1)

    return output

def pair_value(cards):
    # todo i copied this from the three_of_a_kind code, try to abstract it better!!
    output = RankObject()

    # find the best pairs
    pairs = dict()
    for card in cards:
        if card.value not in pairs:
            pairs[card.value] = 0
        pairs[card.value] += 1

    top_pair_value = None
    for card_value_seen in pairs:
        if pairs[card_value_seen] == 2:
            if top_card_map[card_value_seen] > top_card_map[top_pair_value]:
                top_pair_value = card_value_seen

    # find kicker 1
    cards_to_check = []
    for card in cards:
        if card.value != top_pair_value:
            cards_to_check.append(card)
    kicker1 = get_top_card_value(cards_to_check)

    # find kicker 2
    cards_to_check = []
    for card in cards:
        if card.value != top_pair_value and card.value != kicker1:
            cards_to_check.append(card)
    kicker2 = get_top_card_value(cards_to_check)

    # find kicker 3
    cards_to_check = []
    for card in cards:
        if card.value != top_pair_value and card.value != kicker1 and card.value != kicker2:
            cards_to_check.append(card)
    kicker3 = get_top_card_value(cards_to_check)

    if top_pair_value:
        output = RankObject("pair", top_pair_value, kicker1, kicker2, kicker3)

    return output

def high_card_value(cards):
    high_card_value = get_top_card_value(cards)

    # find kicker 1
    cards_to_check = []
    for card in cards:
        if card.value != high_card_value:
            cards_to_check.append(card)
    kicker1 = get_top_card_value(cards_to_check)

    # find kicker 2
    cards_to_check = []
    for card in cards:
        if card.value != high_card_value and card.value != kicker1:
            cards_to_check.append(card)
    kicker2 = get_top_card_value(cards_to_check)

    # find kicker 3
    cards_to_check = []
    for card in cards:
        if card.value != high_card_value and card.value != kicker1 and card.value != kicker2:
            cards_to_check.append(card)
    kicker3 = get_top_card_value(cards_to_check)

    # find kicker 4
    cards_to_check = []
    for card in cards:
        if card.value != high_card_value and card.value != kicker1 and card.value != kicker2 \
                and card.value != kicker3:
            cards_to_check.append(card)
    kicker4 = get_top_card_value(cards_to_check)

    return RankObject("high_card", high_card_value, kicker1, kicker2, kicker3, kicker4)

def get_hand_ranking(hand, board):
    cards_from_hand = [hand.card1, hand.card2]
    seven_cards = cards_from_hand + board

    assert len(seven_cards) == 7, "there must be 2 cards in the hand and 5 on the board"

    does_not_exist = RankObject()

    if royal_flush_value(seven_cards) != does_not_exist:
        return royal_flush_value(seven_cards)
    elif straight_flush_value(seven_cards) != does_not_exist:
        return straight_flush_value(seven_cards)
    elif four_of_a_kind_value(seven_cards) != does_not_exist:
        return four_of_a_kind_value(seven_cards)
    elif full_house_value(seven_cards) != does_not_exist:
        return full_house_value(seven_cards)
    elif flush_value(seven_cards) != does_not_exist:
        return flush_value(seven_cards)
    elif straight_value(seven_cards) != does_not_exist:
        return straight_value(seven_cards)
    elif three_of_a_kind_value(seven_cards) != does_not_exist:
        return three_of_a_kind_value(seven_cards)
    elif two_pair_value(seven_cards) != does_not_exist:
        return two_pair_value(seven_cards)
    elif pair_value(seven_cards) != does_not_exist:
        return pair_value(seven_cards)
    else:
        return high_card_value(seven_cards)

def my_hand_is_better(my_hand, opp_hand, board):
    my_hand_ranking = get_hand_ranking(my_hand, board)
    opp_hand_ranking = get_hand_ranking(opp_hand, board)

    if my_hand_ranking >= opp_hand_ranking: # ties are counted as wins
        return True
    else:
        return False

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

        print("OPPS", simulated_opps)
        print("REMAINING CARDS ON BOARD", simulated_remaining_cards_on_board)

        board = cards_on_board + simulated_remaining_cards_on_board

        win = 1
        for opponent_num in simulated_opps.opp_hands:
            opp_hand = simulated_opps.opp_hands[opponent_num]
            if not my_hand_is_better(hand, opp_hand, board):
                print("lost")
                win = 0
                break

        wins += win

    return wins / iterations
