import matplotlib.pyplot as plt
import numpy as np


def wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=lambda x, y: None):
    '''
    WindMouse algorithm. Calls the move_mouse kwarg with each new step.
    Released under the terms of the GPLv3 license.
    G_0 - magnitude of the gravitational fornce
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped

    see https://ben.land/post/2021/04/25/windmouse-human-mouse-movement/ for full docs
    '''

    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)

    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
            W_y = W_y / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random() * 3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0 * (dest_x - start_x) / dist
        v_y += W_y + G_0 * (dest_y - start_y) / dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0 / 2 + np.random.random() * M_0 / 2
            v_x = (v_x / v_mag) * v_clip
            v_y = (v_y / v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))
        if current_x != move_x or current_y != move_y:
            # This should wait for the mouse polling interval
            move_mouse(current_x := move_x, current_y := move_y)

    return current_x, current_y


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
        send_raise_command_for(lower_num * bb_size)


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

        if percentile >= 164 / 169:  # top 5 or so hands
            check()
        elif percentile >= 146 / 169:  # raise 1-3x bb for these
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
