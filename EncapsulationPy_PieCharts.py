# 饼状图
import matplotlib.pyplot as plt
import numpy as np

from global_config import set_font, sanitize_and_check_filename
from utils.timeUtils import Timer

# 设置字体格式
set_font(plt)

@Timer('get_boxplot')
def get_pie(data, title, sub_title=None, show_labels=None, show_zero=False, figsize=None):
    """
    绘制饼图函数

    参数:
    - data: 可迭代对象，包含要绘制饼图的数据
    - title: 图表的主标题
    - sub_title: 图表的子标题（可选）
    - show_labels: 显示在饼图上的标签，可以是列表或字典（标签到显示的映射）
    - show_zero: 是否显示值为零的标签
    - figsize: 图表大小，元组形式(width, height)

    返回:
    - 无，直接显示图表
    """
    # 确保data是可迭代的
    if not hasattr(data, '__iter__'):
        raise ValueError("data 必须是可迭代的")

    # 设置图表大小
    plt.figure(figsize=figsize)

    # 处理show_labels参数
    if show_labels is None:
        labels = np.unique(data)
    elif isinstance(show_labels, dict):
        labels = list(show_labels.keys())
    elif isinstance(show_labels, list):
        labels = show_labels
    else:
        raise ValueError("show_labels类型不正确(list or dict)")

    # 初始化数据映射和零值标签
    data_map = {}
    zero_label = []

    # 统计每个标签的数量
    for label in labels:
        if hasattr(data, '__getitem__'):
            sub_data = data[data == label]
        else:
            sub_data = [x for x in data if x == label]
        sub_count = len(sub_data)
        if sub_count == 0:
            zero_label.append(show_labels.get(label, label))
        else:
            data_map[show_labels.get(label, label)] = sub_count

    # 对数据映射字典按值进行降序排序
    sorted_data_map = dict(sorted(data_map.items(), key=lambda item: item[1], reverse=True))

    # 如果val小于1，则返回空字符串；否则返回格式化为一位小数的百分比字符串
    def __my_autopct(val):
        return "" if val < 1 else f"{val:.1f}%"

            # 绘制饼图
    x = sorted_data_map.values()
    labels_for_pie = sorted_data_map.keys()
    explode = [0.005 if v > 0 else 0 for v in x]  # 只对非零值进行突出
    colors = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(x)))[::-1]
    patches = plt.pie(x=x, labels=labels_for_pie, autopct=__my_autopct,
                      pctdistance=0.92, explode=explode,
                      shadow=False, colors=colors, frame=False,
                      rotatelabels=False)[0]

    # 添加图例
    labels_with_percent = [f'{label}    {size / sum(x) * 100:.1f}%' for label, size in sorted_data_map.items()]
    plt.legend(patches, labels_with_percent, bbox_to_anchor=(1, 1.05), title='Category Percentages')

    # 显示零值标签
    if show_zero and zero_label:
        zero_label_str = '\n'.join(f'{x} = 0%' for x in zero_label)
        plt.annotate(zero_label_str, xy=(1.1, 0), xytext=(1.1, 0),
                     textcoords='axes fraction', ha='left', va='bottom',
                     bbox=dict(boxstyle="round", fc="yellow", ec="0.5", alpha=0.9))

        # 构造完整的标题
    if sub_title:
        sub_title = f"{sub_title}; 数据量：{len(data)}"
    full_title = title + '\n' + (sub_title if sub_title else '')
    plt.title(full_title, fontsize=18)

    plt.axis('equal')
    # 保存图表为PNG文件，并显示图表
    plt.savefig(sanitize_and_check_filename(title) + '.png', bbox_inches='tight')
    plt.show()