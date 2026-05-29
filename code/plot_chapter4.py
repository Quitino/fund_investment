"""
第四章配套绘图脚本
生成3张图像：
  1. ch4_fund_types_risk.png  — 各类基金风险收益气泡图
  2. ch4_etf_vs_ofs.png       — ETF vs 场外基金雷达/分组条形图
  3. ch4_decision_tree.png    — 基金类型选择决策树流程图
"""

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as FancyBboxPatch
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch

# ── 字体设置 ──────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

OUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# 图1：各类基金风险收益气泡图
# ═══════════════════════════════════════════════════════════
def plot_fund_types_risk():
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    # (风险, 预期收益, 市场规模占比, 标签, 颜色)
    funds = [
        (1.0,  2.5,  28, '货币基金\n(余额宝/零钱通)', '#4ECDC4'),
        (2.2,  3.8,  18, '纯债基金\n(易方达纯债)', '#45B7D1'),
        (3.5,  5.5,  12, '混合偏债型\n(招商安心回报)', '#96CEB4'),
        (5.5,  8.0,  15, '混合偏股型\n(富国天惠)', '#FFEAA7'),
        (7.5, 12.0,  14, '股票型基金\n(工银瑞信核心)', '#FF6B6B'),
        (6.8, 10.5,   8, '指数增强\n(沪深300增强)', '#DDA0DD'),
        (7.0,  9.5,   5, 'QDII基金\n(华夏纳斯达克)', '#F0A500'),
    ]

    for risk, ret, size, label, color in funds:
        ax.scatter(risk, ret, s=size * 120, c=color, alpha=0.85,
                   edgecolors='white', linewidths=1.5, zorder=3)
        # 标签偏移
        offset_x = 0.25
        offset_y = 0.4
        if '货币' in label:
            offset_x, offset_y = -0.15, 0.5
        elif 'QDII' in label:
            offset_x, offset_y = 0.25, -0.6
        elif '指数增强' in label:
            offset_x, offset_y = 0.2, 0.5

        ax.annotate(label,
                    xy=(risk, ret),
                    xytext=(risk + offset_x, ret + offset_y),
                    fontproperties=font_prop, fontsize=9.5,
                    ha='left', va='center',
                    arrowprops=dict(arrowstyle='->', color='#555', lw=1),
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=color, lw=1.2, alpha=0.9))

    # 分区背景
    ax.axhspan(0, 5, alpha=0.06, color='#4ECDC4', zorder=1)
    ax.axhspan(5, 9, alpha=0.06, color='#FFEAA7', zorder=1)
    ax.axhspan(9, 16, alpha=0.06, color='#FF6B6B', zorder=1)

    ax.text(0.6, 4.5, '低风险区', fontproperties=font_prop, fontsize=9,
            color='#4ECDC4', alpha=0.8)
    ax.text(0.6, 8.5, '中风险区', fontproperties=font_prop, fontsize=9,
            color='#DAA520', alpha=0.8)
    ax.text(0.6, 14.5, '高风险区', fontproperties=font_prop, fontsize=9,
            color='#CC4444', alpha=0.8)

    ax.set_xlabel('风险程度（波动率）→', fontproperties=font_prop, fontsize=12, labelpad=8)
    ax.set_ylabel('预期年化收益率（%）→', fontproperties=font_prop, fontsize=12, labelpad=8)
    ax.set_title('各类基金风险收益分布图\n（气泡大小 = 市场规模占比）',
                 fontproperties=font_prop, fontsize=14, fontweight='bold', pad=15)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 16)
    ax.set_xticks([])
    ax.set_yticks(range(0, 17, 2))
    ax.yaxis.set_tick_params(labelsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.4, color='gray')
    ax.spines[['top', 'right']].set_visible(False)

    # 图例：规模
    for s, lbl in [(8*120, '大规模'), (5*120, '中规模'), (2*120, '小规模')]:
        ax.scatter([], [], s=s, c='#AAAAAA', alpha=0.6, label=lbl)
    ax.legend(prop=font_prop, fontsize=9, loc='lower right',
              title='市场规模', title_fontproperties=font_prop,
              framealpha=0.85, edgecolor='#ccc')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch4_fund_types_risk.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已保存: {path}')


# ═══════════════════════════════════════════════════════════
# 图2：ETF vs 场外基金 分组条形图
# ═══════════════════════════════════════════════════════════
def plot_etf_vs_ofs():
    dimensions = ['买卖便捷性', '综合费率', '起购门槛\n（灵活性）', '流动性', '持仓透明度']
    etf_scores   = [4.5, 4.2, 3.5, 4.8, 4.7]
    ofs_scores   = [3.8, 3.5, 4.5, 3.0, 3.2]

    x = np.arange(len(dimensions))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    bars1 = ax.bar(x - width/2, etf_scores, width, label='ETF（交易所交易基金）',
                   color='#4C9BE8', alpha=0.88, edgecolor='white', linewidth=1.2, zorder=3)
    bars2 = ax.bar(x + width/2, ofs_scores, width, label='场外基金（普通开放式）',
                   color='#FF8C69', alpha=0.88, edgecolor='white', linewidth=1.2, zorder=3)

    # 数值标签
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f'{h}',
                ha='center', va='bottom', fontproperties=font_prop, fontsize=10,
                color='#2255AA', fontweight='bold')
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f'{h}',
                ha='center', va='bottom', fontproperties=font_prop, fontsize=10,
                color='#CC4422', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(dimensions, fontproperties=font_prop, fontsize=11)
    ax.set_ylabel('评分（满分5分）', fontproperties=font_prop, fontsize=11, labelpad=8)
    ax.set_ylim(0, 5.8)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.yaxis.set_tick_params(labelsize=10)
    ax.set_title('ETF vs 场外基金 五维度对比\n（评分越高表示该维度越优）',
                 fontproperties=font_prop, fontsize=14, fontweight='bold', pad=15)

    ax.legend(prop=font_prop, fontsize=10, loc='upper right',
              framealpha=0.9, edgecolor='#ccc')
    ax.grid(axis='y', linestyle='--', alpha=0.4, color='gray', zorder=0)
    ax.spines[['top', 'right']].set_visible(False)

    # 注释框
    note = ('注：买卖便捷性—实时交易 vs 每日净值；费率—ETF通常更低；\n'
            '起购—场外基金1元起；流动性—ETF盘中随时成交；透明度—ETF每日披露持仓')
    ax.text(0.01, -0.18, note, transform=ax.transAxes,
            fontproperties=font_prop, fontsize=8, color='#666', va='top')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch4_etf_vs_ofs.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已保存: {path}')


# ═══════════════════════════════════════════════════════════
# 图3：基金类型选择决策树
# ═══════════════════════════════════════════════════════════
def draw_box(ax, x, y, w, h, text, fc, ec='#555', fontsize=10, bold=False):
    box = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle='round,pad=0.04',
                                   facecolor=fc, edgecolor=ec,
                                   linewidth=1.4, zorder=3)
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center',
            fontproperties=font_prop, fontsize=fontsize,
            fontweight=weight, color='#222', zorder=4, wrap=True,
            multialignment='center')


def draw_arrow(ax, x1, y1, x2, y2, label='', color='#888'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5), zorder=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.03, my, label, fontproperties=font_prop, fontsize=8.5,
                color='#444', ha='left', va='center', zorder=5)


def plot_decision_tree():
    fig, ax = plt.subplots(figsize=(14, 10))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # ── 层0：起点 ──
    draw_box(ax, 7, 9.2, 2.8, 0.7, '我应该买哪类基金？', '#B5D3E7', bold=True, fontsize=12)

    # ── 层1：投资期限 ──
    draw_box(ax, 7, 7.8, 2.8, 0.65, '投资期限是多久？', '#D5E8D4', fontsize=11)
    draw_arrow(ax, 7, 8.85, 7, 8.13)

    # 期限分支
    draw_box(ax, 2.5, 6.5, 2.4, 0.6, '< 1年（短期）', '#FFE6CC', fontsize=10)
    draw_box(ax, 7,   6.5, 2.4, 0.6, '1–3年（中期）', '#FFE6CC', fontsize=10)
    draw_box(ax, 11.5,6.5, 2.4, 0.6, '> 3年（长期）', '#FFE6CC', fontsize=10)

    draw_arrow(ax, 5.6, 7.47, 3.3,  6.8)
    draw_arrow(ax, 7,   7.47, 7,    6.8)
    draw_arrow(ax, 8.4, 7.47, 10.7, 6.8)

    # ── 层2：风险偏好（仅中/长期） ──
    # 短期 → 直接货币基金
    draw_box(ax, 2.5, 5.2, 2.4, 0.6, '风险偏好？', '#D5E8D4', fontsize=10)
    draw_box(ax, 7,   5.2, 2.4, 0.6, '风险偏好？', '#D5E8D4', fontsize=10)

    draw_arrow(ax, 2.5, 6.2, 2.5, 5.5)
    draw_arrow(ax, 7,   6.2, 7,   5.5)

    # 短期直达货基 → 不经过风险判断
    draw_box(ax, 2.5, 3.8, 2.2, 0.6, '货币基金\n余额宝/零钱通', '#E1D5E7', fontsize=9.5)
    draw_box(ax, 3.9, 5.2, 1.6, 0.6, '保守', '#FFF2CC', fontsize=9)
    draw_box(ax, 7,   3.8, 2.2, 0.6, '纯债/短债基金\n易方达纯债', '#E1D5E7', fontsize=9.5)

    # 中期分支
    draw_arrow(ax, 2.5, 5.5, 2.5, 4.1, '保守')
    draw_arrow(ax, 3.7, 5.2, 3.0, 4.1, '进取')

    # 进取 中期 → 混合
    draw_box(ax, 3.0, 3.8, 2.2, 0.6, '混合偏债/偏股\n招商安心回报等', '#E1D5E7', fontsize=9)
    draw_arrow(ax, 7, 5.5, 7, 4.1)

    # 长期 → 主动/被动
    draw_box(ax, 11.5, 5.2, 2.4, 0.6, '主动 or 被动？', '#D5E8D4', fontsize=10)
    draw_arrow(ax, 11.5, 6.2, 11.5, 5.5)

    draw_box(ax, 10.2, 3.8, 2.2, 0.6, '主动股票/混合\n易方达蓝筹精选', '#E1D5E7', fontsize=9)
    draw_box(ax, 12.8, 3.8, 2.2, 0.6, '指数/ETF\n沪深300ETF', '#E1D5E7', fontsize=9)

    draw_arrow(ax, 10.8, 5.2, 10.4, 4.1, '主动')
    draw_arrow(ax, 12.2, 5.2, 12.6, 4.1, '被动')

    # ── 层3：进一步细分 ──
    # 进取进取 → QDII/REITs
    draw_box(ax, 1.2, 2.5, 2.0, 0.58, 'QDII/REITs\n纳斯达克/华夏REITs', '#DAE8FC', fontsize=8.5)
    draw_box(ax, 3.7, 2.5, 2.0, 0.58, '指数增强\n沪深300增强等', '#DAE8FC', fontsize=8.5)

    draw_arrow(ax, 2.2, 3.5, 1.5, 2.79, '境外/另类')
    draw_arrow(ax, 3.6, 3.5, 3.5, 2.79, '量化增强')

    # 标题
    ax.set_title('基金类型选择决策树\n（从投资期限出发，逐步缩小选择范围）',
                 fontproperties=font_prop, fontsize=14, fontweight='bold',
                 pad=12, color='#222')

    # 图例
    legend_items = [
        mpatches.Patch(color='#D5E8D4', label='决策节点'),
        mpatches.Patch(color='#FFE6CC', label='期限分支'),
        mpatches.Patch(color='#E1D5E7', label='基金类型'),
        mpatches.Patch(color='#DAE8FC', label='细分类型'),
    ]
    ax.legend(handles=legend_items, prop=font_prop, fontsize=9,
              loc='lower right', framealpha=0.9, edgecolor='#ccc')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch4_decision_tree.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'已保存: {path}')


if __name__ == '__main__':
    print('正在生成第四章配图...')
    plot_fund_types_risk()
    plot_etf_vs_ofs()
    plot_decision_tree()
    print('全部完成！')
