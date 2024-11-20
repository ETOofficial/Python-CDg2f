#废案





import networkx
from matplotlib import pyplot

from utils import csv_editor
from configs import OUTPUT_MENU

def network_generator():
    net = networkx.Graph()
    pyplot.rcParams['font.sans-serif'] = ['SimHei']
    relations = csv_editor.read_csv("../../docs/relationship.csv")[1]
    names = []
    for relationship in relations:
        names += (relationship["relationship"].split(" "))
    names = list(set(names))
    for name in names:
        net.add_node(name)

    for relationship in relationship_analysis(relations).items():
        net.add_edge(relationship[0][0], relationship[0][1], width=relationship[1])

    # 绘制网络图
    pos = networkx.spring_layout(net)  # 为节点生成一个布局
    networkx.draw(net, pos, with_labels=True)  # 绘制节点和标签
    # 绘制边，并设置宽度
    for (u, v, data) in net.edges(data=True):
        networkx.draw_networkx_edges(net, pos, edgelist=[(u, v)], width=data['width'], edge_color='black')

    # networkx.draw(net, with_labels=True)
    pyplot.show()

def relationship_analysis(relationships:list[dict], multiplier=0.05):
    result = {}
    for relationship in relationships:
        relations = relationship["relationship"].split(" ")
        for i in range(len(relations) - 1):
            for j in range(i+1, len(relations)):
                if (relations[i], relations[j]) in result:
                    result[(relations[i], relations[j])] += multiplier
                else:
                    result[(relations[i], relations[j])] = 1
    return result

if __name__ == '__main__':
    network_generator()

    # relationships = csv_editor.read_csv("../../docs/relationship.csv")[1]
    # result = relationship_analysis(relationships)
    # print(result)