# 箱形图
import matplotlib.pyplot as plt
import numpy as np
import pandas
from numpy import percentile

from global_config import set_font, sanitize_and_check_filename, color_scheme
from utils.timeUtils import Timer

# 设置字体格式
set_font(plt)
colors = color_scheme(0.8, 0.85)

@Timer('get_boxplot')
def get_boxplot(data: pandas.Series, tick_labels=None, x_label=None, y_label=None, title=None,
                sub_title=None, vert=True,
                figsize=(5, 5),
                showfliers=False):
    '''
    绘制箱形图
    @param data:
    @param tick_labels:
    @param x_label:
    @param y_label:
    @param title:
    @param sub_title:
    @param vert:
    @param figsize:
    @param showfliers:
    @param Models:
    @param title_fontsize:
    @return:
    '''
    if not isinstance(data, pandas.Series):
        raise TypeError('type is not pandas.Series')

    # 设置图形大小
    plt.figure(figsize=figsize)
    # 绘制箱型图
    bp = plt.boxplot(data, tick_labels=tick_labels, notch=True, sym='.', showfliers=showfliers, vert=vert,
                     patch_artist=True)
    # 标签和背景设置
    plt.ylabel(y_label)  # 设置y轴标签
    plt.xlabel(x_label)  # 设置x轴标签
    plt.gca().patch.set_facecolor('white')  # 设置背景颜色为白色
    plt.grid(False)  # 不显示网格

    # 边框设置
    for spine in plt.gca().spines.values():
        spine.set_visible(True)  # 设置边框可见
        spine.set_color('black')  # 设置边框颜色为黑色
        spine.set_linewidth(0.8)  # 设置边框线宽

    # 随机为箱型图填充颜色
    # colors = random.sample(list(mcolors.CSS4_COLORS.keys()), 1)
    for box, color in zip(bp['boxes'], colors):
        box.set_facecolor(color)

    # 打印数据的基本统计信息
    stats = {}
    q1 = np.percentile(data, 25)
    q2 = np.percentile(data, 50)
    q3 = np.percentile(data, 75)
    q_90 = np.percentile(data, 90)
    stats['90%'] = q_90
    stats['25%'] = q1
    stats['50%'] = q2
    stats['75%'] = q3
    # stats['max'] = data.max()
    # stats['min'] = data.min()
    # stats['mean'] = data.mean()
    print(stats)
    # 计算离群值范围并构造字符串
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    out_line = f'离群值范围:[{lower_bound:.2f}, {upper_bound:.2f}]'

    # 构造数据信息字符串
    data_info = f" 数据量：{int(data.count())}"
    # 在图形上添加统计信息
    # 根据垂直或水平箱型图，在合适的位置添加文本和标记
    for key, value in stats.items():
        if vert:
            plt.text(1.1, value, f'{key}: {value:.2f}', verticalalignment='center')
            plt.plot(1, value, 'ro', markersize=2)
        else:
            plt.text(value, 1.2, f'{key}: {value:.2f}', verticalalignment='center', rotation=90)
            plt.plot(value, 1, 'ro', markersize=2)

    sub_title = f"车型：{sub_title}; {data_info}"
    # 构造完整标题
    full_title = title + '\n'
    if sub_title:
        full_title += sub_title + '\n'
    full_title += out_line
    plt.title(full_title)  # 设置标题及字体大小

    # 添加图例，并设置bbox_to_anchor来调整图例的位置
    # 例如，将图例放置在图表外部
    ax = plt.gca()
    ax.legend([f'MAX={data.max():.2f}\nMIN={data.min():.2f}\nMEAN={data.mean():.2f}'], bbox_to_anchor=(1, 1))
    # 对文件名中特殊字符进行去除,添加统一时间戳前缀,保存图形并显示
    plt.savefig(sanitize_and_check_filename(title) + '.png')
    plt.show()


def find_outliers(data, threshold=1.5):
    """
    找出数据集中的离群值。

    参数:
    data (list or numpy.ndarray): 包含数值的数据集。
    threshold (float): 用于判断离群值的阈值，默认为1.5（通常用于IQR方法）。

    返回:
    list: 数据集中的离群值范围。
    """
    # 例如，使用IQR（四分位距）方法
    Q1 = percentile(data, 25)
    Q3 = percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - (IQR * threshold)
    upper_bound = Q3 + (IQR * threshold)
    return lower_bound, upper_bound

