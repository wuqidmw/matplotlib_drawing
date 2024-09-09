# 小提琴图
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import global_config
from global_config import set_font, sanitize_and_check_filename, color_scheme

set_font(plt)
colors = color_scheme()


def get_color(value, min_value, max_value):
    """
    根据分位点的数值返回渐变的红色
    """
    norm = mcolors.Normalize(vmin=min_value, vmax=max_value)
    cmap = plt.get_cmap('Blues')
    return cmap(norm(value))


def custom_violinplot(data, position=1, title=None, x_label=None, y_label= None, sub_title=None,
                      show_means=True, show_extrema=True, figsize=None):
    """
    参数:
    data (array-like): 数据集，用于绘制小提琴图。
    position (int, optional): 小提琴图在x轴上的位置，默认为1。
    show_means (bool, optional): 是否显示均值，默认为True。
    show_extrema (bool, optional): 是否显示极值（此参数在内部未直接使用，但保留用于兼容性），默认为True。。
    """
    # 创建一个新的绘图区域，应用 figsize 参数
    fig, ax = plt.subplots(figsize=figsize)

    # 绘制小提琴图，但不显示均值、中位数和极值，这些将在后续手动添加
    parts = ax.violinplot([data], positions=[position], showmeans=False, showmedians=False, showextrema=False)

    # 自定义小提琴图的颜色和边缘样式
    for pc in parts['bodies']:
        pc.set_facecolor(colors)
        pc.set_edgecolor('black')  # 设置边缘颜色
        pc.set_alpha(0.7)  # 设置透明度
    ax.patch.set_facecolor('white')  # 设置背景颜色为白色
    ax.grid(False)  # 不显示网格

    # 使用boxplot添加均值和极值线
    ax.boxplot([data], positions=[position], widths=0.1, showfliers=False, showmeans=show_means,
               showcaps=show_extrema, whiskerprops={'linewidth': 2})

    # 定义要计算的百分位数
    quantiles = [25, 50, 75, 90]
    # 根据百分位数计算颜色，并绘制散点图和文本标签
    colors_q = [get_color(np.percentile(data, q), np.min(data), np.max(data)) for q in quantiles]
    for q, color in zip(quantiles, colors_q):
        val = np.percentile(data, q)
        ax.scatter([position], [val], color=color, zorder=3)  # 绘制散点图
        ax.text(position + 0.1, val, f'{q}%: {val:.2f}', va='center')  # 添加文本标签

    # 绘制均值线
    if show_means:
        mean_color = get_color(np.mean(data), np.min(data), np.max(data))
        ax.axvline(x=position, color=mean_color, linestyle='--', label=f'MEAN={np.mean(data):.2f}')

        # 计算四分位距（IQR）和离群值范围
    q1, q3 = np.percentile(data, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    out_line = f'离群值范围:[{lower_bound:.2f}, {upper_bound:.2f}]'

    # 添加图例
    plt.legend([f'MAX={np.max(data):.2f}\nMIN={np.min(data):.2f}\nMEAN={np.mean(data):.2f}'],
               bbox_to_anchor=(1, 1))
    # ax.text(0.85, 0.97,
    #         f'MAX={np.max(data):.2f}\nMIN={np.min(data):.2f}\nMEAN={np.mean(data):.2f}',
    #         fontsize=12,
    #         verticalalignment='top',  # 文本顶部对齐
    #         transform=ax.transAxes,  # 使用坐标轴的变换
    #         bbox=dict(facecolor='white', alpha=0.5, edgecolor=color))  # 添加边框和背景

    # 构造完整标题
    data_info = f" 数据量：{len(data)}"
    sub_title = f"{sub_title}; {data_info}"
    full_title = title + '\n'
    if sub_title:
        full_title += sub_title + '\n'
    full_title += out_line

    # 绘制图表并显示
    fig.tight_layout()
    ax.set_xticklabels([x_label])
    ax.set_title(full_title)
    ax.set_ylabel(y_label)

    plt.savefig(sanitize_and_check_filename(title) + '.png')
    # 显示图像
    plt.show()



#两个小提琴
def custom_violinplots(data1, data2, position1=1, position2=2, title=None, x_labels=None, sub_titles=None,
                       show_means=True, show_extrema=True, figsize=None):
    """
    绘制两个并排的小提琴图。
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(False)
    ax.axvline(x=1.5, color='grey', linestyle='--', linewidth=0.5, zorder=0)

    # 绘制小提琴图
    __plot_violin(ax, data1, position1, colors[0])
    __plot_violin(ax, data2, position2, colors[1])

    # 绘制均值和极值（使用boxplot）
    __plot_boxplot(ax, [data1, data2], [position1, position2], show_means, show_extrema)

    # 绘制百分位数和均值
    __plot_quantiles(ax, data1, position1)
    __plot_quantiles(ax, data2, position2)

    # 添加统计标签
    __add_stats_label(ax, data1, position1, colors[0])
    __add_stats_label(ax, data2, position2, colors[1])

    # 设置标题和标签
    if title:
        ax.set_title(title, fontsize=24, y=1.02)
    if x_labels:
        ax.set_xticks([position1, position2])
        ax.set_xticklabels(x_labels)
    if sub_titles:
        __add_sub_titles(ax, data1, data2, position1, position2, sub_titles)

    plt.savefig(sanitize_and_check_filename(title) + '.png')
    plt.show()



def __plot_violin(ax, data, position, color):
    parts = ax.violinplot([data], positions=[position], showmeans=False, showmedians=False, showextrema=False)
    for pc in parts['bodies']:
        pc.set_facecolor(color)
        pc.set_edgecolor('black')
        pc.set_alpha(0.7)


def __plot_boxplot(ax, data, positions, show_means, show_extrema):
    ax.boxplot(data, positions=positions, widths=0.1, showfliers=False, showmeans=show_means,
               showcaps=show_extrema, whiskerprops={'linewidth': 2})


def __plot_quantiles(ax, data, position):
    quantiles = [25, 50, 75, 90]
    vertical_offset = -0.5 # 初始垂直偏移量

    # 使用自定义颜色映射函数为每个百分位数获取颜色
    colors_q = [get_color(np.percentile(data, q), np.min(data), np.max(data)) for q in quantiles]

    # 绘制散点图和文本标签
    for q, color in zip(quantiles, colors_q):
        val = np.percentile(data, q)
        ax.scatter([position], [val], color=color, zorder=3)  # 绘制散点图

        # 添加文本标签
        # 使用annotate来同时绘制箭头和文本框
        ax.annotate(f'{q}%: {val:.2f}', xy=(position, val), xytext=(position + 0.1, val + vertical_offset),
                    textcoords='data', va='bottom', ha='left',
                    bbox=dict(boxstyle='round', fc='w', ec='0.5', alpha=0.9),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

        # 更新垂直偏移量以避免标签重叠
        vertical_offset -= -1.5


def __add_stats_label(ax, data, position, color):
    stats = {
        'MAX': np.max(data),
        'MIN': np.min(data),
        'MEAN': np.mean(data)
    }
    x_offset = -0.55 if position == 1 else -1.05
    y_offset = 0.97
    ax.text(position + x_offset, y_offset,
            f'MAX={stats["MAX"]:.2f}\nMIN={stats["MIN"]:.2f}\nMEAN={stats["MEAN"]:.2f}',
            fontsize=10, verticalalignment='top', horizontalalignment='center',
            transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5, edgecolor=color))


def __add_sub_titles(ax, data1, data2, position1, position2, sub_titles):
    for pos, sub_title, data in zip([position1, position2], sub_titles, [data1, data2]):
        data_info = f"数据量：{len(data)}"
        sub_title_full = f"{sub_title}; {data_info}"
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        out_line = f'\n离群值范围:[{lower_bound:.2f}, {upper_bound:.2f}]'
        ax.text(pos, ax.get_ylim()[1] * 1.08, sub_title_full + out_line, horizontalalignment='center',
                verticalalignment='top', transform=ax.transData)