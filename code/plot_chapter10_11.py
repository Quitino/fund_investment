"""
第十章和第十一章配套绘图代码
生成以下图像：
- ch10_platform_comparison.png — 各平台功能对比雷达图
- ch11_fee_comparison.png — 各渠道费率对比分组条形图
- ch11_channel_matrix.png — 购买渠道选择矩阵
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
import os

# 中文字体设置
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 图1：ch10_platform_comparison.png — 各平台功能对比雷达图
# ============================================================

def plot_platform_radar():
    # 5个平台，5个维度
    platforms = ['天天基金', '雪球', '晨星', 'AKShare', 'Wind']
    dimensions = ['数据完整性', '免费程度', '易用性', '专业深度', '社区活跃度']

    scores = {
        '天天基金': [4, 5, 5, 3, 4],
        '雪球':     [3, 5, 4, 3, 5],
        '晨星':     [4, 3, 4, 5, 3],
        'AKShare':  [4, 5, 3, 4, 3],
        'Wind':     [5, 1, 3, 5, 2],
    }

    N = len(dimensions)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # 闭合

    colors = ['#E84A3A', '#F5A623', '#4A90D9', '#27AE60', '#8E44AD']
    linestyles = ['-', '--', '-.', ':', '-']

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    # 绘制网格
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontproperties=font_prop, fontsize=13, fontweight='bold')
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=9, color='gray')
    ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

    for i, (platform, score) in enumerate(scores.items()):
        values = score + score[:1]
        ax.plot(angles, values, color=colors[i], linewidth=2.2,
                linestyle=linestyles[i], label=platform)
        ax.fill(angles, values, color=colors[i], alpha=0.10)

    ax.legend(
        loc='upper right',
        bbox_to_anchor=(1.35, 1.15),
        prop=font_prop,
        fontsize=12,
        framealpha=0.9,
        title='平台',
        title_fontproperties=font_prop,
    )

    ax.set_title('主要信息平台功能对比（雷达图）', fontproperties=font_prop,
                 fontsize=15, fontweight='bold', pad=20)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch10_platform_comparison.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已保存：{out_path}')


# ============================================================
# 图2：ch11_fee_comparison.png — 各渠道费率对比分组条形图
# ============================================================

def plot_fee_comparison():
    channels = ['银行', '基金直销', '天天基金', '支付宝', '券商']
    fee_types = ['股票型申购费\n(%)', '债券型申购费\n(%)', '货币基金费率\n(%)']

    # 典型费率数据 (%)
    data = {
        '股票型申购费\n(%)':  [1.20, 1.20, 0.15, 0.10, 0.12],
        '债券型申购费\n(%)':  [0.80, 0.60, 0.08, 0.08, 0.08],
        '货币基金费率\n(%)':  [0.00, 0.00, 0.00, 0.00, 0.00],
    }

    x = np.arange(len(channels))
    width = 0.22
    offsets = [-width, 0, width]
    colors = ['#E84A3A', '#4A90D9', '#27AE60']
    hatches = ['', '///', '...']

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#FFFFFF')

    bars_list = []
    for i, (ft, offset, color, hatch) in enumerate(zip(fee_types, offsets, colors, hatches)):
        bars = ax.bar(x + offset, data[ft], width, label=ft.replace('\n', ''),
                      color=color, alpha=0.85, hatch=hatch, edgecolor='white', linewidth=0.8)
        bars_list.append(bars)
        # 数值标注
        for bar, val in zip(bars, data[ft]):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                        f'{val:.2f}%', ha='center', va='bottom',
                        fontproperties=font_prop, fontsize=9.5, color='#333333')
            else:
                ax.text(bar.get_x() + bar.get_width() / 2, 0.005,
                        '0', ha='center', va='bottom',
                        fontproperties=font_prop, fontsize=9, color='#888888')

    ax.set_xticks(x)
    ax.set_xticklabels(channels, fontproperties=font_prop, fontsize=12)
    ax.set_ylabel('费率 (%)', fontproperties=font_prop, fontsize=12)
    ax.set_title('各渠道基金费率对比（申购费典型值）', fontproperties=font_prop,
                 fontsize=14, fontweight='bold', pad=12)
    ax.set_ylim(0, 1.55)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5)
    ax.set_axisbelow(True)

    # 添加注释
    ax.annotate('天天基金股票型\n申购费打1折', xy=(2 - width, 0.15),
                xytext=(2.8, 0.60),
                fontproperties=font_prop, fontsize=9, color='#E84A3A',
                arrowprops=dict(arrowstyle='->', color='#E84A3A', lw=1.5))

    legend_labels = ['股票型申购费 (%)', '债券型申购费 (%)', '货币基金费率 (%)']
    patches = [mpatches.Patch(color=c, label=l, alpha=0.85)
               for c, l in zip(colors, legend_labels)]
    ax.legend(handles=patches, prop=font_prop, fontsize=11,
              loc='upper right', framealpha=0.9)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch11_fee_comparison.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已保存：{out_path}')


# ============================================================
# 图3：ch11_channel_matrix.png — 购买渠道选择矩阵（表格图）
# ============================================================

def plot_channel_matrix():
    channels = ['银行柜台', '基金直销', '天天基金', '支付宝', '微信理财通', '证券公司']
    features = ['综合费率', '操作便利性', 'ETF支持', '基金品种', '账户安全', '适合人群']

    # 评分矩阵（1-5星）
    scores = [
        # 费率  便利  ETF  品种  安全  适合
        [2,    3,   1,   2,   5,   3],   # 银行柜台
        [4,    3,   1,   3,   5,   3],   # 基金直销
        [5,    5,   2,   5,   5,   5],   # 天天基金
        [4,    5,   1,   3,   4,   4],   # 支付宝
        [4,    5,   1,   3,   4,   4],   # 微信理财通
        [5,    4,   5,   4,   5,   4],   # 证券公司
    ]

    scores_arr = np.array(scores, dtype=float)

    # 星级文字
    star_text = {1: '★☆☆☆☆', 2: '★★☆☆☆', 3: '★★★☆☆',
                 4: '★★★★☆', 5: '★★★★★'}

    fig, ax = plt.subplots(figsize=(13, 5.5))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    ax.axis('off')

    # 颜色映射：浅->深绿
    cmap = LinearSegmentedColormap.from_list('green_scale',
                                             ['#EBF5E9', '#1A7A30'], N=256)

    n_rows, n_cols = scores_arr.shape
    cell_h = 0.12
    cell_w = 0.13
    header_h = 0.13
    left_w = 0.16
    top = 0.92

    col_positions = [left_w + i * cell_w for i in range(n_cols)]

    # 表头背景
    ax.add_patch(mpatches.FancyBboxPatch(
        (0, top - header_h), 1.0, header_h,
        boxstyle='square,pad=0', facecolor='#2C3E50', edgecolor='none',
        transform=ax.transAxes, clip_on=False, zorder=2
    ))

    # 表头文字：渠道
    ax.text(left_w / 2, top - header_h / 2, '购买渠道',
            ha='center', va='center', fontproperties=font_prop,
            fontsize=11, fontweight='bold', color='white',
            transform=ax.transAxes)

    # 表头文字：各特点列
    for j, feat in enumerate(features):
        ax.text(col_positions[j] + cell_w / 2, top - header_h / 2, feat,
                ha='center', va='center', fontproperties=font_prop,
                fontsize=10.5, fontweight='bold', color='white',
                transform=ax.transAxes)

    # 数据行
    for i, channel in enumerate(channels):
        row_top = top - header_h - i * cell_h
        row_bg = '#FFFFFF' if i % 2 == 0 else '#F2F8F2'

        # 行背景
        ax.add_patch(mpatches.FancyBboxPatch(
            (0, row_top - cell_h), 1.0, cell_h,
            boxstyle='square,pad=0', facecolor=row_bg, edgecolor='#CCCCCC',
            linewidth=0.5, transform=ax.transAxes, clip_on=False, zorder=1
        ))

        # 渠道名
        ax.text(left_w / 2, row_top - cell_h / 2, channel,
                ha='center', va='center', fontproperties=font_prop,
                fontsize=11, fontweight='bold', color='#2C3E50',
                transform=ax.transAxes)

        # 各列评分
        for j, score in enumerate(scores[i]):
            # 颜色深浅
            norm_val = (score - 1) / 4.0
            cell_color = cmap(norm_val)
            alpha = 0.25 + 0.55 * norm_val

            ax.add_patch(mpatches.FancyBboxPatch(
                (col_positions[j] + 0.005, row_top - cell_h + 0.008),
                cell_w - 0.01, cell_h - 0.016,
                boxstyle='round,pad=0.005', facecolor=(*cell_color[:3], alpha),
                edgecolor='none', transform=ax.transAxes, clip_on=False, zorder=2
            ))

            ax.text(col_positions[j] + cell_w / 2, row_top - cell_h / 2,
                    star_text[score],
                    ha='center', va='center', fontsize=8,
                    color='#1A5C25' if score >= 4 else '#555555',
                    transform=ax.transAxes)

    # 外框线
    total_h = header_h + n_rows * cell_h
    ax.add_patch(mpatches.FancyBboxPatch(
        (0, top - total_h), 1.0, total_h,
        boxstyle='square,pad=0', facecolor='none', edgecolor='#AAAAAA',
        linewidth=1.2, transform=ax.transAxes, clip_on=False, zorder=3
    ))

    ax.set_title('基金购买渠道综合对比矩阵', fontproperties=font_prop,
                 fontsize=14, fontweight='bold', pad=18)

    # 图注
    fig.text(0.5, 0.01,
             '注：★越多代表该维度越优；费率越高★越少；ETF支持需要证券账户',
             ha='center', fontproperties=font_prop, fontsize=9, color='#666666')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out_path = os.path.join(OUTPUT_DIR, 'ch11_channel_matrix.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已保存：{out_path}')


if __name__ == '__main__':
    print('开始生成第十章、第十一章配套图像...')
    plot_platform_radar()
    plot_fee_comparison()
    plot_channel_matrix()
    print('全部图像生成完毕。')
