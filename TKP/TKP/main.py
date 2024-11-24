

def main_wordcloud_generator(mask=None, font_path=None, num=20):
    from modules.wordcloud_generator import name_wordcloud
    name_wordcloud(mask, font_path, num)

def main_appears():
    from modules.appears import appears, draw
    data = {
        "刘":appears("玄德"),
        "关":appears("关公"),
        "张":appears("张飞"),
        "曹操":appears("曹操"),
        "孙权":appears("孙权"),
        "周瑜":appears("周瑜")
    }
    draw(data)

def main_relationship_analyze():
    from modules.relationship_analyze import relationship_get
    relationship_get()

def main_graphnode_generator():
    from modules.graphnode_generator import network_generator
    network_generator()

if __name__ == '__main__':
    # main_graphnode_generator()
    # main_relationship_analyze()
    main_wordcloud_generator(mask="../docs/mask/dish.jpg")