import os.path

from classes import Card, Hand, RankObject, Opponents, read, write
import itertools, pickle, random


def write(obj, file_name):
    with open(file_name, 'wb') as x:
        pickle.dump(obj, x)


def read(file_name):
    return pickle.load(open(file_name, "rb"))

def write_all_cards():
    if os.path.exists("serialized/all.cards"):
        return read("serialized/all.cards")
    else:
        raw_cards = list(itertools.product(Card.card_values, Card.suits))
        all_cards = []
        for card in raw_cards:
            card = list(card)
            all_cards.append(Card(card[0], card[1]))

        return all_cards

all_cards = write_all_cards()

def get_all_cards():
    return all_cards

def write_all_hands():
    if os.path.exists("serialized/all.hands"):
        return read("serialized/all.hands")

    hands = []
    all_cards = get_all_cards()

    for i1 in range(len(all_cards) - 1):
        for i2 in range(i1 + 1, len(all_cards)):
            card1 = all_cards[i1]
            card2 = all_cards[i2]
            hand = Hand(card1, card2)
            hands.append(hand)

    return hands

all_hands = write_all_hands()

def get_all_hands():
    return all_hands

def get_remaining_cards(hand, cards_on_board):
    all_cards = get_all_cards()

    cards_to_remove = [hand.card1, hand.card2] + cards_on_board

    valid_cards = []
    for card in all_cards:
        if card not in cards_to_remove:
            valid_cards.append(card)

    return valid_cards

def get_simulated_opponents_hands(cards_sampled, num_opponents):
    return Opponents(cards_sampled, num_opponents).opp_hands

def get_simulated_cards_on_board(cards_sampled, num_cards_left_to_reveal):
    return cards_sampled[-num_cards_left_to_reveal:]

def hasFlush(cards):
    cards_by_suit = dict()
    for card in cards:
        if card.suit not in cards_by_suit:
            cards_by_suit[card.suit] = []
        cards_by_suit[card.suit].append(card)
        if len(cards_by_suit[card.suit]) == 5:
            return True
    return False

def royal_flush_value(cards):

    if hasFlush(cards):
        values_per_suit = dict()
        for suit in Card.suits:
            values_per_suit[suit] = []

        valid_values = ["A", "K", "Q", "J", "10"]
        for card in cards:
            if card.value in valid_values:
                values_per_suit[card.suit].append(card.value)
            if len(values_per_suit[card.suit]) == 5:
                return RankObject("royal_flush", "A")

    return RankObject()


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


def straight_value(cards, check_if_straight_flush=False):
    cards.sort(key=lambda c: c.suit)
    cards.sort(key=lambda c: c.value)

    output = RankObject()
    curr_top = -float("inf")

    for i in range(len(cards) - 5):
        five_cards = cards[i:i + 5]
        if isStraight(five_cards):
            top_card = get_top_card_value(five_cards)

            # Checking if straight
            if not check_if_straight_flush:
                if top_card_map[top_card] > curr_top:
                    output = RankObject("straight", top_card)
                    curr_top = top_card_map[top_card]
            # Checking if straight flush
            elif check_if_straight_flush:
                if isFlush(five_cards):
                    if top_card_map[top_card] > curr_top:
                        output = RankObject("straight_flush", top_card)
                        curr_top = top_card_map[top_card]

    return output


def straight_flush_value(cards):
    return straight_value(cards, check_if_straight_flush=True)

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


# generalization of other rankings
# full house = n_groups(3, 2)
# trips = n_groups(3, 1, 1)
# two pair = n_groups(2, 2, 1)
# pair = n_groups(2, 1, 1, 1)
# high_card = n_groups(1, 1, 1, 1, 1)
def best_card_ranking_generalized(cards, n1, n2=0, n3=0, n4=0, n5=0):
    assert n1 + n2 + n3 + n4 + n5 <= 5
    assert n1 >= n2 >= n3 >= n4 >= n5
    output = []
    sizes = [n1, n2, n3, n4, n5]

    card_counts = dict()
    for card in cards:
        if card.value not in card_counts:
            card_counts[card.value] = 0
        card_counts[card.value] += 1

    for size in sizes:
        if size == 0:
            return output

        top_card_value = None
        for card_value_seen in card_counts:
            if card_counts[card_value_seen] >= size:
                if card_value_seen not in output:  # hasn't been used already
                    if top_card_map[card_value_seen] > top_card_map[top_card_value]:
                        top_card_value = card_value_seen

        output.append(top_card_value)

    return output

def four_of_a_kind_value(cards):
    best_cards = best_card_ranking_generalized(cards, 4, 1)
    if None in best_cards:
        return RankObject()
    return RankObject("four_of_a_kind", best_cards[0], best_cards[1])
def full_house_value(cards):
    best_cards = best_card_ranking_generalized(cards, 3, 2)
    if None in best_cards:
        return RankObject()
    return RankObject("full_house", best_cards[0], best_cards[1])
def three_of_a_kind_value(cards):
    best_cards = best_card_ranking_generalized(cards, 3, 1, 1)
    if None in best_cards:
        return RankObject()
    return RankObject("three_of_a_kind", best_cards[0], best_cards[1], best_cards[2])

def two_pair_value(cards):
    best_cards = best_card_ranking_generalized(cards, 2, 2, 1)
    if None in best_cards:
        return RankObject()
    return RankObject("two_pair", best_cards[0], best_cards[1], best_cards[2])

def pair_value(cards):
    best_cards = best_card_ranking_generalized(cards, 2, 1, 1, 1)
    if None in best_cards:
        return RankObject()
    return RankObject("pair", best_cards[0], best_cards[1], best_cards[2], best_cards[3])

def high_card_value(cards):
    best_cards = best_card_ranking_generalized(cards, 1, 1, 1, 1, 1)
    if None in best_cards:
        return RankObject()
    return RankObject("high_card", best_cards[0], best_cards[1], best_cards[2], best_cards[3], best_cards[4])

# todo delete all the print x things later
def get_hand_ranking(hand, board, verbose=False):
    cards_from_hand = [hand.card1, hand.card2]
    seven_cards = cards_from_hand + board
    seven_cards.sort(key=lambda c: c.suit)
    seven_cards.sort(key=lambda c: c.value_for_sorting())
    if verbose:
        print("seven cards were", seven_cards)
    assert len(seven_cards) == 7, "there must be 2 cards in the hand and 5 on the board"

    does_not_exist = RankObject()

    if royal_flush_value(seven_cards) != does_not_exist:
        x = royal_flush_value(seven_cards)
        if verbose: print(x)
        return royal_flush_value(seven_cards)
    elif straight_flush_value(seven_cards) != does_not_exist:
        x = straight_flush_value(seven_cards)
        if verbose: print(x)
        return straight_flush_value(seven_cards)
    elif four_of_a_kind_value(seven_cards) != does_not_exist:
        x = four_of_a_kind_value(seven_cards)
        if verbose: print(x)
        return four_of_a_kind_value(seven_cards)
    elif full_house_value(seven_cards) != does_not_exist:
        x = full_house_value(seven_cards)
        if verbose: print(x)
        return full_house_value(seven_cards)
    elif flush_value(seven_cards) != does_not_exist:
        x = flush_value(seven_cards)
        if verbose: print(x)
        return flush_value(seven_cards)
    elif straight_value(seven_cards) != does_not_exist:
        x = straight_value(seven_cards)
        if verbose: print(x)
        return straight_value(seven_cards)
    elif three_of_a_kind_value(seven_cards) != does_not_exist:
        x = three_of_a_kind_value(seven_cards)
        if verbose: print(x)
        return three_of_a_kind_value(seven_cards)
    elif two_pair_value(seven_cards) != does_not_exist:
        x = two_pair_value(seven_cards)
        if verbose: print(x)
        return two_pair_value(seven_cards)
    elif pair_value(seven_cards) != does_not_exist:
        x = pair_value(seven_cards)
        if verbose: print(x)
        return pair_value(seven_cards)
    else:
        x = high_card_value(seven_cards)
        if verbose: print(x)
        return high_card_value(seven_cards)

def my_hand_is_better(my_hand, opp_hand, board):
    my_hand_ranking = get_hand_ranking(my_hand, board, verbose=False)
    opp_hand_ranking = get_hand_ranking(opp_hand, board)

    if my_hand_ranking >= opp_hand_ranking:  # ties are counted as wins
        return True
    else:
        return False


def monte_carlo_winning_chance_estimator(hand, num_opponents, cards_on_board, iterations=1000, verbose=False):
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

        if verbose:
            print("OPPS", simulated_opps)
            print("REMAINING CARDS ON BOARD", simulated_remaining_cards_on_board)

        board = cards_on_board + simulated_remaining_cards_on_board

        win = 1
        for opponent_num in simulated_opps:
            opp_hand = simulated_opps[opponent_num]
            if not my_hand_is_better(hand, opp_hand, board):
                win = 0
                break

        if verbose:
            if win == 1:
                print("won")
            elif win == 0:
                print("lost")

        wins += win

    p = wins / iterations
    sd = (p * (1-p) / iterations) ** 0.5
    print("99.7% confidence interval", [round(p-3*sd, 3), round(p+3*sd, 3)])
    return p
