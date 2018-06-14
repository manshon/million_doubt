import random

from models import Deck, Card, FieldCards, Player

import utils
# Create your views here.


def main():
    # デッキを作成
    deck = Deck()
    card_nums = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'Joker']
    card_ranks = [12, 13, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14]
    card_suits = ['spade', 'heart', 'diamond', 'club']
    card_mapping = {}
    for (num, rank) in zip(card_nums, card_ranks):
        card_mapping[num] = rank

    for rank in card_ranks[:13]:  # デッキにJoker含むカード54枚を加える
        for suit in card_suits:
            card = Card(suit=suit, rank=rank)
            deck.cards.append(card)

    deck.cards.append(Card(suit='*', rank=card_mapping['Joker']))
    deck.cards.append(Card(suit='*', rank=card_mapping['Joker']))
    # print(len(deck.cards))
    # for card in deck.cards:
    #     print(card)

    # プレイヤー追加
    player1 = Player(name='player1')
    player2 = Player(name='player2')

    # winner, score = play_game(player1, player2, deck)

    # 10回試行する
    datum = []
    for i in range(10):
        data = play_game(player1, player2, deck)
        datum.append([data[0].name, data[1]])

    # スコアを集計
    utils.calc_data(datum)


def play_game(player1, player2, deck):
    """
    1回のゲームを行い、そのゲームのスコアーをそれぞれ返す関数
    :param player1: Playerクラス
    :param player2: Playerクラス
    :param deck: Deckクラス、作成済みのデッキ
    return winner, win_score
    """
    counter = 0
    face_up_or_down = [True, False]  # カードを表で出すか裏で出すか
    doubt_or_through = [True, False]  # カードを表で出すか裏で出すか

    deck.shuffle()  # デッキをシャッフルする
    # それぞれのプレイヤーにカードを配る
    player1.init_hands()  # プレイヤー1のハンドを初期化
    player2.init_hands()  # プレイヤー2のハンドを初期化
    player1.add_hands([card for card in deck.cards[:7]])
    player2.add_hands([card for card in deck.cards[7:14]])

    print('-' * 100)
    print('ゲーム開始')
    print('player1の初期手札')
    print([card.get_suit_and_rank() for card in player1.hands])
    print('player2の初期手札')
    print([card.get_suit_and_rank() for card in player2.hands])
    print('-' * 100)

    while True:
        if len(player1.hands) == 0:
            print('p1の{}枚勝ち!'.format(len(player2.hands)))
            ret = [player1, len(player2.hands)]
            break
        if len(player2.hands) == 0:
            print('p2の{}枚勝ち!'.format(len(player1.hands)))
            ret = [player2, len(player1.hands)]
            break
        if len(player1.hands) >= 11:
            print('p2の{}枚勝ち!'.format(len(player1.hands)))
            ret = [player2, len(player1.hands)]
            break
        if len(player2.hands) >= 11:
            print('p1の{}枚勝ち!'.format(len(player2.hands)))
            ret = [player1, len(player2.hands)]
            break

        field_cards = FieldCards(cards=[], latest_card_rank=0)  # 場を初期化
        #  フィールドが空になるまで繰り返す
        while True:
            if len(player1.hands) == 0 or len(player2.hands) == 0:
                print('-' * 100)
                print('勝負が決まりました')
                break
            print('p1の残りのカード枚数', len(player1.hands))
            print('p2の残りのカード枚数', len(player2.hands))
            print('場のカード枚数', len(field_cards.cards))
            # print('どちらかの手札が0枚になったか: {}'.format(normal_finished))
            # print('どちらかの手札が11枚以上になったか: {}'.format(burst_finished))
            if counter % 2 == 0:  # プレイヤー1のターンの行動
                # card_list = []
                # for cards in player1.hands:
                #     card_list.append(cards.get_suit_and_rank())
                print('-' * 100)
                print('player1の手番')
                print('player1のカード')
                print([card.get_suit_and_rank() for card in player1.hands])
                print('player2のカード')
                print([card.get_suit_and_rank() for card in player2.hands])
                print('場のカード')
                print([card.get_suit_and_rank() for card in field_cards.cards])
                print('*' * 50)

                counter += 1
                is_face = random.choice(face_up_or_down)  # 表か裏か
                play_cards, play_cards_rank = player1.play_cards(delete_indices=[0])  # カードをプレイする
                print('player1は以下のカードをプレイした')
                print(([card.get_suit_and_rank() for card in play_cards]))

                # フィールドにカードを追加する
                for card in play_cards:
                    field_cards.cards.append(card)

                # カードを表でプレイしたか裏でプレイしたかで条件分岐
                if is_face:
                    field_cards.latest_card_rank = play_cards_rank  # 現在の有効最大ランクを更新
                    print('p1はカードを表でプレイした')
                    continue
                else:
                    print('p1はカードを裏でプレイした')
                    is_doubt = random.choice(doubt_or_through)
                    if is_doubt:  # プレイヤー2がダウト宣言をしたとき
                        print('p2はダウトを宣言した')
                        if play_cards_rank > field_cards.latest_card_rank:  # ダウトコール失敗時の処理
                            for penalty_cards in field_cards.cards:
                                player2.hands.append(penalty_cards)
                            print('p2はダウトに失敗した')
                            break
                        else:  # ダウト成功時の処理
                            for penalty_cards in field_cards.cards:
                                player1.hands.append(penalty_cards)
                            counter += 1
                            print('p2はダウトに成功した')
                            break
                    else:  # スルーコール時の処理。相手にターンを渡す
                        print('p2はスルーを宣言した')
                        continue
            else:  # プレイヤー2のターンの行動
                card_list = []
                for cards in player2.hands:
                    card_list.append(cards.get_suit_and_rank())
                print('-' * 100)
                print('player2の手番')
                print('player1のカード')
                print([card.get_suit_and_rank() for card in player1.hands])
                print('player2のカード')
                print([card.get_suit_and_rank() for card in player2.hands])
                print('場のカード')
                print([card.get_suit_and_rank() for card in field_cards.cards])
                print('*' * 50)

                counter += 1
                is_face = random.choice(face_up_or_down)  # 表か裏か
                play_cards, play_cards_rank = player2.play_cards(delete_indices=[0])  # カードをプレイする
                print('player2は以下のカードをプレイした')
                print(([card.get_suit_and_rank() for card in play_cards]))

                # フィールドにカードを追加する
                for card in play_cards:
                    field_cards.cards.append(card)

                # カードを表でプレイしたか裏でプレイしたかで条件分岐
                if is_face:
                    field_cards.latest_card_rank = play_cards_rank  # 現在の有効最大ランクを更新
                    print('p2はカードを表でプレイした')
                    continue
                else:
                    is_doubt = random.choice(doubt_or_through)
                    if is_doubt:  # プレイヤー1がダウト宣言をしたとき
                        print('p1はダウトを宣言した')
                        if play_cards_rank > field_cards.latest_card_rank:  # ダウト失敗時の処理
                            for penalty_cards in field_cards.cards:
                                player1.hands.append(penalty_cards)
                            print('p1はダウトに失敗した')
                            break
                        else:  # ダウト成功時の処理
                            for penalty_cards in field_cards.cards:
                                player2.hands.append(penalty_cards)
                            counter += 1
                            print('p1はダウトに成功した')
                            break
                    else:
                        print('p1はスルーを宣言した')
                        continue
    return ret


if __name__ == '__main__':
    main()
