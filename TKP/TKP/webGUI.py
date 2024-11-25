"""
特别鸣谢：https://github.com/syejing/nicegui-reference-cn
"""

from nicegui import ui
import webbrowser
import os
from tempfile import NamedTemporaryFile # 临时文件模块

import plotly.graph_objects as go # 绘图模块

from modules import wordcloud_generator, appears, map_mark, graphnode_generator
from modules.utils import csv_editor

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

wordcloud_history = {"../docs/masks/leaf.png":"leaf.png"}
masks = {}
# 遍历文件夹
for root, dirs, files in os.walk("../docs/masks"):
    # root：当前遍历的文件夹的路径。
    # dirs：当前文件夹下所有子文件夹的名称列表。
    # files：当前文件夹下所有文件的名称列表。
    for file in files:
        # 构建文件路径
        masks.update({root + "/" + file:file})
fonts = {}
for root, dirs, files in os.walk("../fonts"):
    for file in files:
        fonts.update({root + "/" + file:file})
def update_wordcloud():
    # 获取词云图
    if mask_switch.value:
        # 有遮罩
        file_url = wordcloud_generator.name_wordcloud(mask=mask_select.value, num=int(num_input.value), font_path=font_select.value)["full_output_path"]
    else:
        # 没有遮罩
        file_url = wordcloud_generator.name_wordcloud(num=int(num_input.value), font_path=font_select.value)["full_output_path"]
    # 在历史记录中添加新的词云图
    wordcloud_history.update({file_url:file_url.split("/")[-1]})
    # 更新选项
    history_select.options = wordcloud_history
    history_select.value = file_url
    history_select.update()
    # 更新词云图
    img.update()

async def draw_map():
    ui.notify('正在重新生成,请耐心等待...')
    await map_mark.draw_map()
    ui.notify('已重新生成！')

def network_generator():
    graphnode_generator.network_generator()
    ui.notify('已重新生成！')

with ui.tabs().classes('w-full') as tabs:
    wordcloud = ui.tab('词云图')
    linechart = ui.tab('折线图')
    place = ui.tab("地图")
    network = ui.tab("关系网")
    web_code = ui.tab("网页源代码")
with ui.tab_panels(tabs, value=wordcloud).classes('w-full h-full'):
    # 词云图
    with ui.tab_panel(wordcloud):
        with ui.splitter().classes("w-full h-full") as splitter:
            # 左
            with splitter.before:
                with ui.expansion('生成设置', icon='settings').classes('w-full'):
                    """
                    以下是 Material Symbols and Icons 字体库中的一些示例：
                    - home
                    - menu
                    - keyboard
                    - search
                    - settings
                    - info
                    - close
                    - expand_more
                    - expand_less
                    """
                    # 遮罩
                    with ui.expansion('遮罩设置', value=True).classes('w-full'):
                        with ui.row():
                            mask_switch = ui.switch('启用遮罩', value=True)
                        with ui.row():
                            mask_select = ui.select(masks, label="遮罩", value="../docs/masks/leaf.png")
                            ui.image().bind_source_from(mask_select, "value").style("width: 64px; height: 64px;")
                    # 数量
                    with ui.expansion('数量设置', value=True).classes('w-full'):
                        with ui.row():
                            num_input = ui.number(label='人物数量（0为所有人）', value=20, validation={"值不能小于0":lambda n: n >= 0})
                            ui.button("重置", on_click=lambda: num_input.set_value(20)).style("margin-top: 16px;")
                    # 字体
                    with ui.expansion('字体设置', value=True).classes('w-full'):
                        with ui.row():
                            font_select = ui.select(fonts, label="字体", value="../fonts/PingFangLaiJiangHuLangTi.ttf")
                            # ui.label("字体预览").props(f"font-family: ’../fonts/PingFangLaiJiangHuLangTi.ttf‘")

                with ui.row():
                    ui.button("生成新的词云图", on_click=update_wordcloud).style("margin-top: 16px;")
                    history_select = ui.select(wordcloud_history, label="历史记录", value="../docs/masks/leaf.png")
                img = ui.image().classes("w-full h-full").bind_source(history_select, "value")

                with ui.expansion("数据来源").classes('w-full'):
                    _, rows = csv_editor.read_csv("../docs/names.csv")
                    columns = [
                        {'name': 'name', 'label': '名字', 'required': True, 'field': 'name', 'type': 'text', 'align': 'left', "sortable":True},
                        {'name': 'frequency', 'label': '频率', 'required': True, 'field': 'frequency', 'type': 'number', 'align': 'right', "sortable":True},
                    ]
                    ui.table(columns=columns, rows=rows, pagination=10, title="表格").classes("w-full")
            # 右
            with splitter.after:
                ui.label("源代码").style("font-size: 50px;")
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
                fig.add_trace(go.Scatter(x=[i for i in range(1, 121)], y=i[1], name=i[0], line=dict(shape='spline')))

            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            # 创建 Plotly 元素并显示
            ui.plotly(fig).classes("w-full h-full")

        ui.label("源代码").style("font-size: 50px;")
        with open("modules/appears.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')
    with ui.tab_panel(place):
        # 地理位置
        with ui.row():
            ui.button("查看位置", on_click=open_map)
            ui.button("重新生成", on_click=draw_map)

        ui.label("源代码").style("font-size: 50px;")
        with open("modules/address_analyze.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')
        with open("modules/map_mark.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')
    with ui.tab_panel(network):
        # 人物关系网络图
        with ui.row():
            ui.button("查看关系网", on_click=open_network)
            ui.button("重新生成", on_click=network_generator)
        ui.label("源代码").style("font-size: 50px;")
        with open("modules/graphnode_generator.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')
    with ui.tab_panel(web_code):
        with open("webGUI.py", "r", encoding="utf-8") as f:
            code = f.read()
            ui.code(code).classes('w-full h-full')

# 启动 UI
ui.run()

