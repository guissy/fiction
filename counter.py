# -*- coding: UTF-8 -*-
from collections import Counter
from operator import itemgetter
import pickle

import jieba
import os
import glob

root = 'all'
folds = glob.glob(root+'/**/*.txt')
txt = ''

for file in folds:
    full = False
    with open(file, 'r', encoding='gbk') as f:
        print(file)
        try:
            txt += f.read()
            if len(txt) > pow(10, 8):
                full = True
        except:
            pass
            # print(file + ' encoding error!')
    if full:
        break

# print(txt)
list = jieba.cut(txt, cut_all=False)

data = {}
word_prev = ''
word_total = 0
for word in list:
    if word not in '\n\x00\u3000 _':
        words = word_prev + word
        data.setdefault(word, 0)
        data.setdefault(words, 0)
        data[words] += 1
        data[word] += 1
        word_total += 1
        word_prev = word

# print(word_total)
# print(data)
corpus = sorted(data.items(), key=itemgetter(1), reverse=True)
with open('corpus.txt', 'w') as f:
    f.writelines([k+' '+str(n)+'\n' for (k, n) in corpus])

with open('corpus.pkl', 'wb') as f:
    pickle.dump(data, f)