# 词频统计

import jieba

def words_frequency_statistics(file_path, text):
    words = jieba.lcut(text.strip())
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for i in range(len(items)):
            word, count = items[i]
            f.write(f"{word}\t{count}\n")
