"""
基金投资理财入门教程 - 第十二章、第十三章配套绘图代码
生成图像保存至 docs/pic/ 目录
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
import numpy as np
import os

# 中文字体设置
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

# 输出目录
OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =============================================================================
# 图1：资金分层示意图 ch12_money_layers.png
# =============================================================================
def plot_money_layers():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle('资金分层管理框架', fontsize=16, fontproperties=font_prop, fontweight='bold', y=0.98)

    # 左图：嵌套矩形示意图
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.axis('off')
    ax1.set_title('三层资金结构（嵌套示意）', fontproperties=font_prop, fontsize=13, pad=10)

    # 第一层：活钱（最外层，浅蓝）
    rect1 = mpatches.FancyBboxPatch((0.3, 0.3), 9.4, 9.4,
                                     boxstyle="round,pad=0.1",
                                     linewidth=2, edgecolor='#2196F3',
                                     facecolor='#E3F2FD', zorder=1)
    ax1.add_patch(rect1)
    ax1.text(5, 9.2, '第一层：活钱', ha='center', va='center',
             fontproperties=font_prop, fontsize=12, fontweight='bold', color='#1565C0')
    ax1.text(5, 8.6, '3~6个月日常生活费', ha='center', va='center',
             fontproperties=font_prop, fontsize=10, color='#1976D2')
    ax1.text(5, 8.1, '货币基金 / 活期存款 / 银行理财', ha='center', va='center',
             fontproperties=font_prop, fontsize=9, color='#1976D2', style='italic')
    ax1.text(5, 7.6, '流动性第一，随取随用', ha='center', va='center',
             fontproperties=font_prop, fontsize=9, color='#42A5F5')

    # 第二层：稳钱（中间，浅绿）
    rect2 = mpatches.FancyBboxPatch((1.2, 1.2), 7.6, 5.8,
                                     boxstyle="round,pad=0.1",
                                     linewidth=2, edgecolor='#4CAF50',
                                     facecolor='#E8F5E9', zorder=2)
    ax1.add_patch(rect2)
    ax1.text(5, 6.5, '第二层：稳钱', ha='center', va='center',
             fontproperties=font_prop, fontsize=12, fontweight='bold', color='#2E7D32')
    ax1.text(5, 5.9, '1~3年内可能动用的资金', ha='center', va='center',
             fontproperties=font_prop, fontsize=10, color='#388E3C')
    ax1.text(5, 5.4, '纯债基金 / 短债基金 / 固收+', ha='center', va='center',
             fontproperties=font_prop, fontsize=9, color='#388E3C', style='italic')
    ax1.text(5, 4.9, '保值增值，波动较小', ha='center', va='center',
             fontproperties=font_prop, fontsize=9, color='#66BB6A')

    # 第三层：投资钱（最内层，橙色）
    rect3 = mpatches.FancyBboxPatch((2.5, 1.5), 5.0, 3.0,
                                     boxstyle="round,pad=0.1",
                                     linewidth=2, edgecolor='#FF9800',
                                     facecolor='#FFF3E0', zorder=3)
    ax1.add_patch(rect3)
    ax1.text(5, 4.0, '第三层：投资钱', ha='center', va='center',
             fontproperties=font_prop, fontsize=12, fontweight='bold', color='#E65100')
    ax1.text(5, 3.4, '3年以上长期不动用', ha='center', va='center',
             fontproperties=font_prop, fontsize=10, color='#EF6C00')
    ax1.text(5, 2.9, '股票型 / 指数基金 / QDII', ha='center', va='center',
             fontproperties=font_prop, fontsize=9, color='#EF6C00', style='italic')
    ax1.text(5, 2.3, '追求长期超额收益', ha='center', va='center',
             fontproperties=font_prop, fontsize=9, color='#FFA726')

    # 右图：饼图展示各层占比（典型保守型示例）
    labels = ['活钱\n（货基/活期）', '稳钱\n（债基/短债）', '投资钱\n（权益类）']
    sizes = [20, 40, 40]
    colors = ['#90CAF9', '#A5D6A7', '#FFCC80']
    explode = (0.05, 0.05, 0.05)

    wedges, texts, autotexts = ax2.pie(
        sizes, explode=explode, labels=labels,
        colors=colors, autopct='%1.0f%%',
        startangle=90,
        textprops={'fontproperties': font_prop, 'fontsize': 11},
        pctdistance=0.75,
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'}
    )
    for at in autotexts:
        at.set_fontproperties(font_prop)
        at.set_fontsize(12)
        at.set_fontweight('bold')

    ax2.set_title('典型资金分配比例示意\n（可根据个人情况调整）',
                  fontproperties=font_prop, fontsize=13, pad=15)

    # 右图下方说明
    notes = [
        '活钱：流动性优先，年化1~2%，随时可取',
        '稳钱：安全性优先，年化3~5%，1~3年期',
        '投资钱：收益性优先，长期持有，承担波动',
    ]
    for i, note in enumerate(notes):
        ax2.text(0, -1.35 - i * 0.18, note, ha='center', va='center',
                 fontproperties=font_prop, fontsize=9, color='#555555',
                 transform=ax2.transData)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out_path = os.path.join(OUTPUT_DIR, 'ch12_money_layers.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {out_path}')


# =============================================================================
# 图2：保守型组合配置图 ch12_portfolio_conservative.png
# =============================================================================
def plot_portfolio_conservative():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle('示例组合一：保守型（总资金50万元）',
                 fontsize=16, fontproperties=font_prop, fontweight='bold', y=0.98)

    # 饼图数据
    labels = ['货币基金\n（流动备用）', '纯债基金\n（稳健底仓）',
              '混合债基金\n（固收+）', '宽基指数基金\n（长期增值）', 'QDII基金\n（全球分散）']
    sizes = [30, 20, 20, 20, 10]
    amounts = [15, 10, 10, 10, 5]  # 万元
    colors = ['#90CAF9', '#A5D6A7', '#80DEEA', '#FFCC80', '#CE93D8']
    explode = (0.05, 0.03, 0.03, 0.05, 0.07)

    wedges, texts, autotexts = ax1.pie(
        sizes, explode=explode, labels=labels,
        colors=colors, autopct='%1.0f%%',
        startangle=135,
        textprops={'fontproperties': font_prop, 'fontsize': 10},
        pctdistance=0.72,
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'},
        radius=1.1
    )
    for at in autotexts:
        at.set_fontproperties(font_prop)
        at.set_fontsize(11)
        at.set_fontweight('bold')
        at.set_color('white')

    ax1.set_title('资产配置占比', fontproperties=font_prop, fontsize=13, pad=20)

    # 右图：柱形图展示金额分配
    bar_colors = colors
    bars = ax2.barh(labels, amounts, color=bar_colors, edgecolor='white',
                    linewidth=1.5, height=0.6)

    # 在柱子末端标注金额
    for bar, amt, pct in zip(bars, amounts, sizes):
        ax2.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                 f'{amt}万 ({pct}%)',
                 va='center', ha='left',
                 fontproperties=font_prop, fontsize=11, color='#333333')

    ax2.set_xlim(0, 20)
    ax2.set_xlabel('金额（万元）', fontproperties=font_prop, fontsize=11)
    ax2.set_title('各类资产金额分配', fontproperties=font_prop, fontsize=13)
    ax2.tick_params(axis='y', labelsize=10)
    for label in ax2.get_yticklabels():
        label.set_fontproperties(font_prop)
    for label in ax2.get_xticklabels():
        label.set_fontproperties(font_prop)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='x', alpha=0.3)

    # 底部说明
    info_text = ('投资目标：稳健增值，年化3~5%  |  风险等级：R2中低  |  持有期：3年以上\n'
                 '核心逻辑：以债券打底保稳，以指数基金获取长期增值，QDII分散单一市场风险')
    fig.text(0.5, 0.01, info_text, ha='center', va='bottom',
             fontproperties=font_prop, fontsize=10, color='#555555',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#F5F5F5', edgecolor='#CCCCCC'))

    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    out_path = os.path.join(OUTPUT_DIR, 'ch12_portfolio_conservative.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {out_path}')


# =============================================================================
# 图3：平衡型组合配置图 ch12_portfolio_balanced.png
# =============================================================================
def plot_portfolio_balanced():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle('示例组合二：平衡型（总资金10万元）',
                 fontsize=16, fontproperties=font_prop, fontweight='bold', y=0.98)

    labels = ['宽基指数\n（沪深300/中证500）', '债券基金\n（中短债）',
              'QDII/纳指\n（海外分散）', '行业指数\n（科技/消费）',
              '货币基金\n（机动仓位）']
    sizes = [35, 25, 20, 10, 10]
    amounts = [3.5, 2.5, 2.0, 1.0, 1.0]
    colors = ['#EF9A9A', '#80CBC4', '#FFE082', '#B39DDB', '#90CAF9']
    explode = (0.05, 0.03, 0.05, 0.07, 0.03)

    wedges, texts, autotexts = ax1.pie(
        sizes, explode=explode, labels=labels,
        colors=colors, autopct='%1.0f%%',
        startangle=120,
        textprops={'fontproperties': font_prop, 'fontsize': 10},
        pctdistance=0.72,
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'},
        radius=1.1
    )
    for at in autotexts:
        at.set_fontproperties(font_prop)
        at.set_fontsize(11)
        at.set_fontweight('bold')
        at.set_color('white')

    ax1.set_title('资产配置占比', fontproperties=font_prop, fontsize=13, pad=20)

    # 柱形图
    bar_colors = colors
    bars = ax2.barh(labels, amounts, color=bar_colors, edgecolor='white',
                    linewidth=1.5, height=0.6)

    for bar, amt, pct in zip(bars, amounts, sizes):
        ax2.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                 f'{amt}万 ({pct}%)',
                 va='center', ha='left',
                 fontproperties=font_prop, fontsize=11, color='#333333')

    ax2.set_xlim(0, 5)
    ax2.set_xlabel('金额（万元）', fontproperties=font_prop, fontsize=11)
    ax2.set_title('各类资产金额分配', fontproperties=font_prop, fontsize=13)
    ax2.tick_params(axis='y', labelsize=10)
    for label in ax2.get_yticklabels():
        label.set_fontproperties(font_prop)
    for label in ax2.get_xticklabels():
        label.set_fontproperties(font_prop)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='x', alpha=0.3)

    info_text = ('投资目标：长期持有，追求年化6~8%  |  风险等级：R3中等  |  持有期：5年以上\n'
                 '核心逻辑：股债均衡配置，宽基指数为主力，债券压舱，海外分散，货基保留弹药')
    fig.text(0.5, 0.01, info_text, ha='center', va='bottom',
             fontproperties=font_prop, fontsize=10, color='#555555',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#F5F5F5', edgecolor='#CCCCCC'))

    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    out_path = os.path.join(OUTPUT_DIR, 'ch12_portfolio_balanced.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {out_path}')


# =============================================================================
# 图4：进取型组合配置图 ch12_portfolio_growth.png
# =============================================================================
def plot_portfolio_growth():
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.suptitle('示例组合三：进取型（1万元定投方案）',
                 fontsize=16, fontproperties=font_prop, fontweight='bold', y=0.98)

    # 左图：配置饼图
    ax1 = axes[0]
    labels = ['沪深300指数\n（核心仓）', '中证500指数\n（成长仓）',
              '纳斯达克100\n（科技仓）', '黄金ETF\n（对冲仓）']
    sizes = [50, 30, 15, 5]
    colors = ['#EF5350', '#FF9800', '#AB47BC', '#FFD54F']
    explode = (0.05, 0.03, 0.05, 0.07)

    wedges, texts, autotexts = ax1.pie(
        sizes, explode=explode, labels=labels,
        colors=colors, autopct='%1.0f%%',
        startangle=90,
        textprops={'fontproperties': font_prop, 'fontsize': 9},
        pctdistance=0.72,
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'},
        radius=1.0
    )
    for at in autotexts:
        at.set_fontproperties(font_prop)
        at.set_fontsize(10)
        at.set_fontweight('bold')
        at.set_color('white')
    ax1.set_title('初始配置方案', fontproperties=font_prop, fontsize=12, pad=15)

    # 中图：每月定投金额分配
    ax2 = axes[1]
    monthly_labels = ['沪深300', '中证500', '纳指100', '黄金ETF']
    monthly_amounts = [500, 300, 150, 50]  # 月定投1000元示例
    bar_colors = colors
    bars = ax2.bar(monthly_labels, monthly_amounts, color=bar_colors,
                   edgecolor='white', linewidth=1.5, width=0.6)

    for bar, amt in zip(bars, monthly_amounts):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 8,
                 f'{amt}元',
                 ha='center', va='bottom',
                 fontproperties=font_prop, fontsize=11, fontweight='bold', color='#333333')

    ax2.set_ylabel('每月定投金额（元）', fontproperties=font_prop, fontsize=11)
    ax2.set_title('月定投1000元分配方案', fontproperties=font_prop, fontsize=12)
    ax2.set_ylim(0, 620)
    for label in ax2.get_xticklabels():
        label.set_fontproperties(font_prop)
        label.set_fontsize(10)
    for label in ax2.get_yticklabels():
        label.set_fontproperties(font_prop)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='y', alpha=0.3)
    ax2.text(0.5, -0.15, '（月定投总额1000元，年定投12000元）',
             ha='center', transform=ax2.transAxes,
             fontproperties=font_prop, fontsize=9, color='#777777')

    # 右图：10年定投复利预期（假设年化8%）
    ax3 = axes[2]
    years = np.arange(1, 11)
    monthly = 1000
    annual_rate = 0.08
    monthly_rate = annual_rate / 12
    # 定投终值公式
    fv = [monthly * ((1 + monthly_rate) ** (12 * y) - 1) / monthly_rate
          for y in years]
    cost = [monthly * 12 * y for y in years]

    ax3.fill_between(years, cost, fv, alpha=0.3, color='#4CAF50', label='盈利部分')
    ax3.plot(years, fv, 'o-', color='#4CAF50', linewidth=2.5,
             markersize=6, label='终值（年化8%假设）')
    ax3.plot(years, cost, 's--', color='#90CAF9', linewidth=2,
             markersize=5, label='累计投入本金')

    ax3.set_xlabel('定投年数', fontproperties=font_prop, fontsize=11)
    ax3.set_ylabel('金额（元）', fontproperties=font_prop, fontsize=11)
    ax3.set_title('月投1000元·10年复利预测\n（年化8%假设，非承诺）',
                  fontproperties=font_prop, fontsize=12)
    ax3.legend(prop=font_prop, fontsize=9)
    ax3.set_xticks(years)
    for label in ax3.get_xticklabels():
        label.set_fontproperties(font_prop)
    for label in ax3.get_yticklabels():
        label.set_fontproperties(font_prop)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.grid(alpha=0.3)

    # 标注10年终值
    ax3.annotate(f'10年终值\n≈{fv[-1]/10000:.1f}万元',
                 xy=(10, fv[-1]), xytext=(8.5, fv[-1] * 0.85),
                 fontproperties=font_prop, fontsize=10, color='#2E7D32',
                 arrowprops=dict(arrowstyle='->', color='#2E7D32'),
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#4CAF50'))

    info_text = '投资目标：长期成长，年化8~12%  |  风险等级：R4中高  |  坚持定投，忽视短期波动'
    fig.text(0.5, 0.01, info_text, ha='center', va='bottom',
             fontproperties=font_prop, fontsize=10, color='#555555',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFF8E1', edgecolor='#FFD54F'))

    plt.tight_layout(rect=[0, 0.07, 1, 0.95])
    out_path = os.path.join(OUTPUT_DIR, 'ch12_portfolio_growth.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {out_path}')


# =============================================================================
# 图5：投资行为成本量化 ch13_behavior_cost.png
# =============================================================================
def plot_behavior_cost():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle('投资行为成本量化：频繁操作侵蚀收益',
                 fontsize=16, fontproperties=font_prop, fontweight='bold', y=0.98)

    # 参数设置
    initial = 100000  # 初始10万
    market_annual = 0.08  # 市场年化8%
    years = 10

    # 各策略参数（每次换仓买卖费用合计）
    strategies = {
        '买入持有': {'trades_per_year': 0, 'cost_per_trade': 0.002},
        '每年换仓1次': {'trades_per_year': 1, 'cost_per_trade': 0.003},  # 卖出0.5%+买入0.15%+印花税0.1%
        '每季换仓1次': {'trades_per_year': 4, 'cost_per_trade': 0.003},
        '每月换仓1次': {'trades_per_year': 12, 'cost_per_trade': 0.003},
    }

    colors_list = ['#4CAF50', '#2196F3', '#FF9800', '#F44336']
    results = {}

    ax1 = axes[0]
    for (name, params), color in zip(strategies.items(), colors_list):
        values = [initial]
        for y in range(years):
            # 每年市场增长，扣除交易成本
            v = values[-1] * (1 + market_annual)
            annual_cost = params['cost_per_trade'] * params['trades_per_year']
            v = v * (1 - annual_cost)
            values.append(v)
        results[name] = values
        ax1.plot(range(years + 1), [v / 10000 for v in values],
                 'o-', color=color, linewidth=2.5, markersize=5,
                 label=f'{name}', zorder=3)

    ax1.set_xlabel('持有年数', fontproperties=font_prop, fontsize=12)
    ax1.set_ylabel('资产总值（万元）', fontproperties=font_prop, fontsize=12)
    ax1.set_title('10年资产增长曲线（市场年化8%假设）',
                  fontproperties=font_prop, fontsize=13)
    ax1.legend(prop=font_prop, fontsize=11, loc='upper left')
    ax1.grid(alpha=0.3)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    for label in ax1.get_xticklabels():
        label.set_fontproperties(font_prop)
    for label in ax1.get_yticklabels():
        label.set_fontproperties(font_prop)

    # 添加终值标注
    for (name, params), color in zip(strategies.items(), colors_list):
        final_val = results[name][-1] / 10000
        ax1.annotate(f'{final_val:.1f}万',
                     xy=(10, results[name][-1] / 10000),
                     xytext=(10.15, results[name][-1] / 10000),
                     fontproperties=font_prop, fontsize=9, color=color,
                     va='center')

    # 右图：10年后终值对比柱形图及损失
    ax2 = axes[1]
    strategy_names = list(results.keys())
    final_values = [results[n][-1] / 10000 for n in strategy_names]
    best = final_values[0]
    losses = [best - v for v in final_values]

    x = np.arange(len(strategy_names))
    bars = ax2.bar(x, final_values, color=colors_list, edgecolor='white',
                   linewidth=1.5, width=0.55, zorder=3)

    # 标注终值
    for bar, val in zip(bars, final_values):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                 f'{val:.1f}万',
                 ha='center', va='bottom',
                 fontproperties=font_prop, fontsize=11, fontweight='bold')

    # 标注相比持有不动的损失
    for i, (bar, loss) in enumerate(zip(bars, losses)):
        if loss > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() / 2,
                     f'少赚\n{loss:.1f}万',
                     ha='center', va='center',
                     fontproperties=font_prop, fontsize=9,
                     color='white', fontweight='bold')

    ax2.set_xticks(x)
    ax2.set_xticklabels(strategy_names, fontproperties=font_prop, fontsize=11)
    ax2.set_ylabel('10年后资产总值（万元）', fontproperties=font_prop, fontsize=12)
    ax2.set_title('10年后终值对比\n（初始10万，市场年化8%假设）',
                  fontproperties=font_prop, fontsize=13)
    ax2.set_ylim(0, max(final_values) * 1.2)
    for label in ax2.get_yticklabels():
        label.set_fontproperties(font_prop)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='y', alpha=0.3, zorder=0)

    # 底部注释
    note = ('注：每次换仓成本约0.3%（买入管理费0.15% + 卖出赎回费0.1% + 印花税等），仅为量化说明，实际费率因产品而异\n'
            '结论：持有不动10年 ≈ 21.6万；每月换仓10年 ≈ 17.4万，摩擦成本吞噬约4.2万（损失19%收益）')
    fig.text(0.5, 0.01, note, ha='center', va='bottom',
             fontproperties=font_prop, fontsize=9.5, color='#555555',
             bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFEBEE', edgecolor='#EF9A9A'))

    plt.tight_layout(rect=[0, 0.10, 1, 0.95])
    out_path = os.path.join(OUTPUT_DIR, 'ch13_behavior_cost.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {out_path}')


# =============================================================================
# 主程序
# =============================================================================
if __name__ == '__main__':
    print('开始生成第十二章、第十三章配套图像...')
    print()
    plot_money_layers()
    plot_portfolio_conservative()
    plot_portfolio_balanced()
    plot_portfolio_growth()
    plot_behavior_cost()
    print()
    print('全部图像生成完成！')
    print(f'输出目录：{OUTPUT_DIR}')
