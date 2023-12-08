from collections import Counter
from enum import Enum


def parse_file(fd):
    games = []
    for line in fd:
        hand, bid = line.split()
        games.append((hand, int(bid)))
    return (games,)


class HandType(Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


def _hand_comp(card_strength_mapping, hand_type_comp_func):
    def _wrap(hand_with_bid):
        hand, _ = hand_with_bid
        assert len(hand) == 5
        hand_prts = [card_strength_mapping[card] for card in hand]
        return (hand_type_comp_func(hand), hand_prts)

    return _wrap


def _hand_type_comp_1(hand):
    hand_ctr = Counter(hand)

    if len(hand_ctr) == 1:
        return HandType.FIVE_OF_A_KIND.value
    if len(hand_ctr) == 5:
        return HandType.HIGH_CARD.value

    cards_by_count = [set(), set(), set(), set(), set()]
    for card, card_count in hand_ctr.items():
        cards_by_count[card_count].add(card)

    if cards_by_count[4]:
        return HandType.FOUR_OF_A_KIND.value
    elif cards_by_count[3]:
        if cards_by_count[2]:
            return HandType.FULL_HOUSE.value
        else:
            return HandType.THREE_OF_A_KIND.value
    elif cards_by_count[2]:
        if len(cards_by_count[2]) == 2:
            return HandType.TWO_PAIR.value
        else:
            return HandType.ONE_PAIR.value


def _hand_type_comp_2(hand):
    hand_ctr = Counter(hand)

    if len(hand_ctr) == 1:
        return HandType.FIVE_OF_A_KIND.value

    cards_by_count = [set(), set(), set(), set(), set()]
    jokers = 0
    for card, card_count in hand_ctr.items():
        if card == 'J':
            jokers = card_count
        else:
            cards_by_count[card_count].add(card)

    JOKER_NO_ADD_PAIR_MAPPING = {
        4: HandType.FIVE_OF_A_KIND.value,
        3: HandType.FOUR_OF_A_KIND.value,
        2: HandType.THREE_OF_A_KIND.value,
        1: HandType.ONE_PAIR.value,
        0: HandType.HIGH_CARD.value,
    }

    JOKER_ADD_PAIR_MAPPING = {
        1: HandType.FULL_HOUSE.value,
        0: HandType.TWO_PAIR.value,
    }

    if cards_by_count[4]:
        return JOKER_NO_ADD_PAIR_MAPPING[jokers + 3]
    elif cards_by_count[3]:
        if cards_by_count[2]:
            return JOKER_ADD_PAIR_MAPPING[jokers + 1]
        else:
            return JOKER_NO_ADD_PAIR_MAPPING[jokers + 2]
    elif cards_by_count[2]:
        if len(cards_by_count[2]) == 2:
            return JOKER_ADD_PAIR_MAPPING[jokers]
        else:
            return JOKER_NO_ADD_PAIR_MAPPING[jokers + 1]
    else:
        return JOKER_NO_ADD_PAIR_MAPPING[jokers]


def _task_impl(games, card_strength_mapping, hand_type_comp):
    ranks = sorted(games, key=_hand_comp(card_strength_mapping, hand_type_comp))
    return sum(rank * bid for rank, (_, bid) in enumerate(ranks, start=1))


def task_1(games):
    card_strength_mapping = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11,
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
    }
    return _task_impl(games, card_strength_mapping, _hand_type_comp_1)


def task_2(games):
    card_strength_mapping = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,
        'J': 1,
    }
    return _task_impl(games, card_strength_mapping, _hand_type_comp_2)


solution_function_01 = task_1
solution_function_02 = task_2
