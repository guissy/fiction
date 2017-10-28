# -*- coding: UTF-8 -*-
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle
from collections import Counter

# word_counter 为 Counter 类型的 dict
# key: 词的出现次数
# value: 出现此次数的词个数
word_counter = None
with open('corpus.pkl', 'rb') as f:
    data = pickle.load(f)
    word_counter = Counter(data.values())

if __name__ == '__main__':
    x = list(word_counter.keys())[1:30]
    y = list(word_counter.values())[1:30]
    print(x)
    print(y)

    # 设置全局横纵轴字体大小
    mpl.rcParams['xtick.labelsize'] = 14
    mpl.rcParams['ytick.labelsize'] = 14
    plt.figure('data & model')
    # 通过'k'指定线的颜色，lw指定线的宽度
    # 第三个参数除了颜色也可以指定线形，比如'r--'表示红色虚线
    # 更多属性可以参考官网：http://matplotlib.org/api/pyplot_api.html
    plt.plot(x, y, 'k', lw=2)
    plt.savefig('result.png')
    plt.show()
