import random
import copy

from utils import MultiElementDelete


class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit  # string
        self.rank = rank  # int

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_suit_and_rank(self):
        return '{}-{}'.format(self.suit, str(self.rank))

    def __str__(self):
        return self.suit + str(self.rank)


class Deck(object):
    def __init__(self, cards=[]):
        self.cards = cards

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_7cards(self):
        ret =  self.cards[:7]
        del self.cards[:7]
        return ret


class FieldCards(object):
    def __init__(self, cards, latest_card_rank):
        self. cards = cards
        self.latest_card_rank = latest_card_rank

    def set_cards(self, cards):
        self.cards = cards

    def set_latest_card(self, card):
        self.latest_card_rank = card


class Player(object):
    def __init__(self, hands, score=0):
        self.hands = hands
        self.score = score

    def get_hands(self):
        return self.hands

    def play_cards(self, delete_indices=[]):
        """
        プレイヤーがカードをプレイし、そのカードリストとそのうちの最大ランクを返す
        :param delete_indices:
        :return: playing_cards, max_rank
        """
        print('#' * 50)
        print([index for index in delete_indices])
        copy_list = copy.deepcopy(self.hands)
        print([card.get_suit_and_rank() for card in copy_list])
        # カードを出す
        playing_cards = self.del_list(self.hands, delete_indices)

        print([card.get_suit_and_rank() for card in self.hands])
        max_rank = 0
        for card in playing_cards:
            if card.rank > max_rank:
                max_rank = card.rank
        print('出したカード')
        print([card.get_suit_and_rank() for card in playing_cards])
        print('#' * 50)
        return playing_cards, max_rank

    def del_list(self, items, indexes):
        """
        :param items:
        :param indexes:
        :return:
        """
        ret = []
        for index in sorted(indexes, reverse=True):
            ret.append(items[index])
            del items[index]
            return ret

    def get_rest_cards_num(self):
        return len(self.hands)
