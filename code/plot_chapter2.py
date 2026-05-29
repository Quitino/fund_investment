"""
第二章《金融市场全景图》配套绘图脚本
生成3张图：
  1. ch2_market_structure.png  — 金融市场结构图
  2. ch2_stock_vs_bond.png     — 股票vs债券收益对比
  3. ch2_index_composition.png — 沪深300指数行业分布
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch

# ── 字体设置 ──────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 输出目录 ──────────────────────────────────────────────
OUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUT_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════
# 图1：金融市场结构图
# ═══════════════════════════════════════════════════════════
def plot_market_structure():
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F7F9FC')

    fp = font_prop

    def draw_box(ax, x, y, w, h, color, label, sublabel=None, fontsize=13):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle="round,pad=0.12",
                             linewidth=1.8,
                             edgecolor='white',
                             facecolor=color,
                             zorder=2)
        ax.add_patch(box)
        if sublabel:
            ax.text(x + w / 2, y + h * 0.62, label,
                    ha='center', va='center', fontsize=fontsize,
                    fontweight='bold', color='white', zorder=3,
                    fontproperties=fp)
            ax.text(x + w / 2, y + h * 0.28, sublabel,
                    ha='center', va='center', fontsize=8.5,
                    color='#FFFFFFCC', zorder=3, fontproperties=fp)
        else:
            ax.text(x + w / 2, y + h / 2, label,
                    ha='center', va='center', fontsize=fontsize,
                    fontweight='bold', color='white', zorder=3,
                    fontproperties=fp)

    # 外框：金融市场
    outer = FancyBboxPatch((0.3, 0.3), 12.4, 7.2,
                           boxstyle="round,pad=0.2",
                           linewidth=2.5,
                           edgecolor='#2C3E50',
                           facecolor='#EBF5FB',
                           zorder=1)
    ax.add_patch(outer)
    ax.text(6.5, 7.2, '金融市场（Financial Markets）',
            ha='center', va='center', fontsize=15, fontweight='bold',
            color='#2C3E50', zorder=3, fontproperties=fp)

    # 五大市场子框
    markets = [
        # x,   y,   w,   h,   color,        name,       典型产品
        (0.7,  3.8, 2.3, 3.1, '#2980B9', '股票市场',  'A股/港股/美股\nETF/股票型基金'),
        (3.3,  3.8, 2.3, 3.1, '#27AE60', '债券市场',  '国债/企业债\n可转债/债券基金'),
        (5.9,  3.8, 2.3, 3.1, '#8E44AD', '货币市场',  '国债逆回购\n货币基金/存单'),
        (8.5,  3.8, 2.3, 3.1, '#E67E22', '外汇市场',  '人民币/美元\n欧元/日元'),
        (11.1, 3.8, 1.6, 3.1, '#C0392B', '商品\n市场',  '原油/黄金\n大豆/铜'),
    ]
    for (x, y, w, h, c, name, sub) in markets:
        draw_box(ax, x, y, w, h, c, name, sub, fontsize=12)

    # 底部：基金的位置
    fund_box = FancyBboxPatch((0.7, 0.6), 12.0, 2.8,
                              boxstyle="round,pad=0.12",
                              linewidth=2,
                              edgecolor='#F39C12',
                              facecolor='#FEF9E7',
                              zorder=2)
    ax.add_patch(fund_box)
    ax.text(6.7, 2.75, '基金（Fund）—— 集合理财工具，投资于以上各类市场',
            ha='center', va='center', fontsize=12, fontweight='bold',
            color='#784212', zorder=3, fontproperties=fp)

    # 基金类型小框
    fund_types = [
        (1.0, 0.85, 1.9, 1.55, '#F39C12', '股票型基金'),
        (3.2, 0.85, 1.9, 1.55, '#27AE60', '债券型基金'),
        (5.4, 0.85, 1.9, 1.55, '#8E44AD', '货币型基金'),
        (7.6, 0.85, 1.9, 1.55, '#2980B9', 'QDII基金'),
        (9.8, 0.85, 1.9, 1.55, '#C0392B', '混合型基金'),
        (12.0, 0.85, 0.5, 1.55, '#7F8C8D', '...'),
    ]
    for (x, y, w, h, c, name) in fund_types:
        draw_box(ax, x, y, w, h, c, name, fontsize=10)

    # 向上箭头
    arrow_xs = [1.85, 4.45, 7.05, 9.65, 11.9]
    for xc in arrow_xs:
        ax.annotate('', xy=(xc, 3.78), xytext=(xc, 2.42),
                    arrowprops=dict(arrowstyle='->', color='#888888',
                                   lw=1.5), zorder=4)

    plt.tight_layout(pad=0.5)
    out_path = os.path.join(OUT_DIR, 'ch2_market_structure.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  已保存: {out_path}')


# ═══════════════════════════════════════════════════════════
# 图2：股票 vs 债券收益对比
# ═══════════════════════════════════════════════════════════
def plot_stock_vs_bond():
    np.random.seed(42)
    months = 60  # 5年月度数据

    # 模拟股票价格（高波动，长期正收益）
    stock_returns = np.random.normal(0.008, 0.055, months)
    stock_price = 100 * np.cumprod(1 + stock_returns)

    # 模拟债券价格（低波动，稳定收益）
    bond_returns = np.random.normal(0.003, 0.008, months)
    bond_price = 100 * np.cumprod(1 + bond_returns)

    x = np.arange(months)
    x_labels = [f'{2019 + i // 12}年\n{(i % 12) + 1}月' if i % 12 == 0 else ''
                for i in range(months)]

    fp = font_prop
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True,
                                   gridspec_kw={'hspace': 0.08})
    fig.patch.set_facecolor('#F7F9FC')

    # ── 上图：股票 ──
    ax1.set_facecolor('#EBF5FB')
    ax1.plot(x, stock_price, color='#E74C3C', linewidth=1.8, label='模拟股票净值')
    ax1.fill_between(x, 100, stock_price,
                     where=(stock_price >= 100), alpha=0.25, color='#E74C3C')
    ax1.fill_between(x, 100, stock_price,
                     where=(stock_price < 100), alpha=0.25, color='#7F8C8D')
    ax1.axhline(100, color='#95A5A6', linewidth=1, linestyle='--')
    ax1.set_ylabel('净值（元）', fontproperties=fp, fontsize=11)
    final_stock = stock_price[-1]
    ax1.text(months - 1, final_stock,
             f'  终值:{final_stock:.0f}元\n  ({(final_stock/100-1)*100:+.1f}%)',
             va='center', fontsize=9, color='#E74C3C', fontproperties=fp)
    ax1.set_title('股票 vs 债券：5年价格走势模拟（初始100元）',
                  fontproperties=fp, fontsize=13, fontweight='bold',
                  color='#2C3E50', pad=10)

    # 标注波动率
    volatility_stock = np.std(stock_returns) * np.sqrt(12) * 100
    ax1.text(2, ax1.get_ylim()[0] * 1.02 if ax1.get_ylim()[0] > 0 else 60,
             f'年化波动率: {volatility_stock:.1f}%  |  风险高、弹性大',
             fontproperties=fp, fontsize=9.5, color='#E74C3C',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    ax1.legend(prop=fp, fontsize=10, loc='upper left')
    ax1.grid(axis='y', linestyle=':', alpha=0.5)

    # ── 下图：债券 ──
    ax2.set_facecolor('#EAFAF1')
    ax2.plot(x, bond_price, color='#27AE60', linewidth=1.8, label='模拟债券净值')
    ax2.fill_between(x, 100, bond_price, alpha=0.25, color='#27AE60')
    ax2.axhline(100, color='#95A5A6', linewidth=1, linestyle='--')
    ax2.set_ylabel('净值（元）', fontproperties=fp, fontsize=11)
    ax2.set_xlabel('时间', fontproperties=fp, fontsize=11)
    final_bond = bond_price[-1]
    ax2.text(months - 1, final_bond,
             f'  终值:{final_bond:.0f}元\n  ({(final_bond/100-1)*100:+.1f}%)',
             va='center', fontsize=9, color='#27AE60', fontproperties=fp)

    volatility_bond = np.std(bond_returns) * np.sqrt(12) * 100
    ax2.text(2, bond_price.min() * 0.998,
             f'年化波动率: {volatility_bond:.1f}%  |  风险低、收益稳',
             fontproperties=fp, fontsize=9.5, color='#27AE60',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    ax2.legend(prop=fp, fontsize=10, loc='upper left')
    ax2.grid(axis='y', linestyle=':', alpha=0.5)

    # x轴刻度
    tick_positions = [i for i in range(months) if i % 12 == 0]
    ax2.set_xticks(tick_positions)
    ax2.set_xticklabels([f'{2019 + i // 12}年' for i in tick_positions],
                        fontproperties=fp, fontsize=10)

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'ch2_stock_vs_bond.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  已保存: {out_path}')


# ═══════════════════════════════════════════════════════════
# 图3：沪深300指数行业分布
# ═══════════════════════════════════════════════════════════
def plot_index_composition():
    # 近似真实的沪深300行业权重（虚构但合理）
    industries = [
        '金融（银行/保险）', '消费（食品饮料）', '医药生物',
        '信息技术', '工业', '能源/材料',
        '房地产', '公用事业', '电信服务',
    ]
    weights = [28.5, 16.2, 11.8, 10.4, 9.6, 8.3, 5.7, 5.2, 4.3]
    colors = [
        '#2980B9', '#E67E22', '#27AE60',
        '#8E44AD', '#1ABC9C', '#C0392B',
        '#F39C12', '#7F8C8D', '#2C3E50',
    ]

    fp = font_prop
    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(14, 6.5))
    fig.patch.set_facecolor('#F7F9FC')
    fig.suptitle('沪深300指数行业构成示意（模拟权重）',
                 fontproperties=fp, fontsize=14, fontweight='bold',
                 color='#2C3E50', y=1.01)

    # ── 左：饼图 ──
    ax_pie.set_facecolor('#F7F9FC')
    wedges, texts, autotexts = ax_pie.pie(
        weights,
        labels=None,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140,
        pctdistance=0.78,
        wedgeprops=dict(linewidth=1.5, edgecolor='white'),
    )
    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_fontproperties(fp)
        at.set_color('white')
        at.set_fontweight('bold')

    # 图例放在饼图右侧
    legend_labels = [f'{ind}  {w:.1f}%' for ind, w in zip(industries, weights)]
    legend_patches = [mpatches.Patch(color=c, label=l)
                      for c, l in zip(colors, legend_labels)]
    ax_pie.legend(handles=legend_patches,
                  loc='center left', bbox_to_anchor=(1.0, 0.5),
                  prop=fp, fontsize=9, framealpha=0.9,
                  title='行业', title_fontproperties=fp)
    ax_pie.set_title('权重饼图', fontproperties=fp, fontsize=12, pad=8)

    # ── 右：横向条形图 ──
    ax_bar.set_facecolor('#F7F9FC')
    sorted_idx = np.argsort(weights)
    sorted_weights = [weights[i] for i in sorted_idx]
    sorted_industries = [industries[i] for i in sorted_idx]
    sorted_colors = [colors[i] for i in sorted_idx]

    bars = ax_bar.barh(range(len(industries)), sorted_weights,
                       color=sorted_colors, edgecolor='white', linewidth=1)
    ax_bar.set_yticks(range(len(industries)))
    ax_bar.set_yticklabels(sorted_industries, fontproperties=fp, fontsize=9.5)
    ax_bar.set_xlabel('指数权重 (%)', fontproperties=fp, fontsize=11)
    ax_bar.set_title('行业权重排名', fontproperties=fp, fontsize=12, pad=8)

    # 数值标签
    for i, (bar, w) in enumerate(zip(bars, sorted_weights)):
        ax_bar.text(w + 0.3, i, f'{w:.1f}%',
                    va='center', fontsize=9, color='#2C3E50',
                    fontproperties=fp)
    ax_bar.set_xlim(0, max(weights) * 1.2)
    ax_bar.grid(axis='x', linestyle=':', alpha=0.5)
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)

    # 注释
    fig.text(0.5, -0.03,
             '注：以上行业权重为示意性虚构数据，仅用于教学说明，不代表实际指数构成',
             ha='center', fontproperties=fp, fontsize=9, color='#7F8C8D')

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'ch2_index_composition.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  已保存: {out_path}')


# ═══════════════════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print('正在生成第二章配图...')
    print('[1/3] 金融市场结构图')
    plot_market_structure()
    print('[2/3] 股票vs债券对比图')
    plot_stock_vs_bond()
    print('[3/3] 沪深300指数行业分布图')
    plot_index_composition()
    print('全部完成！')
