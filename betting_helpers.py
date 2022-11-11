import scipy.stats as st
from monte_carlo_helpers import *
import matplotlib.pyplot as plt

# todo what if i add genetc / rl algo - assign values to traits like bluffing,
#  aggressiveness, randomness, etc. and incudenthat into ur behavior. also
#  maybe is there a way for the model to learn from what others are doing to
#  make money?
#  if i can't code it up rn, at least leave space to add it in later!!!

# todo this function sucks
def optimal_bet_proportion(p_winning, num_villains, min_probability_of_making_money=0.9):
    '''
      returns the optimal betting size x subject to the probability of making money being
      above a certain threshold
        # In this calculation, we assume that only 1 opponent calls us. This is the
        # worst case scenario that we account for. If all 5 opponents call us, we
        # have the best possible EV, so I don't want to model based on that. If 0
        # call us, the p_winning changes to 1, so our EV calculation is useless.
        # Therefore, we assume that one opponent will always call us, and this
        # helps us model it as a binary indicator (win or lose) and the calculation
        # for standard deviation checks out and is much simpler.
      '''
    num_players = num_villains + 1
    if p_winning <= 1 / num_players:
        # If there are 4 players who we have to play against and we have
        # a less than 0.25 chance of winning, we shouldn't play at all
        # note this isn't the TOTAL number of players, just those who
        # haven't folded yet since now the probability of winning is
        # evenly split amongst those guys
        # JK Idk if this is good
        return 0

    edge_demanded = 0.05  # TODO can be changed later

    best_x = 0
    p_losing = 1 - p_winning
    best_EV = -float("inf")

    upper_bound_on_x = p_winning / p_losing  # break even point, never bet more than this
    upper_bound_on_x = upper_bound_on_x - edge_demanded

    print("breakeven x", upper_bound_on_x)

    for i in range(101):
        dx = 0.01 * i
        x = upper_bound_on_x - dx
        if x > upper_bound_on_x or x <= 0:
            best_x = x
            break

        gains_from_winning = 1 + num_villains * x
        losses_from_losing = -x

        EV = p_winning * gains_from_winning + p_losing * losses_from_losing

        var = ((p_winning * gains_from_winning - EV) ** 2 + (p_losing * losses_from_losing - EV) ** 2) / 2
        std = var ** 0.5

        p_making_money = st.norm.cdf(EV / std)

        if p_making_money > min_probability_of_making_money:
            if EV > best_EV:
                best_EV = EV
                best_x = x

        print("betsize", x, "Ev", round(EV, 3), "P+", round(p_making_money, 4))

    return max(best_x, 0)


print(optimal_bet_proportion(0.3, 4))
exit()

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

# todo delete these two lines
# #write_pre_flop_odds_memoized({})
# memoize_probabilities_preflop()

hand = Hand(Card("2", "clubs"), Card('3', "hearts"))
print(get_hand_percentile(hand))

d = get_pre_flop_probabilities_dict_memoized()
l = list()
for key in d:
    l.append([key, d[key]])

l.sort(key=lambda x:-x[1])
for i in range(len(l)):
    print(i, l[i])
