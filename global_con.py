#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：datavista
@File    ：global_config.py
@Author  ：Dong qinping
@Date    ：2024/8/27 上午9:32
'''
import colorsys
import os
import re
import time
import random

colors_int = [
    (193, 40, 45),  # 红
    (92, 160, 207),  # 蓝色
    (237, 134, 34),  # 黄
    (252, 231, 206),  # 蛋黄
]


def desaturate_and_lighten_color(rgb, saturation_factor=0.7, lightness_factor=1.2, type='rgb'):
    # 将RGB值从0-255转换为0-1范围
    r, g, b = [x / 255.0 for x in rgb]
    # 将RGB转换为HSV
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    # 调整饱和度和亮度
    s *= saturation_factor
    v *= lightness_factor
    # 确保亮度不超过1
    v = min(1.0, v)
    # 将HSV转换回RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    # 将RGB值转换回0-255范围并取整
    if type == 'rgb':
        return int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def color_scheme(saturation_factor=1, lightness_factor=1):
    colors = [desaturate_and_lighten_color((r, g, b), saturation_factor, lightness_factor, type='rgba') for r, g, b in
              colors_int]
    random.shuffle(colors)
    return colors


def set_font(plt):
    # 设置matplotlib参数
    plt.rcParams["font.family"] = ["Times New Roman", "SimHei"]
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
    plt.rcParams['font.size'] = 12


def sanitize_and_check_filename(filename, max_length=260):
    # 去除或替换特殊字符
    invalid_chars = re.compile(r'[<>:"/\|?*]+')
    filename = invalid_chars.sub('_', filename)

    # 去除空格和特殊空格字符
    filename = filename.replace(" ", "_").replace("\u3000", "_")

    # 限制文件名长度
    if len(filename) > max_length:
        filename = filename[:max_length]

    # 添加时间戳
    filename = get_now_timestamp() + '.' + filename

    # 检查文件名是否已存在
    if os.path.exists(filename):
        print('已覆盖源文件!')

    return filename


def get_now_timestamp(format="%Y%m%d%H%M%S"):
    timestamp = int(time.time())
    formatted_timestamp = time.strftime(format, time.localtime(timestamp))
    return formatted_timestamp
