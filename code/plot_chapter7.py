"""
第七章绘图代码：投资策略——怎么买比买什么更重要
生成4张配图：
1. ch7_dca_effect.png      — 定投平均成本效应
2. ch7_asset_allocation.png — 不同资产配置比例的风险收益散点图
3. ch7_rebalance.png        — 再平衡操作示意堆积柱状图
4. ch7_chase_trap.png       — 追涨杀跌陷阱折线图
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
import os

# ── 字体 ──────────────────────────────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 输出目录 ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 图1：定投平均成本效应
# 市场净值序列：先跌后涨  100→70→120
# 对比：一次性买入 vs 每月定投（每月投500元，共12个月）
# ═══════════════════════════════════════════════════════════════════════════════
def plot_dca_effect():
    np.random.seed(42)

    # 构造12个月净值：前6个月从100跌到70，后6个月从70涨到120
    months = np.arange(0, 13)   # 0..12，代表第0月初到第12月末
    # 每月末净值（投资发生在每月初，用当月末净值结算）
    nav = np.array([
        100, 92, 85, 79, 74, 71, 70,   # 0-6月末
        78, 88, 98, 108, 116, 120       # 7-12月末
    ])

    monthly_invest = 500.0   # 每月定投金额
    lump_sum = monthly_invest * 12   # 一次性投入总额 = 6000

    # ── 定投累计份额 ──────────────────────────────────────────────────────────
    # 每月初（用当月末nav近似当月初nav）按照当月初净值买入
    # 简化：第m个月（m=1..12），用nav[m-1]作为买入价
    dca_units = 0.0
    dca_cost = 0.0
    dca_monthly_units = []
    for m in range(1, 13):
        buy_nav = nav[m - 1]          # 当月初净值
        units = monthly_invest / buy_nav
        dca_units += units
        dca_cost += monthly_invest
        dca_monthly_units.append(dca_units)

    dca_final_value = dca_units * nav[-1]
    dca_avg_cost = dca_cost / dca_units

    # ── 一次性买入 ────────────────────────────────────────────────────────────
    lump_units = lump_sum / nav[0]    # 第0月初净值=100买入
    lump_final_value = lump_units * nav[-1]
    lump_avg_cost = nav[0]

    # ── 作图 ──────────────────────────────────────────────────────────────────
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color_nav = '#2c7bb6'
    color_dca = '#d7191c'
    color_lump = '#fdae61'
    color_bar = '#abd9e9'

    # 柱状：每月定投金额（恒定500）
    ax2 = ax1.twinx()
    bar_x = np.arange(1, 13)
    bars = ax2.bar(bar_x, [monthly_invest] * 12, color=color_bar, alpha=0.4,
                   label='每月定投 500 元', width=0.6, zorder=1)
    ax2.set_ylabel('每月投入金额（元）', fontproperties=font_prop, fontsize=11)
    ax2.set_ylim(0, 1800)
    ax2.set_yticks([0, 200, 400, 600])

    # 折线：净值曲线
    ax1.plot(months, nav, color=color_nav, linewidth=2.5,
             marker='o', markersize=5, label='基金净值', zorder=3)

    # 定投平均成本水平线
    ax1.axhline(dca_avg_cost, color=color_dca, linewidth=2,
                linestyle='--', label=f'定投平均成本 {dca_avg_cost:.1f} 元', zorder=3)

    # 一次性买入成本水平线
    ax1.axhline(lump_avg_cost, color=color_lump, linewidth=2,
                linestyle='-.', label=f'一次性买入成本 {lump_avg_cost:.0f} 元', zorder=3)

    # 标注终点收益
    ax1.annotate(
        f'定投终值 {dca_final_value:.0f} 元\n收益率 {(dca_final_value/dca_cost-1)*100:.1f}%',
        xy=(12, nav[-1]), xytext=(9.5, 110),
        fontproperties=font_prop, fontsize=10,
        arrowprops=dict(arrowstyle='->', color=color_dca),
        color=color_dca,
        bbox=dict(boxstyle='round,pad=0.3', fc='#fff0f0', ec=color_dca)
    )
    ax1.annotate(
        f'一次性终值 {lump_final_value:.0f} 元\n收益率 {(lump_final_value/lump_sum-1)*100:.1f}%',
        xy=(12, nav[-1]), xytext=(8.0, 125),
        fontproperties=font_prop, fontsize=10,
        arrowprops=dict(arrowstyle='->', color=color_lump),
        color='#a06000',
        bbox=dict(boxstyle='round,pad=0.3', fc='#fff8e0', ec=color_lump)
    )

    ax1.set_xlabel('月份', fontproperties=font_prop, fontsize=12)
    ax1.set_ylabel('基金净值（元）', fontproperties=font_prop, fontsize=12)
    ax1.set_xticks(range(0, 13))
    ax1.set_xticklabels([f'第{m}月' for m in range(0, 13)],
                        fontproperties=font_prop, fontsize=9, rotation=30)
    ax1.set_ylim(55, 145)
    ax1.set_title('图7-1  定投平均成本效应：先跌后涨市场中定投 vs 一次性买入',
                  fontproperties=font_prop, fontsize=13, pad=12)
    ax1.grid(axis='y', linestyle=':', alpha=0.5)

    # 合并图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2,
               prop=font_prop, fontsize=10, loc='upper left')

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'ch7_dca_effect.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  已保存: {out}')


# ═══════════════════════════════════════════════════════════════════════════════
# 图2：不同资产配置比例的风险收益散点图
# 5种配置：全债/30:70/50:50/70:30/全股，有效前沿曲线
# ═══════════════════════════════════════════════════════════════════════════════
def plot_asset_allocation():
    # 历史数据参考值（年化，简化模拟）
    # 股票：年化收益9%，波动18%；债券：年化收益4%，波动5%；相关系数0.1
    mu_stock, sigma_stock = 9.0, 18.0
    mu_bond, sigma_bond = 4.0, 5.0
    rho = 0.1
    cov = rho * sigma_stock * sigma_bond

    # 5种典型配置 (股票权重)
    presets = [
        ('全债券\n(股0:债100)', 0.0),
        ('保守型\n(股30:债70)', 0.3),
        ('平衡型\n(股50:债50)', 0.5),
        ('积极型\n(股70:债30)', 0.7),
        ('全股票\n(股100:债0)', 1.0),
    ]
    colors = ['#2166ac', '#74add1', '#fdae61', '#f46d43', '#d73027']
    markers = ['s', 'D', 'o', 'D', 's']

    def port_stats(w):
        mu = w * mu_stock + (1 - w) * mu_bond
        sigma = np.sqrt(w**2 * sigma_stock**2 +
                        (1-w)**2 * sigma_bond**2 +
                        2 * w * (1-w) * cov)
        return mu, sigma

    fig, ax = plt.subplots(figsize=(9, 6))

    # 有效前沿曲线（0%→100%股票，细密采样）
    ws = np.linspace(0, 1, 200)
    mus = [port_stats(w)[0] for w in ws]
    sigmas = [port_stats(w)[1] for w in ws]
    ax.plot(sigmas, mus, color='#888888', linewidth=1.5,
            linestyle='--', alpha=0.6, label='有效前沿', zorder=1)

    # 填充有效前沿左侧区域
    ax.fill_betweenx(mus, sigmas,
                     [min(sigmas)] * len(sigmas),
                     alpha=0.06, color='#4dac26')

    # 5个典型配置点
    for (label, w), c, m in zip(presets, colors, markers):
        mu, sigma = port_stats(w)
        ax.scatter(sigma, mu, color=c, s=160, marker=m, zorder=5,
                   edgecolors='white', linewidths=1.5)
        offset_x = 0.3
        offset_y = -0.25 if label.startswith('全股') else 0.2
        ax.annotate(
            f'{label}\n年化收益 {mu:.1f}%\n年化波动 {sigma:.1f}%',
            xy=(sigma, mu),
            xytext=(sigma + offset_x, mu + offset_y),
            fontproperties=font_prop, fontsize=9,
            color=c,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=c, alpha=0.85)
        )

    ax.set_xlabel('年化波动率（风险）%', fontproperties=font_prop, fontsize=12)
    ax.set_ylabel('年化预期收益率 %', fontproperties=font_prop, fontsize=12)
    ax.set_title('图7-2  不同股债配置比例的风险收益特征', fontproperties=font_prop, fontsize=13, pad=12)
    ax.grid(linestyle=':', alpha=0.5)

    legend_patches = [
        mpatches.Patch(color=c, label=label.replace('\n', ' '))
        for (label, _), c in zip(presets, colors)
    ]
    legend_patches.append(plt.Line2D([0], [0], color='#888888', linestyle='--',
                                     label='有效前沿'))
    ax.legend(handles=legend_patches, prop=font_prop, fontsize=9,
              loc='lower right', framealpha=0.9)

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'ch7_asset_allocation.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  已保存: {out}')


# ═══════════════════════════════════════════════════════════════════════════════
# 图3：再平衡操作示意（堆积柱状图）
# 3个时间节点：初始 → 市场上涨后 → 再平衡后
# ═══════════════════════════════════════════════════════════════════════════════
def plot_rebalance():
    labels = ['初始配置\n（建仓）', '1年后\n（市场上涨）', '再平衡后\n（调整仓位）']
    stock = [60, 72, 60]
    bond  = [40, 28, 40]

    color_stock = '#e05c5c'
    color_bond  = '#5c9ee0'

    fig, ax = plt.subplots(figsize=(8, 6))

    x = np.arange(len(labels))
    width = 0.45

    b1 = ax.bar(x, stock, width, label='股票基金', color=color_stock, zorder=3)
    b2 = ax.bar(x, bond,  width, bottom=stock, label='债券基金', color=color_bond, zorder=3)

    # 数值标注
    for i, (s, b) in enumerate(zip(stock, bond)):
        ax.text(x[i], s / 2,       f'{s}%', ha='center', va='center',
                fontproperties=font_prop, fontsize=14, color='white', fontweight='bold')
        ax.text(x[i], s + b / 2,   f'{b}%', ha='center', va='center',
                fontproperties=font_prop, fontsize=14, color='white', fontweight='bold')

    # 目标线 60%
    ax.axhline(60, color=color_stock, linewidth=1.5, linestyle=':',
               alpha=0.8, label='股票目标线 60%')
    ax.axhline(100, color='#aaa', linewidth=0.8, linestyle='-', alpha=0.3)

    # 箭头：市场上涨导致股票仓位偏高
    ax.annotate('', xy=(1.22, 72), xytext=(0.22, 60),
                arrowprops=dict(arrowstyle='->', color='#888', lw=1.5))
    ax.text(0.72, 68, '股票上涨\n仓位偏高', ha='center', fontproperties=font_prop,
            fontsize=9, color='#888')

    # 箭头：再平衡卖高买低
    ax.annotate('', xy=(2 - 0.22, 60), xytext=(1 + 0.22, 72),
                arrowprops=dict(arrowstyle='->', color='#c44', lw=1.5))
    ax.text(1.78, 68, '卖股买债\n恢复比例', ha='center', fontproperties=font_prop,
            fontsize=9, color='#c44')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontproperties=font_prop, fontsize=12)
    ax.set_yticks(range(0, 110, 10))
    ax.set_yticklabels([f'{v}%' for v in range(0, 110, 10)], fontproperties=font_prop)
    ax.set_ylim(0, 115)
    ax.set_ylabel('仓位占比 %', fontproperties=font_prop, fontsize=12)
    ax.set_title('图7-3  再平衡操作示意：股债偏离后调整回目标比例',
                 fontproperties=font_prop, fontsize=13, pad=12)
    ax.legend(prop=font_prop, fontsize=10, loc='upper right')
    ax.grid(axis='y', linestyle=':', alpha=0.4)

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'ch7_rebalance.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  已保存: {out}')


# ═══════════════════════════════════════════════════════════════════════════════
# 图4：追涨杀跌陷阱
# 折线：基金净值 + 标注散户买入/卖出点 + 持有不动对比
# ═══════════════════════════════════════════════════════════════════════════════
def plot_chase_trap():
    np.random.seed(7)
    # 构造3年（36个月）净值曲线，呈W形
    t = np.linspace(0, 36, 37)
    # 用分段函数模拟：上涨→大跌→反弹→再跌→长期上涨
    nav_raw = np.array([
        1.00, 1.05, 1.12, 1.18, 1.25, 1.30,   # 0-5  上涨
        1.22, 1.10, 0.98, 0.87, 0.78, 0.72,   # 6-11 暴跌
        0.75, 0.80, 0.86, 0.92, 0.98, 1.05,   # 12-17 反弹
        1.10, 1.15, 1.08, 0.99, 0.90, 0.82,   # 18-23 再跌
        0.85, 0.91, 0.98, 1.06, 1.14, 1.22,   # 24-29 复苏
        1.28, 1.33, 1.38, 1.42, 1.47, 1.52,   # 30-35 稳步上涨
        1.55                                    # 36
    ])

    # 散户行为节点（月份索引, 行为标签, y偏移, 颜色）
    behavior_points = [
        (5,  '散户买入\n（追涨）',   +0.07, '#d73027'),
        (11, '散户卖出\n（割肉）',   -0.09, '#4575b4'),
        (17, '散户再次买入\n（反弹追入）', +0.07, '#d73027'),
        (23, '散户再次卖出\n（再次割肉）', -0.10, '#4575b4'),
        (36, '持有不动者\n终值 +55%', +0.07, '#1a9641'),
    ]

    fig, ax = plt.subplots(figsize=(11, 6))

    # 净值曲线
    ax.plot(t, nav_raw, color='#2c7bb6', linewidth=2.5, zorder=3, label='基金净值')
    ax.fill_between(t, nav_raw, 1.0, where=(nav_raw >= 1.0),
                    alpha=0.08, color='#1a9641', interpolate=True)
    ax.fill_between(t, nav_raw, 1.0, where=(nav_raw < 1.0),
                    alpha=0.08, color='#d73027', interpolate=True)
    ax.axhline(1.0, color='#888', linewidth=1, linestyle=':')

    # 标注行为点
    for (idx, label, dy, c) in behavior_points:
        nav_v = nav_raw[idx]
        marker = 'v' if '卖出' in label else '^'
        ax.scatter(idx, nav_v, color=c, s=120, marker=marker, zorder=6,
                   edgecolors='white', linewidths=1.2)
        ax.annotate(
            label,
            xy=(idx, nav_v),
            xytext=(idx, nav_v + dy),
            fontproperties=font_prop, fontsize=9,
            color=c,
            ha='center',
            arrowprops=dict(arrowstyle='->', color=c, lw=1.2),
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=c, alpha=0.85)
        )

    # 起点标注
    ax.scatter(0, nav_raw[0], color='#555', s=80, marker='o', zorder=6)
    ax.annotate('起点 1.00', xy=(0, nav_raw[0]), xytext=(1.5, 1.04),
                fontproperties=font_prop, fontsize=9, color='#555',
                arrowprops=dict(arrowstyle='->', color='#555'))

    # 累计亏损提示
    ax.text(18, 0.67,
            '散户追涨杀跌实际收益：约 -15%\n持有不动收益：+55%',
            fontproperties=font_prop, fontsize=10,
            color='#333',
            bbox=dict(boxstyle='round,pad=0.5', fc='#fff8e0', ec='#f4a430', alpha=0.92))

    ax.set_xticks(range(0, 37, 3))
    ax.set_xticklabels([f'第{m}月' for m in range(0, 37, 3)],
                       fontproperties=font_prop, fontsize=9, rotation=30)
    ax.set_ylabel('基金净值（元）', fontproperties=font_prop, fontsize=12)
    ax.set_ylim(0.55, 1.75)
    ax.set_title('图7-4  追涨杀跌陷阱：散户典型操作 vs 持有不动的收益对比',
                 fontproperties=font_prop, fontsize=13, pad=12)
    ax.legend(prop=font_prop, fontsize=10)
    ax.grid(linestyle=':', alpha=0.4)

    fig.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'ch7_chase_trap.png')
    fig.savefig(out, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'  已保存: {out}')


# ═══════════════════════════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('正在生成第七章配图...')
    plot_dca_effect()
    plot_asset_allocation()
    plot_rebalance()
    plot_chase_trap()
    print('\n全部完成！')
