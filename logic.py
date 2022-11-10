# Backend
from monte_carlo_helpers import *
import time
from game_logic_helpers import *

test_hand = Hand(Card("A", "spades"),
                 Card("K", "spades"))

print("MY CARDS", test_hand)
print("--------")

test_cards_on_board = [
]

print("CARDS ON BOARD", test_cards_on_board)
print("--------")

print(
    "Probability of having the best hand:",
    get_probability_of_winning(hand=test_hand, num_opponents=5, cards_on_board=test_cards_on_board, verbose=False)
)

def get_my_hand():
    raise NotImplementedError

def get_number_of_opponents():
    # for zone poker it'll be fixed at 5
    return 5

def get_cards_on_board():
    raise NotImplementedError

def is_game_loaded_or_not():
    raise NotImplementedError

def start_a_session():

    # todo code to actually start the session

    game_loaded = False
    while not game_loaded:
        game_loaded = is_game_loaded_or_not()

    raise NotImplementedError

def is_my_turn_now():
    raise NotImplementedError

def get_pot_size():
    raise NotImplementedError

def get_my_balance():
    raise NotImplementedError

def get_current_betting_round():
    cards_on_board = get_cards_on_board()
    if len(cards_on_board) == 0:
        return "pre_flop"
    elif len(cards_on_board) == 3:
        return "flop"
    elif len(cards_on_board) == 4:
        return "turn"
    elif len(cards_on_board) == 5:
        return "river"

# todo add a function for the edge case where we barely have enough money so we go all in with a decent hand
# i.e. if bb is $5 and we have $7 and get a hand at 98%, just go all in
# obviously make the logic more fleshed out

def get_optimal_bet_size():
    '''
    see game_logic_helpers.optimal_bet_proportion
    '''
    pot_size = get_pot_size()
    optimal_bet_proportion = optimal_bet_proportion()

    return optimal_bet_proportion * pot_size

def check():
    raise NotImplementedError

def fold():
    raise NotImplementedError

def can_check():
    # return True if can check the current hand else False
    raise NotImplementedError

def get_amount_to_call():
    raise NotImplementedError

def get_min_raise():
    raise NotImplementedError

def send_raise_command_for_arbitrary(x):
    '''
    Raises by some amount that's not a nice multiple of the big blind size
    '''

    raise NotImplementedError

def send_raise_command_for_n_big_blinds(n):
    '''
    Raises by n big blinds
    '''

    raise NotImplementedError

def send_raise_command_for(x):
    # actually sends command to the front-end

    x = int(x)
    bb_size = get_big_blind_size()

    if x % bb_size == 0:
        send_raise_command_for_n_big_blinds(x)
    else:
        send_raise_command_for_arbitrary(x)

def go_all_in():
    my_balance = get_my_balance()
    for _ in range(5):
        print("ALERT! GOING ALL IN WITH", my_balance, "DOLLARS. WISH FOR THE BEST")

    send_raise_command_for_arbitrary(my_balance)

def raise_by(x):
    # add randomizer such that you only choose a discrete number of big blinds
    # to raise by
    # i.e. if x is 76, and big blind is 25, we can raise by 75 24/25 of the time
    # and 100 1/25 of the time

    if x >= get_my_balance():
        go_all_in()

    bb_size = get_big_blind_size()

    for num_big_blinds in range(10):
        if num_big_blinds * bb_size > x:
            lower_num = num_big_blinds - 1
            larger_num = num_big_blinds

    assert larger_num * bb_size > x >= lower_num * bb_size

    if random.random() > (larger_num * bb_size - x) / bb_size:
        send_raise_command_for(larger_num * bb_size)
    else:
        send_raise_command_for(lower_num *  bb_size)


def call():
    assert is_my_turn_now()

    if x >= get_my_balance():
        go_all_in()

    raise NotImplementedError

def bet(x):
    # todo should i add code for when the bet size is ridiculously big?
    # todo for example if the pot is $20, and we get a bet
    amount_to_call = get_amount_to_call()
    min_raise = get_min_raise()

    if amount_to_call + min_raise <= x:
        raise_by(x)
    elif amount_to_call <= x < amount_to_call + min_raise:
        call()
    else:
        fold()

def get_big_blind_size():
    raise NotImplementedError

def make_betting_decision_preflop(hand, num_opponents=5):
    '''
    check if you have an amazing hand
    raise by 1-3 big blinds if you have a good hand
    else fold
    '''

    num_players = num_opponents + 1
    percentile = get_hand_percentile(hand, num_opponents)

    # todo these numbers are all subject to change
    if percentile >= 1 - 1 / (num_players + 1):
        # Expected max of n iid random variables is (n) / (n + 1)
        # if we let the number of players be n, then we want to
        # only play when we have a higher than expected max hand

        if percentile >= 164/169: # top 5 or so hands
            check()
        elif percentile >= 146/169: # raise 1-3x bb for these
            big_blind_size = get_big_blind_size()
            num_big_blinds_to_raise_by = random.randint(1, 3)
            bet(big_blind_size * num_big_blinds_to_raise_by)
        else:
            fold()
    else:
        fold()


def quit_session():
    fold()
    raise NotImplementedError


def error_detected():
    raise NotImplementedError

def quit_game_if_any_error():
    # todo this function is important
    # idk how to implement this but if there's an error just quit the session
    if error_detected():
        quit_session()

def make_betting_decision_ftr():
    # logic to raise by x /check/fold on flop turn river

    bet_size = get_optimal_bet_size()
    assert bet_size >= 0, "somethings funky"

    if bet_size == 0:
        if can_check():
            check()
        else:
            fold()

    elif bet_size > 0:
        bet(bet_size)

def make_betting_decision(betting_round, p_winning, pot_size, num_opponents, my_balance):
    if betting_round == "pre-flop":
        make_betting_decision_preflop()
    elif betting_round in ["flop", "turn", "river"]:
        make_betting_decision_ftr()


def wait_until_my_turn():
    my_turn = False
    while not my_turn:
        my_turn = is_my_turn_now()
    return

def wait_until_game_is_loaded():
    raise NotImplementedError

def wait_until_betting_round_is_loaded(betting_round):
    raise NotImplementedError

### ACTUAL GAME LOGIC ###
num_games_to_play = 20 # todo change this if you want

start_a_session()
num_games_played = 0
while num_games_played < num_games_to_play:
    wait_until_game_is_loaded()

    my_hand = get_my_hand()
    num_opponents = get_number_of_opponents()


    for betting_round in ["pre-flop", "flop", "turn", "river"]:
        wait_until_betting_round_is_loaded(betting_round)
        cards_on_board = get_cards_on_board()

        # todo add assert statements everywhere to make sure the code reads each step properly

        my_balance = get_my_balance()

        p_winning = get_probability_of_winning(hand=my_hand, num_opponents=num_opponents, cards_on_board=cards_on_board)

        wait_until_my_turn()

        pot_size = get_pot_size()

        make_betting_decision(p_winning, pot_size, num_opponents, my_balance)

    num_games_played += 1
quit_session()

'''
1. only play preflop when ur hand has 90% chance of winning. otherwise fold. never bluff (zone poker).

preflop
if 90 < chance of winning < 96:
- raise up to 1-3 big blinds.
if chance of winning> 96:
- check

flop turn river
- if chance of winning ever drops below 51%, just fold
- round this to some nice big blind multiple

**randomly check some % of the time also
** replace each constant number above with an RV so its not detectable
'''


