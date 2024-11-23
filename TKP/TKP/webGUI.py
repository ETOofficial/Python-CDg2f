from nicegui import ui
import webbrowser
import os

import plotly.graph_objects as go

from modules import wordcloud_generator, appears, map_mark

def open_map():
    webbrowser.open(r"C:\Users\dynas\Documents\Code\Python\Python-CDg2f\TKP\outputs\map_marked.html") # 这里改成自己的路径

def open_network():
    webbrowser.open(r"C:\Users\dynas\Documents\Code\Python\Python-CDg2f\TKP\outputs\graph_with_options.html") # 这里改成自己的路径

def update_wordcloud():
    img.source = wordcloud_generator.name_wordcloud()["full_output_path"]
    img.update()

with ui.tabs().classes('w-full') as tabs:
    wordcloud = ui.tab('词云图')
    linechart = ui.tab('折线图')
    place = ui.tab("地图")
    network = ui.tab("网络图")
with ui.tab_panels(tabs, value=wordcloud).classes('w-full h-full'):
    with ui.tab_panel(wordcloud):
        with ui.splitter().classes("w-full h-full") as splitter:
            with splitter.before:
                # 词云图
                with ui.card().classes('w-full h-full'):
                        ui.button("生成新的词云图", on_click=update_wordcloud)
                        img = ui.image("../docs/example.png").style("width: 100%; height: 100%;")
            with splitter.after:
                ui.label("源代码").style("size: 30px")
                with open("modules/wordcloud_generator.py", "r", encoding="utf-8") as f:
                    code = f.read()
                    ui.code(code).classes('w-full h-full')

    with ui.tab_panel(linechart):
        # 刘、关、张、曹操、孙权、周瑜在各回中出场次数变化的折线图
        with ui.card().classes('w-full h-full'):
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
                    ui.plotly(fig).classes('w-full h-40').style("width: 100%; height: 100%;")

        ui.label("源代码").style("size: 30px")
        with open("modules/appears.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')
    with ui.tab_panel(place):
        # 地理位置
        ui.button("查看位置", on_click=open_map)
        with open("modules/address_analyze.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')
        with open("modules/map_mark.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')

    with ui.tab_panel(network):
        # 人物关系网络图
        ui.button("查看关系网", on_click=open_network)
        with open("modules/graphnode_generator.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')

# 启动 UI
ui.run()

