# -*- coding: UTF-8 -*-
import pickle
from functools import reduce

d = {}
ddd = {}  # 所有此字开头的词个数
total = 0  # 所有词的总数，必须是单词与二元单词的之和
lt9 = 0  # 小于9的所有词的总数
lt9_dict = {}  # 各词的总数（仅小于9）
lt10_dict = {}  # 各词的总数（仅小于9）
dr9_dict = {}  # 各词的总数（仅小于9）
Q_dict = {}  # Qwi-1 =  1 - ∑ P(wi|wi-1) / ∑ f(wi)

# 初始化：读入数据
with open('corpus.pkl', 'rb') as f:
    d = pickle.load(f)
    for (r, v) in d.items():
        total += v
        if v < 9:
            lt9 += v
            lt9_dict.setdefault(v, 0)
            lt9_dict[v] += 1
        if v < 10:
            lt10_dict.setdefault(v, 0)
            lt10_dict[v] += 1

# 估算零概念
_sum = 0  # r次（1-8） 所有 古德-图灵估计 概率
for (r, v) in lt10_dict.items():
    if r > 1:
        dr9_dict[r - 1] = r * lt10_dict[r] / lt10_dict[r - 1]
        _sum += (r - 1) * lt10_dict[r]
unseen = lt9 / total - _sum / total  # 零概率
print('总词数：%s' % total)
print('零概率估计：%s' % unseen)


# print(lt9_dict)
# print(dr9_dict)


# 求某字开头的所有词的出现个数，对应 ddd[w] = dd(w)
def dd(word):
    __word_i_j = [w for w in d.keys() if w.startswith(word)]
    return sum([d[w] for w in __word_i_j])


# 求零概率
def zero(wi, wj):
    word_i_j = [w for w in d.keys() if w.startswith(wi) and not wi == w]
    word_j = [w[1:] for w in word_i_j]
    ddd[wi] = sum([d[w] for w in word_i_j]) + d[wi]
    for r in word_j:
        d.setdefault(r, 0.0)
    word_p_i_j = [d[k] / ddd[wi] for k in word_i_j]
    word_p_j = [d[k] / ddd[wi] for k in word_j]
    # print(word_p_i_j)
    # print(word_p_j)
    sum_p_i_j = sum(word_p_i_j)
    sum_p_j = sum(word_p_j)
    # print(sum_p_i_j)
    # print(sum_p_j)
    Q_dict[wi] = (1 - sum_p_i_j) / sum_p_j
    # print('Q_dict[%s] = %s' % (wi, Q_dict[wi]))
    # print('zero P(%s|%s) = %s' % (wi, wj, Q_dict[wi] * (d[wj] / total)))
    return Q_dict[wi] * (d[wj] / total)


def pp(words):
    p_list = []
    for i, wj in enumerate(words):
        if i > 0:
            wi = words[i - 1]
            # 分三种情况
            p = None
            r = dd(wi + wj)
            if r >= 9:
                p = dd(wi + wj) / dd(wi)
            elif r > 0:
                p = dr9_dict[r] / total
            else:
                # 零概率
                print('零概率了！')
                p = zero(wi, wj)
        else:
            p = dd(wj) / total
        p_list.append(p)
    # print(p_list)
    return reduce(lambda x, y: x * y, p_list)


def pp0(words):
    p_list = []
    for i, wj in enumerate(words):
        if i > 0:
            wi = words[i - 1]
            p = d[wi + wj] / d[wi]
        else:
            p = d[wj] / total
        p_list.append(p)
    # print(p_list)
    return reduce(lambda x, y: x * y, p_list)


def pp1(words):
    p_list = []
    for i, wj in enumerate(words):
        if i > 0:
            wi = words[i - 1]
            p = d[wi + wj] / d[wi]
        else:
            p = dd(wj) / total
        p_list.append(p)
    # print(p_list)
    return reduce(lambda x, y: x * y, p_list)


def test(words):
    # print('-------')
    # print('P(%s) = %s' % (words, pp0(words)))
    # print('P(%s) = %s' % (words, pp1(words)))
    print('P(%s) = %s' % (words, pp(words)))


test('我爱女人')
test('我爱钱')
test('我爱中国')
