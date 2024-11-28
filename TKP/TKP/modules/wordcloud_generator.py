# 词云图生成

import jieba
import wordcloud
import numpy
import time

from PIL import Image
from modules.configs import OUTPUT_MENU, STOPWORDS

from modules.utils import csv_editor

DEFAULT_FONT = "../fonts/PingFangLaiJiangHuLangTi.ttf"
DEFAULT_MASK = None

def wordcloud_generator(output_path,
                        width,
                        height,
                        file_path=None,
                        text="",
                        background_color="white",
                        max_words=100,
                        stopwords=None,
                        font_path=DEFAULT_FONT,
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

def default_wordcloud(mask=None, font_path=None):
    if mask is None:
        mask = DEFAULT_MASK

    if font_path is None:
        font_path = DEFAULT_FONT

    file_name = time.strftime('词云图%Y年%m月%d日%H时%M分%S秒.png', time.localtime())
    full_output_path = OUTPUT_MENU + file_name
    mask = numpy.array(Image.open(mask))

    wordcloud_generator(file_path="../docs/names.csv",
                        output_path=full_output_path,
                        width=1000,
                        height=800,
                        stopwords=STOPWORDS,
                        mask=mask,
                        font_path=font_path,)
    return {"file_name": file_name, "full_output_path": full_output_path}

def name_wordcloud(mask=None, font_path=None, num=20, background_color="white"):
    if mask is None:
        mask = DEFAULT_MASK

    if font_path is None:
        font_path = DEFAULT_FONT

    file_name = time.strftime('词云图%Y年%m月%d日%H时%M分%S秒.png', time.localtime())
    full_output_path = OUTPUT_MENU + file_name

    if mask is not None:
        mask = numpy.array(Image.open(mask))

    f = csv_editor.read_csv("../docs/names.csv")[1]
    if num <= 0:
        text = " ".join([line["name"] for line in f])  # 所有名字
    else:
        try:
            text = " ".join([line["name"] for line in f][:num]) # 前 num 个名字
        except IndexError:
            print("数量超出索引范围")
            text = " ".join([line["name"] for line in f][:20])


    wordcloud_generator(text=text,
                        output_path=full_output_path,
                        width=1000,
                        height=800,
                        mask=mask,
                        relative_scaling=0,
                        font_path=font_path,
                        background_color=background_color)
    return {"file_name": file_name, "full_output_path": full_output_path}

if __name__ == '__main__':
    # import sys
    # sys.path.append(".")

    name_wordcloud()