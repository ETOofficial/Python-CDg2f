from jieba import posseg
from .configs import OUTPUT_MENU, BOOK_PATH
from time import time

def name_statistics(file_path, text):
    words = posseg.cut(text.strip())
    counts = {}

    n = 0
    t = time()
    for word in words:
        n += 1
        if time() - t > 1:
            t = time()
            print("\r已处理", n-1, "个词", end='')
        if word.flag != "nr":
            continue
        counts[word] = counts.get(word, 0) + 1


    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("name,frequency\n")
        for i, _ in enumerate(items):
            word, count = items[i]
            f.write(f"{str(word)[:-3]},{count}\n")

def names_get():
    full_output_path = OUTPUT_MENU + "names.csv"
    with open(BOOK_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    name_statistics(file_path=full_output_path, text=text)

if __name__ == '__main__':

    names_get()

    pass
