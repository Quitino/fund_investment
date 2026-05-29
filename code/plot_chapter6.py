"""
第六章配套绘图代码
《基金投资理财入门教程》Chapter 6 Plots
生成图像保存到 docs/pic/ 目录
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ── 字体配置 ──────────────────────────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 输出目录 ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# 图1：基金经理投资风格雷达图
# ─────────────────────────────────────────────────────────────────────────────
def plot_manager_style():
    categories = ['年化收益率', '波动性', '换手率', '最大回撤', '持仓集中度']
    N = len(categories)

    # 成长型数据（归一化到0-10，收益/集中度高，波动/换手/回撤也较高）
    growth_values = [8.5, 7.5, 8.0, 6.5, 7.0]
    # 价值型数据（收益稳健，波动低，换手低，回撤控制好）
    value_values  = [6.5, 4.0, 3.5, 3.5, 5.5]

    # 闭合数据
    growth_values += growth_values[:1]
    value_values  += value_values[:1]

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    # 网格样式
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontproperties=font_prop)
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10'], fontsize=8, color='grey')
    ax.grid(color='#CCCCCC', linestyle='--', linewidth=0.8, alpha=0.7)

    # 绘制成长型
    ax.plot(angles, growth_values, 'o-', linewidth=2.2, color='#E63946', label='成长型基金经理')
    ax.fill(angles, growth_values, alpha=0.18, color='#E63946')

    # 绘制价值型
    ax.plot(angles, value_values, 's-', linewidth=2.2, color='#2176AE', label='价值型基金经理')
    ax.fill(angles, value_values, alpha=0.18, color='#2176AE')

    ax.set_title('基金经理投资风格对比雷达图\n（各维度满分10分）',
                 fontsize=14, fontproperties=font_prop,
                 pad=25, fontweight='bold', color='#333333')

    legend = ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15),
                       fontsize=11, prop=font_prop,
                       framealpha=0.85, edgecolor='#AAAAAA')

    # 注释说明
    fig.text(0.5, 0.02,
             '注：数值越高表示该维度特征越突出；波动性/换手率/最大回撤越高代表风险越大',
             ha='center', fontsize=9, color='#666666', fontproperties=font_prop)

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out_path = os.path.join(OUTPUT_DIR, 'ch6_manager_style.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  已保存: {out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图2：基金规模与收益散点图
# ─────────────────────────────────────────────────────────────────────────────
def plot_fund_size_effect():
    rng = np.random.default_rng(42)

    # 模拟数据：规模区间（亿元）
    # 微型（<5亿）：流动性差，收益方差大
    tiny_scale  = rng.uniform(0.5, 5, 30)
    tiny_ret    = rng.normal(8, 12, 30)

    # 小型（5-10亿）：略好
    small_scale = rng.uniform(5, 10, 25)
    small_ret   = rng.normal(12, 8, 25)

    # 最优区间（10-100亿）：最佳
    mid_scale   = rng.uniform(10, 100, 60)
    mid_ret     = rng.normal(16, 5, 60)

    # 大型（100-300亿）：规模压制
    large_scale = rng.uniform(100, 300, 35)
    large_ret   = rng.normal(10, 5, 35)

    # 超大型（>300亿）：明显衰减
    xlarge_scale = rng.uniform(300, 800, 20)
    xlarge_ret   = rng.normal(6, 4, 20)

    all_scale = np.concatenate([tiny_scale, small_scale, mid_scale, large_scale, xlarge_scale])
    all_ret   = np.concatenate([tiny_ret,   small_ret,   mid_ret,   large_ret,   xlarge_ret])
    colors_list = (
        ['#E63946'] * 30 +
        ['#F4A261'] * 25 +
        ['#2A9D8F'] * 60 +
        ['#457B9D'] * 35 +
        ['#8B7BB5'] * 20
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')

    ax.scatter(np.log10(all_scale), all_ret, c=colors_list,
               alpha=0.65, s=55, edgecolors='white', linewidths=0.5)

    # 最优区间底纹
    ax.axvspan(np.log10(10), np.log10(100), alpha=0.10,
               color='#2A9D8F', label='最优规模区间（10-100亿）')
    ax.axvline(np.log10(10),  color='#2A9D8F', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.axvline(np.log10(100), color='#2A9D8F', linestyle='--', linewidth=1.5, alpha=0.7)

    # 趋势注释
    ax.annotate('规模过小\n流动性差\n业绩波动大',
                xy=(np.log10(2), 22), fontsize=9, color='#E63946',
                fontproperties=font_prop, ha='center',
                bbox=dict(boxstyle='round,pad=0.3', fc='#FFF0EE', ec='#E63946', alpha=0.8))

    ax.annotate('最优区间\n收益稳健',
                xy=(np.log10(32), 25), fontsize=9, color='#2A9D8F',
                fontproperties=font_prop, ha='center',
                bbox=dict(boxstyle='round,pad=0.3', fc='#EEFAF8', ec='#2A9D8F', alpha=0.8))

    ax.annotate('规模过大\n操作受限\n收益衰减',
                xy=(np.log10(500), 18), fontsize=9, color='#8B7BB5',
                fontproperties=font_prop, ha='center',
                bbox=dict(boxstyle='round,pad=0.3', fc='#F3F0FA', ec='#8B7BB5', alpha=0.8))

    # 图例
    legend_elements = [
        mpatches.Patch(color='#E63946', label='微型 <5亿', alpha=0.75),
        mpatches.Patch(color='#F4A261', label='小型 5-10亿', alpha=0.75),
        mpatches.Patch(color='#2A9D8F', label='中型 10-100亿 ★最优', alpha=0.75),
        mpatches.Patch(color='#457B9D', label='大型 100-300亿', alpha=0.75),
        mpatches.Patch(color='#8B7BB5', label='超大型 >300亿', alpha=0.75),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
              prop=font_prop, framealpha=0.85, edgecolor='#AAAAAA')

    # 坐标轴
    ax.set_xlabel('基金规模（亿元，对数轴）', fontsize=12, fontproperties=font_prop, labelpad=8)
    ax.set_ylabel('近3年年化收益率（%）', fontsize=12, fontproperties=font_prop, labelpad=8)
    ax.set_title('基金规模与近3年年化收益率关系散点图', fontsize=14,
                 fontproperties=font_prop, fontweight='bold', pad=15, color='#333333')

    tick_vals = [0.5, 1, 5, 10, 50, 100, 300, 800]
    ax.set_xticks([np.log10(v) for v in tick_vals])
    ax.set_xticklabels([str(v) for v in tick_vals], fontsize=9)
    ax.set_ylim(-15, 35)
    ax.axhline(0, color='#AAAAAA', linewidth=0.8, linestyle=':')
    ax.grid(axis='y', color='#DDDDDD', linestyle='--', linewidth=0.7, alpha=0.7)

    fig.text(0.5, -0.02,
             '注：数据为模拟示意，仅用于说明规模效应规律，不代表真实基金数据',
             ha='center', fontsize=8.5, color='#888888', fontproperties=font_prop)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch6_fund_size_effect.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  已保存: {out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图3：选基SOP流程图
# ─────────────────────────────────────────────────────────────────────────────
def plot_selection_flow():
    fig, ax = plt.subplots(figsize=(9, 13))
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')

    # 标题
    ax.text(5, 13.3, '主动基金筛选 SOP 流程图',
            ha='center', va='center', fontsize=15, fontweight='bold',
            fontproperties=font_prop, color='#1A1A2E')

    # 步骤定义：(y_center, 标题, 副文字, 主色, 浅色)
    steps = [
        (12.0, '第一步：确定投资目标',
         '明确风险承受能力 / 收益预期 / 持有期限',
         '#1A1A2E', '#E8E8F0'),
        (10.5, '第二步：筛选基金类型',
         '偏股混合 / 股票型 / 灵活配置\n排除近1年成立或规模 <5亿 的基金',
         '#2176AE', '#E6F1FB'),
        (8.8,  '第三步：考察基金经理',
         '任职年限 ≥3年 / 在管同类产品 ≤3只\n最大回撤 <30% / 夏普比率 >1',
         '#2A9D8F', '#E6F5F3'),
        (7.1,  '第四步：分析历史业绩',
         '看完整牛熊周期（≥5年）表现\n年化收益跑赢基准 ≥3% / 避免冠军魔咒',
         '#457B9D', '#EBF2F8'),
        (5.4,  '第五步：解读重仓持仓',
         '行业集中度是否符合自己判断\n前十大重仓股持仓比 <60%',
         '#F4A261', '#FEF5EC'),
        (3.7,  '第六步：确认基金规模',
         '股票型建议 10-100亿\n规模超 200亿 则谨慎选择',
         '#E76F51', '#FDEEE9'),
        (2.0,  '第七步：最终决策',
         '综合评分 ≥4项达标 → 加入候选池\n设定止盈止损纪律后建仓',
         '#6A0572', '#F3E6F5'),
    ]

    box_h = 0.95
    box_w = 7.8
    x_left = (10 - box_w) / 2

    for y, title, desc, main_color, light_color in steps:
        # 主色左边条
        bar = FancyBboxPatch((x_left, y - box_h / 2), 0.35, box_h,
                             boxstyle='round,pad=0.02',
                             facecolor=main_color, edgecolor='none', zorder=3)
        ax.add_patch(bar)

        # 主体背景框
        body = FancyBboxPatch((x_left + 0.35, y - box_h / 2), box_w - 0.35, box_h,
                              boxstyle='round,pad=0.05',
                              facecolor=light_color, edgecolor=main_color,
                              linewidth=1.2, zorder=3)
        ax.add_patch(body)

        # 标题文字
        ax.text(x_left + 0.65, y + 0.17, title,
                fontsize=11, fontweight='bold', va='center',
                fontproperties=font_prop, color=main_color, zorder=4)

        # 描述文字
        ax.text(x_left + 0.65, y - 0.22, desc,
                fontsize=9, va='center', color='#444444',
                fontproperties=font_prop, zorder=4)

    # 绘制箭头（步骤之间）
    for i in range(len(steps) - 1):
        y_top = steps[i][0] - box_h / 2
        y_bot = steps[i + 1][0] + box_h / 2
        y_mid_top = y_top - 0.01
        y_mid_bot = y_bot + 0.01
        ax.annotate('',
                    xy=(5, y_mid_bot), xytext=(5, y_mid_top),
                    arrowprops=dict(arrowstyle='->', color='#888888',
                                   lw=1.8, mutation_scale=16),
                    zorder=2)

    # 底部说明
    ax.text(5, 0.8,
            '注：至少满足4项关键指标才纳入候选，最终结合市场环境做决策',
            ha='center', fontsize=9, color='#888888', fontproperties=font_prop)

    plt.tight_layout(rect=[0, 0.0, 1, 1])
    out_path = os.path.join(OUTPUT_DIR, 'ch6_selection_flow.png')
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  已保存: {out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('开始生成第六章图像...')
    print('[1/3] 基金经理投资风格雷达图')
    plot_manager_style()
    print('[2/3] 基金规模与收益散点图')
    plot_fund_size_effect()
    print('[3/3] 选基SOP流程图')
    plot_selection_flow()
    print('\n全部图像生成完毕，保存在:', OUTPUT_DIR)
