from configs import BOOK_PATH
from snownlp import SnowNLP
from tqdm import tqdm
import matplotlib.pyplot as plt

def said_get():
    with open(BOOK_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    said = []
    left = 0
    right = 0
    for i, word in enumerate(text):
        if word == "\"" and left == 0:
            left = i
        elif word == "\"" and right == 0 and text[i - 1] != "：":
            right = i
        if left != 0 and right != 0:
            said.append(text[left:right])
            left = 0
            right = 0
    return said

def sentiment_analyze(sentences):
    sentiments = []
    for sentence in tqdm(sentences):
        sentiments.append(SnowNLP(sentence).sentiments)
    return sentiments

def draw_linegraph(sentiments):
    plt.plot(range(len(sentiments)), sentiments, 'b*--', alpha=0.5, linewidth=1, label='acc')  # 'bo-'表示蓝色实线，数据点实心原点标注
    ## plot中参数的含义分别是横轴值，纵轴值，线的形状（'s'方块,'o'实心圆点，'*'五角星   ...，颜色，透明度,线的宽度和标签 ，

    plt.legend()  # 显示上面的label
    plt.xlabel('context')  # x_label
    plt.ylabel('sentiment')  # y_label

    plt.show()

def draw_histogram(sentiments):

    data = [0 for _ in range(10)]
    for i in sentiments:
        if i > 0.9:
            data[9] += 1
        elif i > 0.8:
            data[8] += 1
        elif i > 0.7:
            data[7] += 1
        elif i > 0.6:
            data[6] += 1
        elif i > 0.5:
            data[5] += 1
        elif i > 0.4:
            data[4] += 1
        elif i > 0.3:
            data[3] += 1
        elif i > 0.2:
            data[2] += 1
        elif i > 0.1:
            data[1] += 1
        else:
            data[0] += 1

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.title("基本柱状图")
    plt.grid(ls="--", alpha=0.5)

    plt.bar(range(10), data)

    plt.show()

def draw_pie(sentiments):
    labels = [f"{round(i/10, 1)}~{round(i/10 + 0.1, 1)}" for i in range(10)]
    print(labels)

    data = [0 for _ in range(10)]
    for i in sentiments:
        if i > 0.9:
            data[9] += 1
        elif i > 0.8:
            data[8] += 1
        elif i > 0.7:
            data[7] += 1
        elif i > 0.6:
            data[6] += 1
        elif i > 0.5:
            data[5] += 1
        elif i > 0.4:
            data[4] += 1
        elif i > 0.3:
            data[3] += 1
        elif i > 0.2:
            data[2] += 1
        elif i > 0.1:
            data[1] += 1
        else:
            data[0] += 1

    plt.pie(data, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')  # 显示为圆（避免比例压缩为椭圆）
    plt.show()


if __name__ == '__main__':
    said = said_get()
    sentiments = sentiment_analyze(said)
    draw_pie(sentiments)


    pass