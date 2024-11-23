from nicegui import ui
import webbrowser
import os
from tempfile import NamedTemporaryFile # 临时文件模块

import plotly.graph_objects as go

from modules import wordcloud_generator, appears, map_mark

def open_map():
    with open("../outputs/map_marked.html", "r", encoding="utf-8") as f:
        # 创建一个临时的HTML文件
        with NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as tmp_file:
            # 将HTML文本写入临时文件
            tmp_file.write(f.read())
            # 获取临时文件的名称
            tmp_file_name = tmp_file.name

        # 使用webbrowser打开临时HTML文件
        webbrowser.open(f'file://{tmp_file_name}')

        # 清理：删除临时文件
        # 注意：在打开浏览器后删除文件可能导致一些浏览器无法打开文件
        # 你可能需要在关闭浏览器后再删除文件，或者不删除文件
        # os.unlink(tmp_file_name)

def open_network():
    with open("../outputs/graph_with_options.html", "r", encoding="utf-8") as f:
        # 创建一个临时的HTML文件
        with NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as tmp_file:
            # 将HTML文本写入临时文件
            tmp_file.write(f.read())
            # 获取临时文件的名称
            tmp_file_name = tmp_file.name

        # 使用webbrowser打开临时HTML文件
        webbrowser.open(f'file://{tmp_file_name}')


wordcloud_history = {"../docs/example.png":"example.png"}
def update_wordcloud():
    # 获取词云图
    file_url = wordcloud_generator.name_wordcloud()["full_output_path"]
    # 在历史记录中添加新的词云图
    wordcloud_history.update({file_url:file_url.split("/")[-1]})
    # 更新选项
    history.options = wordcloud_history
    history.value = file_url
    history.update()
    # 更新词云图
    img.update()

async def draw_map():
    ui.notify('正在重新生成,请耐心等待...')
    await map_mark.draw_map()
    ui.notify('已重新生成！')

with ui.tabs().classes('w-full') as tabs:
    wordcloud = ui.tab('词云图')
    linechart = ui.tab('折线图')
    place = ui.tab("地图")
    network = ui.tab("网络图")
with ui.tab_panels(tabs, value=wordcloud).classes('w-full h-full'):
    with ui.tab_panel(wordcloud):
        with ui.splitter().classes("w-full h-full") as splitter:
            with splitter.before:
                history = ui.select(wordcloud_history, label="历史记录", value="../docs/example.png")
                # 词云图
                with ui.card().classes('w-full h-full'):
                    ui.button("生成新的词云图", on_click=update_wordcloud)
                    img = ui.image().classes("w-full h-full").bind_source(history, "value")


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
        with ui.row():
            ui.button("查看位置", on_click=open_map)
            ui.button("重新生成", on_click=draw_map)
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

