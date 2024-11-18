import jieba
import wordcloud
import numpy
import time

from PIL import Image
from configs import OUTPUT_MENU, STOPWORDS

from utils import csv_editor


def wordcloud_generator(output_path,
                        width,
                        height,
                        file_path=None,
                        text="",
                        background_color="white",
                        max_words=100,
                        stopwords=None,
                        font_path="../../fonts/PingFangLaiJiangHuLangTi.ttf",
                        mask=None,
                        relative_scaling=0.5):

    if file_path is not None:
        with open(file_path,encoding="utf-8") as f:
            text = ' '.join(jieba.lcut(f.read())) # 生成分词列表，连接成字符串

    wc = wordcloud.WordCloud(font_path=font_path,
                             width = width,
                             height = height,
                             background_color=background_color,
                             max_words=max_words,
                             stopwords=stopwords,
                             mask=mask,
                             relative_scaling=relative_scaling,)

    wc.generate(text) # 加载词云文本
    wc.to_file(output_path) # 保存词云文件

def default_wordcloud():
    full_output_path = OUTPUT_MENU + time.strftime('词云图%Y年%m月%d日%H时%M分%S秒.png', time.localtime())
    mask = numpy.array(Image.open("../../docs/example.png"))

    wordcloud_generator(file_path="../../docs/names.csv",
                        output_path=full_output_path,
                        width=1000,
                        height=800,
                        stopwords=STOPWORDS,
                        mask=mask)

def name_wordcloud():
    full_output_path = OUTPUT_MENU + time.strftime('词云图%Y年%m月%d日%H时%M分%S秒.png', time.localtime())
    mask = numpy.array(Image.open("../../docs/example.png"))

    f = csv_editor.read_csv("../../docs/names.csv")[1]
    text = " ".join([line["name"] for line in f][:20]) # 前二十个名字

    wordcloud_generator(text=text,
                        output_path=full_output_path,
                        width=1000,
                        height=800,
                        mask=mask,
                        relative_scaling=0)

if __name__ == '__main__':
    name_wordcloud()