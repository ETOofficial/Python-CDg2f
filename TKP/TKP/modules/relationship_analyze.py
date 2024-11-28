from modules.utils import csv_editor
from modules.configs import NAMES_PATH, BOOK_PATH, OUTPUT_MENU

def relationship_statistics(names:list, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    paragraphs = text.split('\n')
    del text
    relationship = {}
    for paragraph in paragraphs:
        relationship_in_paragraph = ""
        for name in names:
            if name in paragraph:
                relationship_in_paragraph += name + " "
        if relationship_in_paragraph == "":
            continue
        relationship_in_paragraph = relationship_in_paragraph[:-1] # 去除最后一个逗号
        if len(relationship_in_paragraph.split(" ")) == 1:
            continue

        relationship[relationship_in_paragraph] = relationship.get(relationship_in_paragraph, 0) + 1

    csv_editor.write_csv(OUTPUT_MENU + "relationship.csv",
                         ["relationship", "frequency"],
                         [{"relationship": relationship_in_paragraph,
                           "frequency": relationship[relationship_in_paragraph]} for relationship_in_paragraph in relationship])

def relationship_get():
    names = [name_frequency["name"] for name_frequency in csv_editor.read_csv(NAMES_PATH)[1]][:20] # 取前20个名字
    relationship_statistics(names, BOOK_PATH)

if __name__ == '__main__':

    relationship_get()