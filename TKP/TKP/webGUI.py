from nicegui import ui
import webbrowser

import plotly.graph_objects as go

from modules import wordcloud_generator, appears, map_mark

def update_wordcloud():
    img.source = wordcloud_generator.name_wordcloud()["full_output_path"]
    img.update()

def open_map():
    webbrowser.open(map_mark.draw_map())

# 词云图
with ui.card().style("width: 500px; height: 500px;"):
    ui.button("生成新的词云图", on_click=update_wordcloud)
    img = ui.image("../docs/example.png")

# 刘、关、张、曹操、孙权、周瑜在各回中出场次数变化的折线图
with ui.card().style("width: 500px; height: 500px;"):
    data = {
        "刘":appears.appears("玄德"),
        "关":appears.appears("关公"),
        "张":appears.appears("张飞"),
        "曹操":appears.appears("曹操"),
        "孙权":appears.appears("孙权"),
        "周瑜":appears.appears("周瑜")
    }


    fig = go.Figure()
    for i in data.items():
        fig.add_trace(go.Scatter(x=[i for i in range(1, 121)], y=i[1], name=i[0]))

    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    # 创建 Plotly 元素并显示
    ui.plotly(fig).classes('w-full h-40')

# 地理位置
with ui.card().style("width: 100px; height: 100px;"):
    ui.button("查看位置", on_click=open_map)

webbrowser.open("../output/map_marked.html")
# 启动 UI
ui.run()

