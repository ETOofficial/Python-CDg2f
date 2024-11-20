"""
刘、关、张、曹操、孙权、周瑜在各回中出场次数变化的折线图。绘制在一个图中，以不同颜色表示，标注清楚图例
"""

import matplotlib.pyplot as plt
from matplotlib import rcParams
import re # 用于正则表达式分割字符串

from scipy.ndimage import label

from configs import BOOK_PATH

def appears(name):
    with open(BOOK_PATH, "r", encoding="utf-8") as f:
        text = f.read()
        text = re.split(r'第[\u4e00-\u9fa5]+回', text)[1:] # 去掉“第一回”前的内容
    app = [0 for _ in range(len(text))]
    for index, chapter in enumerate(text):
        app[index] += chapter.count(name)
    return app

def draw(data:dict):
    rcParams['font.sans-serif'] = ['SimHei']
    x = [i + 1 for i in range(120)]

    # plt.figure(figsize=(len(x), max([max(i) for i in data.values()])))
    plt.figure(figsize=(8, 6))
    for i in data.items():
        plt.plot(x, i[1], label=i[0])
    plt.title('人物各章节出现次数')
    plt.xlabel('章节')
    plt.ylabel('次数')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    data = {
        "刘":appears("玄德"),
        "关":appears("关公"),
        "张":appears("张飞"),
        "曹操":appears("曹操"),
        "孙权":appears("孙权"),
        "周瑜":appears("周瑜")
    }

    print(len(appears("玄德")))

    # print(data)

    draw(data)

