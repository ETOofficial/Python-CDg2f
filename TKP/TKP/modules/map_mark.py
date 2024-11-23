# 地图标记

import folium
# from folium.plugins import FloatImage
# import pandas
import requests
# import math

from .configs import OUTPUT_MENU, GD_MAP_API_KEY
from .utils import csv_editor

gd_map_called = 0

def remove_none_none(l):
    return [i for i in l if i[0] != "unknown" and i[1] != "unknown"]

def average(nums):
    if len(nums) == 0:
        return 0
    return sum(nums) / len(nums)

def average_lon_lat(lon_lat:list):
    lon_lat = remove_none_none(lon_lat)
    return average([i[0] for i in lon_lat]), average([i[1] for i in lon_lat])

def gd_map(addr):
    global gd_map_called
    if gd_map_called >= 30:
        print("超过30次调用限制")
        return None, None
    gd_map_called += 1

    key = GD_MAP_API_KEY  # 替换为你在高德开放平台上申请的key
    params = {
        'key': key,
        'address': addr
    }
    url = 'https://restapi.amap.com/v3/geocode/geo?'
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"请求失败，状态码：{response.status_code}")
        return None, None

    result = response.json()

    if 'geocodes' not in result:
        print("返回的数据中没有 'geocodes' 键")
        print(result)  # 打印结果以供调试
        return None, None

    if len(result['geocodes']) == 0:
        print("没有找到对应的经纬度信息")
        return None, None

    location = result['geocodes'][0]['location']
    lon_lat = location.split(',')
    lon = float(lon_lat[0])
    lat = float(lon_lat[1])
    print(f"{addr} 的高德标准经纬度为: ({lon}, {lat})")
    return lon, lat

def draw_map():
    f = csv_editor.read_csv("../docs/address.csv")[1][:20]

    for address in f:
        if address["lon"] == "unknown" or address["lat"] == "unknown":
            if address["current_address"] == "unknown":
                lon, lat = gd_map(address["address"])
            else:
                lon, lat = gd_map(address["current_address"])

            if lon is None or lat is None:
                continue
            address["lon"] = lon
            address["lat"] = lat

    # 设置地图
    m = folium.Map(
        location=list(average_lon_lat([[address["lon"], address["lat"]] for address in f]))[::-1],  # 中心点经纬度（先纬后经）
        tiles='https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
        attr='高德-常规图',
        zoom_start=15,  # 默认比例尺
        control_scale=True  # 是否在地图上添加比例尺
    )

    for address in f:
        if address["lon"] == "unknown" or address["lat"] == "unknown":
            continue

        # 添加标记点
        folium.Marker(
            location=[address["lat"], address["lon"]],  # 标记点的经纬度
            popup=address["address"],  # 点击标记点时显示的信息
            icon=folium.Icon(color='blue')  # 标记点的颜色
        ).add_to(m)

    # 保存地图到HTML文件
    m.save(OUTPUT_MENU + 'map_marked.html')
    return OUTPUT_MENU +'map_marked.html'

if __name__ == '__main__':
    # addr = '江东'
    # lon, lat = gd_map(addr) # 经纬

    draw_map()

