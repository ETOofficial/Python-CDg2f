from pyecharts import options as opts
from pyecharts.charts import Graph
from utils import csv_editor
from configs import OUTPUT_MENU

def network_generator():
    nodes = []
    links = []

    relations = csv_editor.read_csv("../../docs/relationship.csv")[1]
    names = []
    for relationship in relations:
        names += (relationship["relationship"].split(" "))
    names = list(set(names))
    for name in names:
        nodes.append(opts.GraphNode(name=name, symbol_size=10))

    for relationship in relationship_analysis(relations).items():
        links.append(opts.GraphLink(source=relationship[0][0], target=relationship[0][1], value=round(relationship[1], 2), linestyle_opts=opts.LineStyleOpts(width=2)))

    graph = Graph(init_opts=opts.InitOpts(width="1440px", height="900px"))
    graph.add("",
                nodes,
                links,
                is_draggable=True,
                # repulsion=2000,  # 减小斥力因子
                # edge_length=100,  # 增加边长
                gravity=0.8,  # 增加引力因子
                edge_label=opts.LabelOpts(is_show=True,
                                          position="middle",
                                          formatter="{c}")).set_global_opts(title_opts=opts.TitleOpts(title="Graph-GraphNode-GraphLink")).render(OUTPUT_MENU + "graph_with_options.html")


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