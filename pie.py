# 饼状图
import matplotlib.pyplot as plt
from matplotlib import cm
from utils.timeUtils import Timer
from global_config import set_font, sanitize_and_check_filename

# 设置字体格式
set_font(plt)

'''
    data:要处理的数据,pandas.Series或list
    title：主题
    sub_title：子标题
    show_label：饼图的标签,可以默认,或传入字典类型,list类型
    show_zero：是否显示统计数量为0的特殊标签
'''


@Timer('get_boxplot')
def get_pie(data,title, sub_title=None, show_labels=None, show_zero=False):
    data_map = {}  # 存储标签及对应的数据计数
    zero_label = []  # 存储数据量为0的标签
    labels = None
    data_describe = data.describe().T
    all_data_count = data_describe['count']  # 总数据量
    sub_title += f' 数据量:{int(all_data_count)}'  # 在子标题显示总数据量

    if show_labels is None:
        labels = data.unique()  # 获取所有可能值
    else:
        if isinstance(show_labels, dict):
            labels = show_labels.keys()  # 获取字典键值充当标签
        elif isinstance(show_labels, list):
            labels = show_labels
        else:
            raise ValueError("show_labels类型不正确(list or map)")

    for label in labels:
        sub_data = data[data == label]  # 从原始数据中筛选等于该标签的元素
        sub_describe = sub_data.describe().T
        sub_count = sub_describe['count']  # 统计总数
        if sub_count == 0:
            zero_label.append(show_labels.get(label))  # 若总数为0，则表示值为0的标签,加入0列表
        else:  # 总数不为0,将该标签及其对应的数量加入事先声明的字典data_map
            if isinstance(show_labels, dict):
                data_map[show_labels.get(label)] = sub_count  # 字典类型的标签,以传入的字典value作为label
            else:
                data_map[label] = sub_count

    # if show_zero:
    #     data_map[';'.join(zero_label) ]=0

    data_map = dict(sorted(data_map.items(), key=lambda item: item[1]))  # sorted()函数接受字典的items()作为输入,将data_map转换格式,
    # 同时key=lambda itm:item[1]则指定排序根据每项的第二个元素即value,实现根据出现次数从小到大排序
    x = data_map.values()
    labels = data_map.keys()
    print(x)
    print(labels)
    explode = [0.001 for _ in x]  # 假设最大值的10%作为最大爆炸距离

    # plt.figure(figsize=figsize)
    # 绘制饼状图
    # 设置渐变颜色映射
    cmap = cm.Accent
    norm = plt.Normalize(vmin=0, vmax=len(labels))  # 创建一个归一化对象
    colors = [cmap(norm(i)) for i in range(len(labels))]  # 为每个分类生成颜色

    # autopct='%1.1f%%'表示每个分块旁边的百分比标签会显示到小数点后一位。
    plt.pie(x=x, labels=labels, explode=explode, autopct='%1.1f%%', shadow=False, colors=colors, frame=False,
            rotatelabels=False)

    # 设置标题和显示图形
    plt.axis('equal')  # 确保是圆形,而不是椭圆
    # 在同时设置子标题和主标题的时候，会出现错位，使用格式化换行只使用子标题
    ftitle = f'{title}'
    fsub_title = f'{sub_title}'
    plt.suptitle(f'{ftitle}\n{fsub_title}')
    # plt.title(title, pad=40)

    zero_label_str = ''
    for x in zero_label:
        zero_label_str += x + ' = 0%' + '\n'
    print(zero_label_str)
    # 获取x轴和y轴的范围
    x_min, x_max = plt.xlim()
    y_min, y_max = plt.ylim()

    print(f"X轴范围: [{x_min}, {x_max}]")
    print(f"Y轴范围: [{y_min}, {y_max}]")
    # 设置矩形背景板用于凸显0数值标签
    # xy设置位置,wh设置宽度高度,fill=true保证颜色填充,alpha设置透明度
    # bg=plt.Rectangle((x_max-0.1 , (y_min) * 3 / 4-0.1),1.5,0.6,fill=True,color='yellow',alpha=0.8)
    # plt.gca().add_patch(bg)
    bbox_props = dict(boxstyle="round", fc="yellow", ec="0.5", alpha=0.9)
    plt.annotate(zero_label_str, xy=(x_max - 0.1, y_min * 3 / 4), xytext=(x_max - 0.1, y_min * 3 / 4),
                 textcoords='data', bbox=bbox_props)
    # 自适应控制布局
    # plt.tight_layout()
    # plt.text(x_max-0.1, (y_min) * 3 / 4, zero_label_str)
    # plt.tight_layout()
    plt.savefig(sanitize_and_check_filename(title) + '.png', bbox_inches='tight')
    plt.show()
