from jieba import posseg
from configs import OUTPUT_MENU, BOOK_PATH
from time import time

def address_statistics(file_path, text):
    words = posseg.cut(text.strip())
    counts = {}

    n = 0
    t = time()
    for word in words:
        n += 1
        if time() - t > 1:
            t = time()
            print("\r已处理", n-1, "个词", end='')
        if word.flag != "ns":
            continue
        if len(word.word) <= 1:
            continue
        counts[word] = counts.get(word, 0) + 1


    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("address,frequency,current_address,lon,lat,note\n")
        for i, _ in enumerate(items):
            word, count = items[i]
            f.write(f"{word.word},{count},unknown,unknown,unknown,None\n")

def address_get():
    full_output_path = OUTPUT_MENU + "address.csv"
    with open(BOOK_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    address_statistics(file_path=full_output_path, text=text)

if __name__ == '__main__':

    address_get()

    pass
