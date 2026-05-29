"""
第一章配套绘图代码
《基金投资理财入门教程》Chapter 1 Plots
生成图像保存到 docs/pic/ 目录
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager

# ── 字体配置 ──────────────────────────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 输出目录 ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# 图1：通货膨胀侵蚀购买力
# ─────────────────────────────────────────────────────────────────────────────
def plot_inflation_erosion():
    years = np.arange(0, 31)
    initial = 100.0

    rates = [0.01, 0.03, 0.06]
    labels = ['通胀率 1%', '通胀率 3%', '通胀率 6%']
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    linestyles = ['-', '--', '-.']

    fig, ax = plt.subplots(figsize=(10, 6))

    for rate, label, color, ls in zip(rates, labels, colors, linestyles):
        values = initial * (1 - rate) ** years
        ax.plot(years, values, label=label, color=color,
                linewidth=2.5, linestyle=ls)
        # 标注第30年终值
        end_val = values[-1]
        ax.annotate(
            f'{end_val:.1f} 元',
            xy=(30, end_val),
            xytext=(27, end_val + 3),
            fontproperties=font_prop,
            fontsize=10,
            color=color,
            arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
        )

    ax.axhline(y=100, color='gray', linewidth=1, linestyle=':', alpha=0.6)
    ax.set_xlabel('年数', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('实际购买力（元）', fontproperties=font_prop, fontsize=13)
    ax.set_title('通货膨胀对 100 元购买力的侵蚀（30 年）',
                 fontproperties=font_prop, fontsize=15, fontweight='bold')
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 115)
    ax.set_xticks(range(0, 31, 5))
    ax.legend(prop=font_prop, fontsize=12, loc='upper right')
    ax.grid(True, alpha=0.3)

    # 填充区域（仅6%那条下方）
    values_6 = initial * (1 - 0.06) ** years
    ax.fill_between(years, values_6, 0, alpha=0.08, color='#e74c3c')

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch1_inflation_erosion.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图2：复利 vs 单利对比
# ─────────────────────────────────────────────────────────────────────────────
def plot_compound_vs_simple():
    years = np.arange(0, 41)
    principal = 10.0  # 单位：万元
    rate = 0.08

    compound = principal * (1 + rate) ** years
    simple = principal * (1 + rate * years)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(years, compound, label='复利（年化 8%）', color='#e74c3c',
            linewidth=2.5)
    ax.plot(years, simple, label='单利（年化 8%）', color='#3498db',
            linewidth=2.5, linestyle='--')

    # 填充复利超出单利的差异区域
    ax.fill_between(years, compound, simple,
                    where=(compound >= simple),
                    alpha=0.15, color='#e74c3c', label='复利超出部分')

    # 标注关键节点
    key_years = [10, 20, 30, 40]
    for y in key_years:
        c_val = compound[y]
        s_val = simple[y]
        # 复利标注
        ax.annotate(
            f'{c_val:.1f}万',
            xy=(y, c_val),
            xytext=(y + 0.8, c_val + 2),
            fontproperties=font_prop,
            fontsize=9,
            color='#c0392b',
            arrowprops=dict(arrowstyle='->', color='#c0392b', lw=1.2),
        )
        # 单利标注
        ax.annotate(
            f'{s_val:.1f}万',
            xy=(y, s_val),
            xytext=(y + 0.8, s_val - 5),
            fontproperties=font_prop,
            fontsize=9,
            color='#2980b9',
            arrowprops=dict(arrowstyle='->', color='#2980b9', lw=1.2),
        )

    ax.set_xlabel('年数', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('资产总额（万元）', fontproperties=font_prop, fontsize=13)
    ax.set_title('10 万元在年化 8% 下：复利 vs 单利（40 年）',
                 fontproperties=font_prop, fontsize=15, fontweight='bold')
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 240)
    ax.set_xticks(range(0, 41, 5))
    ax.legend(prop=font_prop, fontsize=12, loc='upper left')
    ax.grid(True, alpha=0.3)

    # 72法则注释
    rule72_years = 72 / 8
    ax.axvline(x=rule72_years, color='gray', linewidth=1,
               linestyle=':', alpha=0.7)
    ax.text(rule72_years + 0.3, 10,
            f'第{rule72_years:.0f}年\n（72法则翻倍点）',
            fontproperties=font_prop, fontsize=9, color='gray')

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch1_compound_interest.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图3：风险收益散点图
# ─────────────────────────────────────────────────────────────────────────────
def plot_risk_return():
    # (风险/波动率%, 年化收益%, 名称, 颜色)
    assets = [
        (0.5,  2.5,  '货币基金',   '#27ae60'),
        (3.0,  4.5,  '短债基金',   '#2ecc71'),
        (6.0,  6.0,  '债券基金',   '#f1c40f'),
        (10.0, 7.5,  '混合型基金', '#e67e22'),
        (16.0, 9.0,  '指数基金',   '#e74c3c'),
        (22.0, 10.5, '股票型基金', '#c0392b'),
        (35.0, 5.0,  '个股（平均）','#95a5a6'),
    ]

    fig, ax = plt.subplots(figsize=(10, 7))

    for risk, ret, name, color in assets:
        ax.scatter(risk, ret, s=220, color=color, zorder=5,
                   edgecolors='white', linewidths=1.5)
        # 根据位置微调文字偏移，避免重叠
        x_off = 0.5
        y_off = 0.3
        if name == '个股（平均）':
            y_off = -0.6
        elif name == '指数基金':
            y_off = 0.4
        ax.text(risk + x_off, ret + y_off, name,
                fontproperties=font_prop, fontsize=11,
                color=color, fontweight='bold')

    # 绘制大致趋势箭头
    ax.annotate(
        '',
        xy=(30, 10),
        xytext=(2, 3),
        arrowprops=dict(arrowstyle='->', color='#bdc3c7',
                        lw=2, connectionstyle='arc3,rad=0.1'),
    )
    ax.text(12, 5.5, '风险↑  收益↑',
            fontproperties=font_prop, fontsize=11,
            color='#95a5a6', rotation=20, alpha=0.8)

    # 参考线：无风险利率
    ax.axhline(y=2.5, color='#27ae60', linewidth=1,
               linestyle=':', alpha=0.5)
    ax.text(25, 2.7, '≈无风险利率基准',
            fontproperties=font_prop, fontsize=9, color='#27ae60')

    ax.set_xlabel('风险（年化波动率 %）', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('预期年化收益（%）', fontproperties=font_prop, fontsize=13)
    ax.set_title('各类资产风险-收益分布示意图',
                 fontproperties=font_prop, fontsize=15, fontweight='bold')
    ax.set_xlim(-2, 42)
    ax.set_ylim(0, 14)
    ax.grid(True, alpha=0.3)

    # 图例说明
    note = ax.text(
        0.02, 0.97,
        '注：数据为示意性历史均值，非精确预测，不构成投资建议',
        transform=ax.transAxes,
        fontproperties=font_prop,
        fontsize=8.5,
        color='gray',
        verticalalignment='top',
    )

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch1_risk_return.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('开始生成第一章配图...')
    plot_inflation_erosion()
    plot_compound_vs_simple()
    plot_risk_return()
    print('全部图像生成完毕。')
