import matplotlib.pyplot as plt
import re # 用于正则表达式分割字符串

from configs import BOOK_PATH



def appears(name):
    with open(BOOK_PATH, "r", encoding="utf-8") as f:
        text = f
