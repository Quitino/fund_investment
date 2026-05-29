"""
第三章配套绘图代码
生成三张图像：
1. ch3_fund_structure.png  — 基金运作结构图
2. ch3_nav_calculation.png — 净值计算示意图
3. ch3_fee_impact.png      — 费率侵蚀效果图
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
import os

# ── 中文字体配置 ──────────────────────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════════════
# 图1：基金运作结构图
# ══════════════════════════════════════════════════════════════════════════════
def plot_fund_structure():
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    fig.patch.set_facecolor('#F8F9FA')

    fp = font_manager.FontProperties(fname=font_path)

    def draw_box(ax, x, y, w, h, text, subtext='', facecolor='#4A90D9', textcolor='white', fontsize=12):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                             boxstyle="round,pad=0.1",
                             facecolor=facecolor, edgecolor='white',
                             linewidth=2, zorder=3)
        ax.add_patch(box)
        ax.text(x, y + (0.15 if subtext else 0), text,
                ha='center', va='center', fontsize=fontsize,
                color=textcolor, fontweight='bold',
                fontproperties=fp, zorder=4)
        if subtext:
            ax.text(x, y - 0.28, subtext,
                    ha='center', va='center', fontsize=8.5,
                    color=textcolor, alpha=0.85,
                    fontproperties=fp, zorder=4)

    def draw_arrow(ax, x1, y1, x2, y2, label='', color='#333333', style='->'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color,
                                   lw=2.0, connectionstyle='arc3,rad=0.0'),
                    zorder=2)
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 0.05, my + 0.15, label,
                    ha='center', va='center', fontsize=8,
                    color=color, fontproperties=fp, zorder=5,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                              edgecolor=color, alpha=0.8))

    # 节点位置
    nodes = {
        '投资者\n（你）':       (1.5, 4.0, 1.6, 0.9,  '#5B8FF9', '认购/申购'),
        '基金公司':              (4.5, 6.0, 1.8, 0.9,  '#5AD8A6', '发行并管理基金'),
        '基金经理':              (4.5, 4.0, 1.8, 0.9,  '#F6BD16', '执行投资决策'),
        '证券市场':              (8.0, 4.0, 1.8, 0.9,  '#E8684A', '股票/债券/货币'),
        '托管银行':              (4.5, 2.0, 1.8, 0.9,  '#9B8EE2', '资金托管监督'),
    }

    for text, (x, y, w, h, color, sub) in nodes.items():
        draw_box(ax, x, y, w, h, text.replace('\n', ''), sub,
                 facecolor=color, fontsize=11)

    # 箭头
    draw_arrow(ax, 2.35, 4.0, 3.55, 4.0,  '申购资金', '#5B8FF9')
    draw_arrow(ax, 3.55, 4.0, 2.35, 4.0,  '基金份额', '#F6BD16')

    draw_arrow(ax, 4.5, 4.45, 4.5, 5.55, '汇报', '#5AD8A6')
    draw_arrow(ax, 4.5, 5.55, 4.5, 4.45, '指令', '#5AD8A6')

    draw_arrow(ax, 5.4, 4.0, 7.1, 4.0,  '买入指令', '#E8684A')
    draw_arrow(ax, 7.1, 4.0, 5.4, 4.0,  '资产收益', '#E8684A')

    # 托管银行 ↔ 基金经理（监督）
    draw_arrow(ax, 4.5, 3.55, 4.5, 2.45, '资金划转', '#9B8EE2')
    draw_arrow(ax, 4.5, 2.45, 4.5, 3.55, '监督合规', '#9B8EE2')

    # 投资者 ↔ 托管银行（赎回）
    ax.annotate('', xy=(1.5, 2.5), xytext=(1.5, 3.55),
                arrowprops=dict(arrowstyle='<->', color='#9B8EE2', lw=1.5),
                zorder=2)
    ax.text(0.95, 3.0, '赎回结算', ha='center', va='center', fontsize=8,
            color='#9B8EE2', fontproperties=fp,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor='#9B8EE2', alpha=0.8))

    ax.annotate('', xy=(3.55, 2.0), xytext=(1.5, 2.0),
                arrowprops=dict(arrowstyle='->', color='#9B8EE2', lw=1.5),
                zorder=2)
    ax.text(2.5, 1.75, '资金托管', ha='center', va='center', fontsize=8,
            color='#9B8EE2', fontproperties=fp)

    # 标题
    ax.set_title('基金运作结构示意图', fontsize=16, fontweight='bold',
                 fontproperties=fp, pad=15, color='#2C3E50')

    # 图例说明
    legend_text = '★ 托管银行独立保管资金，基金公司无法直接挪用，保障投资者安全'
    ax.text(5.0, 0.6, legend_text, ha='center', va='center', fontsize=9,
            color='#555555', fontproperties=fp,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF9E6',
                      edgecolor='#F6BD16', alpha=0.9))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'ch3_fund_structure.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已生成: {out}')


# ══════════════════════════════════════════════════════════════════════════════
# 图2：净值计算示意图
# ══════════════════════════════════════════════════════════════════════════════
def plot_nav_calculation():
    fig, axes = plt.subplots(1, 3, figsize=(14, 6),
                             gridspec_kw={'width_ratios': [2.5, 0.4, 1.2]})
    fig.patch.set_facecolor('#F8F9FA')
    fp = font_manager.FontProperties(fname=font_path)

    # ── 左图：持仓构成条形图 ──────────────────────────────────────────────────
    ax1 = axes[0]
    ax1.set_facecolor('#F8F9FA')

    categories = ['股票 A\n（腾讯）', '股票 B\n（茅台）', '股票 C\n（宁德）',
                  '债券', '现金/货币']
    values     = [3200, 2800, 1500, 1800, 700]
    colors     = ['#5B8FF9', '#5AD8A6', '#F6BD16', '#E8684A', '#9B8EE2']

    bars = ax1.barh(categories, values, color=colors, edgecolor='white',
                    linewidth=1.5, height=0.6)

    for bar, val in zip(bars, values):
        ax1.text(bar.get_width() + 80, bar.get_y() + bar.get_height()/2,
                 f'{val:,} 万元', va='center', ha='left',
                 fontsize=10, fontproperties=fp, color='#333333')

    ax1.set_xlabel('持仓市值（万元）', fontsize=11, fontproperties=fp)
    ax1.set_title('基金持仓构成', fontsize=13, fontweight='bold',
                  fontproperties=fp, pad=10)
    ax1.set_xlim(0, 4800)
    ax1.tick_params(axis='y', labelsize=9)
    for label in ax1.get_yticklabels():
        label.set_fontproperties(fp)
    for label in ax1.get_xticklabels():
        label.set_fontproperties(fp)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    total = sum(values)
    ax1.axvline(x=total/5*0, color='gray', lw=0)  # placeholder
    ax1.text(4600, -0.8, f'总资产\n= {total:,} 万元', ha='right', va='top',
             fontsize=11, fontweight='bold', color='#E8684A',
             fontproperties=fp,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF2EF',
                       edgecolor='#E8684A'))

    # ── 中间：箭头 + 公式 ────────────────────────────────────────────────────
    ax2 = axes[1]
    ax2.axis('off')
    ax2.set_facecolor('#F8F9FA')
    ax2.annotate('', xy=(0.9, 0.5), xytext=(0.1, 0.5),
                 xycoords='axes fraction',
                 arrowprops=dict(arrowstyle='->', color='#E8684A', lw=3))
    ax2.text(0.5, 0.62, '÷ 份额', ha='center', va='center',
             fontsize=11, fontweight='bold', color='#E8684A',
             fontproperties=fp, transform=ax2.transAxes)
    ax2.text(0.5, 0.38, '10,000\n万份', ha='center', va='center',
             fontsize=10, color='#555555',
             fontproperties=fp, transform=ax2.transAxes)

    # ── 右图：净值结果 ───────────────────────────────────────────────────────
    ax3 = axes[2]
    ax3.axis('off')
    ax3.set_facecolor('#F8F9FA')

    nav = total / 10000  # 单位净值
    ax3.text(0.5, 0.72, '单位净值（NAV）', ha='center', va='center',
             fontsize=12, fontweight='bold', color='#2C3E50',
             fontproperties=fp, transform=ax3.transAxes)
    ax3.text(0.5, 0.50, f'= {nav:.4f} 元', ha='center', va='center',
             fontsize=22, fontweight='bold', color='#5B8FF9',
             fontproperties=fp, transform=ax3.transAxes)
    ax3.text(0.5, 0.30, f'= {total:,} 万元\n÷ 10,000 万份',
             ha='center', va='center', fontsize=10, color='#777777',
             fontproperties=fp, transform=ax3.transAxes)
    ax3.text(0.5, 0.10, '即：每份基金\n价值约 1 元',
             ha='center', va='center', fontsize=10, color='#5AD8A6',
             fontproperties=fp, transform=ax3.transAxes,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0FFF8',
                       edgecolor='#5AD8A6'))

    rect = FancyBboxPatch((0.05, 0.02), 0.9, 0.96,
                          boxstyle='round,pad=0.02',
                          facecolor='#EEF3FF', edgecolor='#5B8FF9',
                          linewidth=2, transform=ax3.transAxes, zorder=0)
    ax3.add_patch(rect)

    fig.suptitle('基金净值（NAV）计算示意', fontsize=15, fontweight='bold',
                 fontproperties=fp, y=1.01, color='#2C3E50')

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'ch3_nav_calculation.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已生成: {out}')


# ══════════════════════════════════════════════════════════════════════════════
# 图3：费率侵蚀效果折线图
# ══════════════════════════════════════════════════════════════════════════════
def plot_fee_impact():
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    fp = font_manager.FontProperties(fname=font_path)

    principal = 10  # 10万元
    annual_return = 0.08  # 假设年化收益8%
    years = np.arange(0, 21)

    fee_scenarios = [
        ('0% 管理费（理论上限）',   0.000, '#5AD8A6', '--'),
        ('0.5% 管理费（指数基金）', 0.005, '#5B8FF9', '-'),
        ('1.5% 管理费（主动基金）', 0.015, '#F6BD16', '-'),
        ('2.5% 管理费（部分主动）', 0.025, '#E8684A', '-'),
    ]

    for label, fee, color, ls in fee_scenarios:
        net_return = annual_return - fee
        values = principal * (1 + net_return) ** years
        ax.plot(years, values, label=label, color=color,
                linewidth=2.5, linestyle=ls, marker='o',
                markersize=4, markevery=5)

        # 标注终值
        end_val = values[-1]
        ax.annotate(f'{end_val:.1f} 万',
                    xy=(20, end_val),
                    xytext=(20.3, end_val),
                    fontsize=9.5, color=color, fontproperties=fp,
                    va='center')

    # 标注差距
    val_0pct   = principal * (1 + annual_return) ** 20
    val_15pct  = principal * (1 + annual_return - 0.015) ** 20
    val_025pct = principal * (1 + annual_return - 0.025) ** 20
    gap_15  = val_0pct - val_15pct
    gap_025 = val_0pct - val_025pct

    ax.annotate(f'20年后差 {gap_15:.1f} 万',
                xy=(20, (val_0pct + val_15pct) / 2),
                xytext=(15.5, (val_0pct + val_15pct) / 2 + 1.5),
                fontsize=9, color='#F6BD16', fontproperties=fp,
                arrowprops=dict(arrowstyle='->', color='#F6BD16', lw=1.2))

    # 区域填充：0费率 vs 2.5%费率
    vals_0   = principal * (1 + annual_return) ** years
    vals_025 = principal * (1 + annual_return - 0.025) ** years
    ax.fill_between(years, vals_025, vals_0, alpha=0.08, color='#E8684A',
                    label=f'费率差异造成的损失区间')

    ax.set_xlabel('投资年数（年）', fontsize=12, fontproperties=fp)
    ax.set_ylabel('资产价值（万元）', fontsize=12, fontproperties=fp)
    ax.set_title(f'费率侵蚀效果：初始投入 {principal} 万元，年化收益假设 {annual_return*100:.0f}%',
                 fontsize=13, fontweight='bold', fontproperties=fp, pad=12)
    ax.set_xlim(0, 22)
    ax.set_xticks(range(0, 21, 5))

    for label in ax.get_xticklabels():
        label.set_fontproperties(fp)
    for label in ax.get_yticklabels():
        label.set_fontproperties(fp)

    legend = ax.legend(loc='upper left', fontsize=10,
                       prop=fp, framealpha=0.9,
                       edgecolor='#DDDDDD')

    ax.grid(True, alpha=0.3, linestyle='--', color='gray')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 注释框
    note = (f'关键结论：\n'
            f'• 0% vs 1.5% 管理费，20年差 {gap_15:.1f} 万（初始的{gap_15/principal*100:.0f}%）\n'
            f'• 0% vs 2.5% 管理费，20年差 {gap_025:.1f} 万（初始的{gap_025/principal*100:.0f}%）\n'
            f'• 费率不是"小事"——复利效应让它滚雪球般放大')
    ax.text(0.02, 0.97, note, transform=ax.transAxes,
            fontsize=9, va='top', fontproperties=fp,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFFBEA',
                      edgecolor='#F6BD16', alpha=0.95))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'ch3_fee_impact.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已生成: {out}')


# ── 主程序 ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('开始生成第三章配图...')
    plot_fund_structure()
    plot_nav_calculation()
    plot_fee_impact()
    print('全部图像已生成完毕！')
