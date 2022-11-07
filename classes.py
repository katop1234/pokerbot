import itertools
import pickle
import os


class Card:
    card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    face_values = ["A", "K", "J", "Q"]
    suits = ["spades", "diamonds", "clubs", "hearts"]

    def __init__(self, value, suit):

        self.value = value.upper()
        self.suit = suit.lower()

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __repr__(self):
        return str([self.value, self.suit])

    def value_for_sorting(self):
        # Number card (2-10)
        val = self.value
        if self.value not in Card.face_values:
            return int(val)

        # Face card (A, Q, J, K)
        else:
            if val == "J":
                return 11
            elif val == "Q":
                return 12
            elif val == "K":
                return 13
            elif val == "A":
                return 1

            else:
                raise ValueError


class Hand:
    def __init__(self, card1, card2):
        assert type(card1) is Card
        assert type(card2) is Card
        assert card1 != card2, "both cards can't be the same"
        self.card1 = card1
        self.card2 = card2

    def __repr__(self):
        return str([self.card1, self.card2])

    def __eq__(self, other):
        return self.card1 == other.card1 and self.card2 == other.card2


class Opponents:
    def __init__(self, cards_sampled, num_opponents):
        simulated_opponents_hands = dict()
        for i in range(num_opponents):
            card1 = cards_sampled[2 * i]
            card2 = cards_sampled[2 * i + 1]

            simulated_opponents_hands[i + 1] = Hand(card1, card2)

        self.opp_hands = simulated_opponents_hands

    def __repr__(self):
        return str(self.opp_hands)


ranking_map = dict()
ranking_map[None] = -float("inf")
ranking_map["high_card"] = 1
ranking_map["pair"] = 2
ranking_map["two_pair"] = 3
ranking_map["three_of_a_kind"] = 4
ranking_map["straight"] = 5
ranking_map["flush"] = 6
ranking_map["full_house"] = 7
ranking_map["four_of_a_kind"] = 8
ranking_map["straight_flush"] = 9
ranking_map["royal_flush"] = 10

with open("serialized/ranking.map", 'wb') as pickle_file:
    pickle.dump(ranking_map, pickle_file)

top_card_map = dict()
top_card_map[None] = -float("inf")
top_card_map["2"] = 2
top_card_map["3"] = 3
top_card_map["4"] = 4
top_card_map["5"] = 5
top_card_map["6"] = 6
top_card_map["7"] = 7
top_card_map["8"] = 8
top_card_map["9"] = 9
top_card_map["10"] = 10
top_card_map["J"] = 11
top_card_map["Q"] = 12
top_card_map["K"] = 13
top_card_map["A"] = 14

with open("serialized/top_card.map", 'wb') as pickle_file:
    pickle.dump(top_card_map, pickle_file)


class RankObject:
    def __init__(self, ranking=None, top_card=None, kicker1=None, kicker2=None, kicker3=None, kicker4=None):
        self.ranking = ranking_map[ranking]
        self.top_card = top_card_map[top_card]
        self.kicker1 = top_card_map[kicker1]
        self.kicker2 = top_card_map[kicker2]
        self.kicker3 = top_card_map[kicker3]
        self.kicker4 = top_card_map[kicker4]

    def __ge__(self, other):
        if self.ranking > other.ranking:
            return True
        elif self.ranking == other.ranking:
            if self.top_card > other.top_card:
                return True
            elif self.top_card == other.top_card:
                if self.kicker1 > other.kicker1:
                    return True
                elif self.kicker1 == other.kicker1:
                    if self.kicker2 > other.kicker2:
                        return True
                    elif self.kicker2 == other.kicker2:
                        if self.kicker3 > other.kicker3:
                            return True
                        elif self.kicker3 == other.kicker3:
                            if self.kicker4 == other.kicker4:
                                return True

        return False

    def __eq__(self, other):
        if self.ranking == other.ranking:
            if self.top_card == other.top_card:
                if self.kicker1 == other.kicker1:
                    if self.kicker2 == other.kicker2:
                        if self.kicker3 == other.kicker3:
                            if self.kicker4 == other.kicker4:
                                return True
        return False
