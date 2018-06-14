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
        ret = self.cards[:7]
        del self.cards[:7]
        return ret


class FieldCards(object):
    def __init__(self, cards, latest_card_rank):
        self.cards = cards
        self.latest_card_rank = latest_card_rank

    def set_cards(self, cards):
        self.cards = cards

    def set_latest_card(self, card):
        self.latest_card_rank = card


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hands = []
        self.score = 0
        # 下記の4つをパラメータとする
        self.doubt_pct = 0  # ダウトする確率
        self.lie_pct = 0  # 嘘をつく確率
        self.psycho_state = 0  # 心理状態
        self.trust = 0  # 信頼度

    def get_hands(self):
        return self.hands

    def add_hands(self, hands):
        for hand in hands:
            self.hands.append(hand)

    def init_hands(self):
        self.hands = []

    def play_cards(self, delete_indices=[]):
        """
        プレイヤーがカードをプレイし、そのカードリストとそのうちの最大ランクを返す
        :param delete_indices:
        :return: playing_cards, max_rank
        """
        # カードを出す
        playing_cards = self.del_list(self.hands, delete_indices)

        max_rank = 0
        for card in playing_cards:
            if card.rank > max_rank:
                max_rank = card.rank
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
