"""
第八章配套绘图代码
《基金投资理财入门教程》Chapter 8 Plots — 风险管理
生成图像保存到 docs/pic/ 目录
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch

# ── 字体配置 ──────────────────────────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 输出目录 ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# 图1：最大回撤示意图
# ─────────────────────────────────────────────────────────────────────────────
def plot_drawdown():
    np.random.seed(42)
    n = 120  # 月数（10年）

    # 构造一条有明显回撤的净值曲线
    # 分阶段：上涨 → 大幅回撤 → 修复 → 继续上涨
    t = np.linspace(0, 1, n)
    trend = 1.0 + 1.2 * t  # 长期上涨趋势

    # 叠加随机扰动
    noise = np.cumsum(np.random.normal(0, 0.015, n))

    # 构造回撤区间（月35-70期间）
    drawdown_mask = np.zeros(n)
    drawdown_mask[35:70] = 1
    drawdown_shape = np.sin(np.linspace(0, np.pi, 35)) * (-0.45)  # -45% 回撤深度
    drawdown_component = np.zeros(n)
    drawdown_component[35:70] = drawdown_shape

    nav = trend + noise * 0.3 + drawdown_component
    nav = np.maximum(nav, 0.5)  # 净值不低于0.5

    # 归一化起始值为 1.0
    nav = nav / nav[0]

    # 找最大回撤区间：峰值在第35月附近
    peak_idx = 35
    trough_idx = 35 + np.argmin(nav[35:70])
    peak_val = nav[peak_idx]
    trough_val = nav[trough_idx]
    max_dd = (trough_val - peak_val) / peak_val  # 约 -35%

    months = np.arange(n)

    fig, ax = plt.subplots(figsize=(12, 6))

    # 净值曲线
    ax.plot(months, nav, color='#2c7bb6', linewidth=2.5, label='基金净值', zorder=3)

    # 填充回撤区域（峰值到谷值）
    ax.fill_between(
        months[peak_idx:trough_idx + 1],
        nav[peak_idx:trough_idx + 1],
        peak_val,
        alpha=0.25, color='#d7191c', label='最大回撤区间'
    )

    # 峰值水平参考线（虚线延伸到谷值）
    ax.hlines(peak_val, peak_idx, trough_idx,
              colors='#d7191c', linewidths=1.5, linestyles='--', zorder=4)

    # 标注峰值点
    ax.scatter([peak_idx], [peak_val], color='#d7191c', s=120, zorder=6)
    ax.annotate(
        f'历史最高点\n净值 = {peak_val:.2f}',
        xy=(peak_idx, peak_val),
        xytext=(peak_idx - 18, peak_val + 0.15),
        fontproperties=font_prop, fontsize=10, color='#d7191c',
        arrowprops=dict(arrowstyle='->', color='#d7191c', lw=1.5),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff5f5', edgecolor='#d7191c', alpha=0.8)
    )

    # 标注谷值点
    ax.scatter([trough_idx], [trough_val], color='#d7191c', s=120, zorder=6, marker='v')
    ax.annotate(
        f'区间最低点\n净值 = {trough_val:.2f}',
        xy=(trough_idx, trough_val),
        xytext=(trough_idx + 5, trough_val - 0.18),
        fontproperties=font_prop, fontsize=10, color='#d7191c',
        arrowprops=dict(arrowstyle='->', color='#d7191c', lw=1.5),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff5f5', edgecolor='#d7191c', alpha=0.8)
    )

    # 双向箭头标注回撤幅度
    mid_x = (peak_idx + trough_idx) // 2
    ax.annotate(
        '',
        xy=(mid_x, trough_val),
        xytext=(mid_x, peak_val),
        arrowprops=dict(arrowstyle='<->', color='#d7191c', lw=2.0)
    )
    ax.text(
        mid_x + 2, (peak_val + trough_val) / 2,
        f'最大回撤\n≈ {max_dd * 100:.1f}%\n（从最高点跌了{abs(max_dd) * 100:.1f}%）',
        fontproperties=font_prop, fontsize=11, color='#d7191c', fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fffbe6', edgecolor='#d7191c', alpha=0.9)
    )

    # 最终净值标注
    final_val = nav[-1]
    ax.scatter([n - 1], [final_val], color='#1a9641', s=100, zorder=6)
    ax.annotate(
        f'当前净值 = {final_val:.2f}',
        xy=(n - 1, final_val),
        xytext=(n - 25, final_val + 0.12),
        fontproperties=font_prop, fontsize=10, color='#1a9641',
        arrowprops=dict(arrowstyle='->', color='#1a9641', lw=1.5),
    )

    ax.set_xlabel('时间（月）', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('基金净值（元）', fontproperties=font_prop, fontsize=13)
    ax.set_title('最大回撤示意图：衡量"最惨的时候亏了多少"',
                 fontproperties=font_prop, fontsize=15, fontweight='bold')
    ax.set_xlim(-2, n + 2)
    ax.legend(prop=font_prop, fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.25, linestyle='--')

    # 公式注释
    formula = (
        '最大回撤 = (谷值净值 - 峰值净值) / 峰值净值 × 100%\n'
        '衡量区间内从最高点下跌至最低点的最大跌幅'
    )
    ax.text(
        0.01, 0.03, formula,
        transform=ax.transAxes,
        fontproperties=font_prop, fontsize=9.5, color='#555555',
        verticalalignment='bottom',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#f0f4f8', edgecolor='#aaaaaa', alpha=0.85)
    )

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch8_drawdown.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图2：夏普比率对比（分组条形图）
# ─────────────────────────────────────────────────────────────────────────────
def plot_sharpe_comparison():
    funds = ['基金A\n（高收益高波动）', '基金B\n（中收益低波动）', '基金C\n（低收益低波动）']
    annual_return = np.array([18.0, 12.0, 6.5])   # 年化收益率 %
    annual_vol    = np.array([28.0, 10.0, 5.0])    # 年化波动率 %
    rf = 2.5                                        # 无风险利率 %
    sharpe = (annual_return - rf) / annual_vol

    x = np.arange(len(funds))
    width = 0.25

    fig, ax1 = plt.subplots(figsize=(11, 7))
    ax2 = ax1.twinx()

    color_ret = '#e74c3c'
    color_vol = '#3498db'
    color_sh  = '#2ecc71'

    bars1 = ax1.bar(x - width, annual_return, width, label='年化收益率 (%)',
                    color=color_ret, alpha=0.85, edgecolor='white', linewidth=1.2)
    bars2 = ax1.bar(x,          annual_vol,   width, label='年化波动率 (%)',
                    color=color_vol, alpha=0.85, edgecolor='white', linewidth=1.2)
    bars3 = ax2.bar(x + width,  sharpe,       width, label='夏普比率',
                    color=color_sh,  alpha=0.85, edgecolor='white', linewidth=1.2)

    # 在每个条形上方标注数值
    def autolabel(bars, ax, fmt='{:.1f}', color='black'):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2., height + 0.3,
                fmt.format(height),
                ha='center', va='bottom',
                fontproperties=font_prop, fontsize=11,
                color=color, fontweight='bold'
            )

    autolabel(bars1, ax1, '{:.1f}%', color_ret)
    autolabel(bars2, ax1, '{:.1f}%', color_vol)
    autolabel(bars3, ax2, '{:.2f}', '#1a7a3e')

    ax1.set_ylabel('年化收益率 / 年化波动率 (%)', fontproperties=font_prop, fontsize=12)
    ax2.set_ylabel('夏普比率', fontproperties=font_prop, fontsize=12, color='#1a7a3e')
    ax2.tick_params(axis='y', colors='#1a7a3e')
    ax2.set_ylim(0, 1.6)

    ax1.set_xticks(x)
    ax1.set_xticklabels(funds, fontproperties=font_prop, fontsize=12)
    ax1.set_ylim(0, 38)
    ax1.set_title('三只基金夏普比率对比\n——单位风险所获得的超额收益',
                  fontproperties=font_prop, fontsize=15, fontweight='bold')

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, prop=font_prop, fontsize=11,
               loc='upper right', framealpha=0.9)

    ax1.grid(True, axis='y', alpha=0.3, linestyle='--')

    # 结论注释
    winner_idx = np.argmax(sharpe)
    conclusion = (
        f'结论：基金B夏普比率最高（{sharpe[1]:.2f}），\n'
        f'同等风险下超额收益最优，是性价比最高的选择。\n'
        f'公式：Sharpe = (Rp - Rf) / σp，Rf = {rf}%（无风险利率）'
    )
    ax1.text(
        0.01, 0.97, conclusion,
        transform=ax1.transAxes,
        fontproperties=font_prop, fontsize=9.5, color='#333333',
        verticalalignment='top',
        bbox=dict(boxstyle='round,pad=0.45', facecolor='#eafaf1', edgecolor='#2ecc71', alpha=0.9)
    )

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch8_sharpe_comparison.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图3：仓位管理示意（分组堆积条形图）
# ─────────────────────────────────────────────────────────────────────────────
def plot_position_sizing():
    profiles = ['保守型', '平衡型', '进取型']

    # 各类别占总资产比例（%），三组合计 = 100
    # [投资资金（高风险权益）, 投资资金（低风险固收）, 应急备用金, 日常生活资金]
    data = {
        '权益类投资\n（股票/偏股基金）': [10,  25,  45],
        '固收类投资\n（债券/货币基金）': [30,  25,  20],
        '应急备用金\n（3-6个月生活费）': [30,  30,  20],
        '日常生活资金\n（随时可用）':     [30,  20,  15],
    }

    colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db']
    x = np.arange(len(profiles))
    bar_width = 0.5

    fig, ax = plt.subplots(figsize=(10, 7))

    bottom = np.zeros(len(profiles))
    bars_list = []
    for (category, values), color in zip(data.items(), colors):
        vals = np.array(values)
        bars = ax.bar(x, vals, bar_width, bottom=bottom, label=category,
                      color=color, alpha=0.88, edgecolor='white', linewidth=1.5)
        bars_list.append((bars, vals, bottom.copy()))
        # 在每段中间标百分比
        for i, (bar, val, bot) in enumerate(zip(bars, vals, bottom)):
            if val >= 8:  # 只在足够高的区块标注
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    bot + val / 2.,
                    f'{val}%',
                    ha='center', va='center',
                    fontproperties=font_prop, fontsize=12,
                    color='white', fontweight='bold'
                )
        bottom += vals

    # 在条形顶部标注总计
    for i, profile in enumerate(profiles):
        ax.text(x[i], 102, '100%', ha='center', va='bottom',
                fontproperties=font_prop, fontsize=11, color='#333333', fontweight='bold')

    ax.set_xticks(x)
    ax.set_xticklabels(profiles, fontproperties=font_prop, fontsize=14, fontweight='bold')
    ax.set_ylabel('占总资产比例 (%)', fontproperties=font_prop, fontsize=13)
    ax.set_title('不同风险偏好的建议仓位配置\n——永远不要把所有鸡蛋放在一个篮子里',
                 fontproperties=font_prop, fontsize=15, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.set_xlim(-0.6, 2.6)

    # 图例放在右侧
    ax.legend(prop=font_prop, fontsize=10.5, loc='upper right',
              framealpha=0.9, bbox_to_anchor=(1.0, 0.98))

    ax.grid(True, axis='y', alpha=0.25, linestyle='--')
    ax.set_yticks(range(0, 101, 10))

    # 关键提示
    tips = (
        '核心原则：\n'
        '① 先留应急备用金（3-6个月生活费）\n'
        '② 投资资金中再做资产配置\n'
        '③ 进取型≠全仓，仍需保留流动性缓冲'
    )
    ax.text(
        -0.55, 60, tips,
        fontproperties=font_prop, fontsize=9.5, color='#333333',
        verticalalignment='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef9e7', edgecolor='#f39c12', alpha=0.9)
    )

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch8_position_sizing.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('开始生成第八章配图（风险管理）...')
    plot_drawdown()
    plot_sharpe_comparison()
    plot_position_sizing()
    print('全部图像生成完毕。')
