# 刘、关、张、曹操、孙权、周瑜在各回中出场次数变化的折线图。
# 绘制在一个图中，以不同颜色表示，标注清楚图例

import matplotlib.pyplot as plt
from matplotlib import rcParams
import re # 用于正则表达式分割字符串

from modules.configs import BOOK_PATH

# 定义 appears 函数，用于统计指定人物在文本中各章节的出现次数
def appears(name):
    # 打开配置文件 BOOK_PATH 并读取内容
    with open(BOOK_PATH, "r", encoding="utf-8") as f:
        text = f.read()
        # 使用正则表达式将文本按“第[汉字]回”分割，并去掉“第一回”前的内容
        text = re.split(r'第[\u4e00-\u9fa5]+回', text)[1:]
    # 初始化一个列表，长度为章节数，初始值都为 0
    app = [0 for _ in range(len(text))]
    # 遍历章节列表，统计人物在每个章节中的出现次数
    for index, chapter in enumerate(text):
        app[index] += chapter.count(name)
    # 返回人物在各章节的出现次数列表
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

    draw(data)

