import numpy as np
import scipy.stats as st
from monte_carlo_helpers import *
import matplotlib.pyplot as plt


# todo what if i add genetc / rl algo - assign values to traits like bluffing,
#  aggressiveness, randomness, etc. and incudenthat into ur behavior. also
#  maybe is there a way for the model to learn from what others are doing to
#  make money?
#  if i can't code it up rn, at least leave space to add it in later!!!

def optimal_bet_proportion(p_winning, min_probability_of_making_money=0.75, edge_demanded=0.05):
    '''
    ok here's my plan
    find the breakeven betting value x = p/q - e (where e is the edge we demand, probably fix at 0.05)

    keep lowering x until the probability of making money is just above 90%. if this isn't possible, x is 0. simple.

    therefore we will make money 90% or more of the time, and this will always be a positive EV bet for us.
    '''

    # todo have to consider the case where we have a really high chance of winning (95%), and this code tells us to
    #  raise by like 8 pots... then we also have the chance to lose a lot of money, even though we're expected to
    #  make money 80% of the time (the weight of the 20% is not accounted for).
    #  so should i add some code that basically also makes sure that the expected loss is never above a certain amount?
    #  ie find a distribution of the outcomes, where x axis is the profit and y is probability, so find the area
    #  for x < 0 (the expected loss) and make sure it's above a certain amount. So EVEN IF we lose, we only lose
    #  by some salvageable amount. This will also help prevent us from overbetting and causing others to fold.

    # avoid division by zero error
    if p_winning == 1: p_winning = 0.999

    p_losing = 1 - p_winning

    # assume there's 1 in the pot, and we want to bet x. If we have a probability p of winning, then the breakeven
    # is p * (1) + (1-p) * x = 0. Solving for x, we get x = p / (1 - p). We demand some edge so reduce this number,
    # and now we have an upper bound on what x should be. However, this might still be quite large, so we use the
    # rest of the code to reduce it until the probability of losing money / the expected amount of money we lose if
    # we lose are manageable also.
    upper_bound_x = p_winning / p_losing - edge_demanded

    for i in range(int(1e5)):
        dx = 0.01 * i
        x = upper_bound_x - dx

        if x <= 0 or x > upper_bound_x:
            break

        gains_from_winning = 1
        losses_from_losing = -x

        EV = p_winning * gains_from_winning + p_losing * losses_from_losing

        var = ((p_winning * gains_from_winning - EV) ** 2 + (p_losing * losses_from_losing - EV) ** 2) / 2
        std = var ** 0.5

        p_making_money = st.norm.cdf(EV / std)
        print("betting", round(x, 3), "ev", EV, "P+", round(p_making_money, 3))
        if p_making_money >= min_probability_of_making_money:
            return x

    return 0

def get_pre_flop_probabilities_dict_memoized():
    return read("serialized/pre_flop_odds")


def write_pre_flop_probabilities_dict_memoized(pre_flop_odds_dict):
    raise NotImplementedError
    # i ran this for 100,000 iterations so don't want to overwrite it for no good reason

    write(pre_flop_odds_dict, "serialized/pre_flop_odds")


pre_flop_odds_memoized = get_pre_flop_probabilities_dict_memoized()


def get_preflop_odds_key(hand, num_opponents=5, cards_on_board=[]):
    card1_val = hand.card1.value
    card1_suit = hand.card1.suit
    card2_val = hand.card2.value
    card2_suit = hand.card2.suit

    # keep in sorted order for ease of use
    if card1_val > card2_val:
        card1_val, card1_suit, card2_val, card2_suit = card2_val, card2_suit, card1_val, card1_suit

    suit_to_suitkey_map = dict()
    key_from_hand = ""
    num_suits_seen = 1

    key_from_hand += card1_val
    key_from_hand += "s" + str(num_suits_seen) + "_"

    if card2_suit != card1_suit:
        num_suits_seen += 1

    key_from_hand += card2_val
    key_from_hand += "s" + str(num_suits_seen) + "_"

    key_from_num_opp = str(num_opponents) + "opps_"

    key_from_cards_on_board = ""
    cards_on_board.sort(key=lambda c: c.value_for_sorting())
    for card in cards_on_board:
        if card.suit not in suit_to_suitkey_map:
            num_suits_seen += 1

        key_from_cards_on_board += card.value
        key_from_cards_on_board += "s" + str(num_suits_seen) + "_"

    return key_from_hand + key_from_cards_on_board + key_from_num_opp


def get_pre_flop_memoized_probability_of_winning(hand, num_opponents=5, cards_on_board=[]):
    lookup = get_preflop_odds_key(hand, num_opponents, cards_on_board)
    print("lookup for memoized", lookup, "dict rn", pre_flop_odds_memoized)
    return get_pre_flop_probabilities_dict_memoized()[lookup]


def memoize_probabilities_preflop():
    pre_flop_odds_memoized = get_pre_flop_probabilities_dict_memoized()
    print("dict before starting", pre_flop_odds_memoized)

    all_hands = get_all_hands()
    for hand in all_hands:
        key = get_preflop_odds_key(hand, num_opponents=5, cards_on_board=[])
        if key not in pre_flop_odds_memoized:
            p_winning = get_probability_of_winning(hand, 5, cards_on_board=[], num_games_simulated=100000)
            pre_flop_odds_memoized[key] = p_winning
            write_pre_flop_probabilities_dict_memoized(pre_flop_odds_memoized)
            print("memoized", hand, "p winning", p_winning)
            print("% memoized", len(pre_flop_odds_memoized) / 169)
        else:
            print("previously memoized", hand, "p winning",
                  get_pre_flop_memoized_probability_of_winning(hand, num_opponents=5, cards_on_board=[]))


def get_hand_percentile(hand, num_opponents=5):
    p_winning = get_pre_flop_memoized_probability_of_winning(hand, num_opponents=num_opponents, cards_on_board=[])
    pre_flop_odds_memoized = get_pre_flop_probabilities_dict_memoized()

    ps_of_winning = []
    for key in pre_flop_odds_memoized:
        ps_of_winning.append(pre_flop_odds_memoized[key])
    ps_of_winning.sort()

    for i in range(len(ps_of_winning)):
        curr_p_winning = ps_of_winning[i]
        if p_winning < curr_p_winning:
            break

    return i / (len(ps_of_winning) - 1)


def visualize_preflop_hand_percentiles_5_opps():
    d = get_pre_flop_probabilities_dict_memoized()
    l = list()
    for key in d:
        l.append([key, d[key]])

    print("HANDS AND THEIR CORRESPONDING PERCENTILES")
    l.sort(key=lambda x: -x[1])
    for i in range(len(l)):
        print(i, l[i])

    plt.hist([d[hand] for hand in d], bins=20)
    plt.show()
