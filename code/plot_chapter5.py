"""
第五章配套绘图代码
《基金投资理财入门教程》Chapter 5 Plots
生成图像保存到 docs/pic/ 目录
"""

import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from matplotlib.lines import Line2D

# ── 字体配置 ──────────────────────────────────────────────────────────────────
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 输出目录 ──────────────────────────────────────────────────────────────────
OUTPUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# 图1：沪深300 PE历史走势（模拟数据）
# ─────────────────────────────────────────────────────────────────────────────
def plot_pe_history():
    np.random.seed(42)

    # 生成 2010-01 到 2023-12 的月度时间轴（共168个月）
    n = 168
    years = np.linspace(2010, 2024, n)

    # 构建模拟PE走势（均值~13，范围8~22，模拟真实市场周期）
    # 使用多个正弦叠加 + 随机扰动
    t = np.linspace(0, 4 * np.pi, n)
    pe_base = 13.0
    pe = (pe_base
          + 5.0 * np.sin(t * 0.6 + 0.5)          # 主周期
          + 2.5 * np.sin(t * 1.5 + 1.2)           # 次周期
          + 1.2 * np.random.randn(n))              # 随机扰动

    # 手动植入几个历史事件特征
    # 2015年牛市顶峰（约第60个月，即2015年中）
    idx_2015_peak = 62
    pe[idx_2015_peak - 3:idx_2015_peak + 3] += np.array([3, 5, 7, 6, 4, 2])

    # 2018年底熊市低谷
    idx_2018_low = 107
    pe[idx_2018_low - 2:idx_2018_low + 3] -= np.array([2, 3, 4, 2, 1])

    # 2020-2021年科技牛
    idx_2021 = 132
    pe[idx_2021 - 4:idx_2021 + 4] += np.array([1, 2, 3, 4, 3, 2, 1, 0])

    # 限制范围在合理区间
    pe = np.clip(pe, 7.5, 24)

    mean_pe = pe.mean()
    std_pe = pe.std()
    upper1 = mean_pe + std_pe
    lower1 = mean_pe - std_pe

    fig, ax = plt.subplots(figsize=(12, 6))

    # 标准差区间填充
    ax.fill_between(years, lower1, upper1,
                    alpha=0.15, color='#3498db', label=f'均值 ± 1 标准差')

    # PE折线
    ax.plot(years, pe, color='#2c3e50', linewidth=1.8, label='沪深300 PE（TTM）', zorder=4)

    # 均值线
    ax.axhline(y=mean_pe, color='#3498db', linewidth=1.5,
               linestyle='--', label=f'历史均值 PE = {mean_pe:.1f}x', zorder=3)

    # +1/-1标准差
    ax.axhline(y=upper1, color='#e74c3c', linewidth=1.2,
               linestyle=':', alpha=0.8, label=f'+1σ = {upper1:.1f}x（偏高）')
    ax.axhline(y=lower1, color='#27ae60', linewidth=1.2,
               linestyle=':', alpha=0.8, label=f'-1σ = {lower1:.1f}x（偏低）')

    # 标注高低点
    peak_idx = np.argmax(pe)
    low_idx = np.argmin(pe)

    ax.annotate(
        f'高点 {pe[peak_idx]:.1f}x\n（约2015年牛市）',
        xy=(years[peak_idx], pe[peak_idx]),
        xytext=(years[peak_idx] - 1.5, pe[peak_idx] + 1.5),
        fontproperties=font_prop, fontsize=9, color='#e74c3c',
        arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.3),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffeaea', alpha=0.8),
    )
    ax.annotate(
        f'低点 {pe[low_idx]:.1f}x\n（约2018年底）',
        xy=(years[low_idx], pe[low_idx]),
        xytext=(years[low_idx] + 0.5, pe[low_idx] - 2.0),
        fontproperties=font_prop, fontsize=9, color='#27ae60',
        arrowprops=dict(arrowstyle='->', color='#27ae60', lw=1.3),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#eafff0', alpha=0.8),
    )

    # 区域着色：PE > +1σ 为高估区，PE < -1σ 为低估区
    ax.fill_between(years, pe, upper1,
                    where=(pe > upper1),
                    alpha=0.20, color='#e74c3c', label='高估区间')
    ax.fill_between(years, lower1, pe,
                    where=(pe < lower1),
                    alpha=0.20, color='#27ae60', label='低估区间')

    ax.set_xlabel('年份', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('市盈率 PE（倍）', fontproperties=font_prop, fontsize=13)
    ax.set_title('沪深300 市盈率（PE）历史走势（2010-2023，模拟示意）',
                 fontproperties=font_prop, fontsize=14, fontweight='bold')
    ax.set_xlim(2010, 2024)
    ax.set_ylim(4, 28)
    x_ticks = list(range(2010, 2024))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(y) for y in x_ticks],
                       fontproperties=font_prop, rotation=45, fontsize=9)
    ax.legend(prop=font_prop, fontsize=9.5, loc='upper right', ncol=2)
    ax.grid(True, alpha=0.3)

    ax.text(0.01, 0.02,
            '注：数据为教学演示用模拟数据，不代表真实历史行情，不构成投资建议',
            transform=ax.transAxes,
            fontproperties=font_prop, fontsize=8, color='gray',
            verticalalignment='bottom')

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch5_index_pe_history.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图2：主要指数累计收益对比
# ─────────────────────────────────────────────────────────────────────────────
def plot_index_comparison():
    np.random.seed(7)

    n = 168  # 168个月，2010-2023
    years = np.linspace(2010, 2024, n)

    def simulate_index(annual_return, annual_vol, seed_offset=0):
        """模拟月度收益率，生成累计净值"""
        np.random.seed(42 + seed_offset)
        monthly_return = annual_return / 12
        monthly_vol = annual_vol / np.sqrt(12)
        returns = np.random.normal(monthly_return, monthly_vol, n)
        # 叠加市场周期共同因子
        t = np.linspace(0, 3 * np.pi, n)
        market_factor = 0.008 * np.sin(t + seed_offset * 0.3)
        returns += market_factor
        nav = 100 * np.cumprod(1 + returns)
        return nav

    # 各指数参数：(年化收益, 年化波动, 偏移)
    hs300  = simulate_index(0.09,  0.22, seed_offset=0)   # 沪深300
    zz500  = simulate_index(0.11,  0.28, seed_offset=1)   # 中证500
    cyb    = simulate_index(0.13,  0.38, seed_offset=2)   # 创业板指
    sp500  = simulate_index(0.125, 0.17, seed_offset=3)   # 标普500

    # 2015年牛熊市特征加强
    bull_start, bull_end = 55, 65
    bear_start, bear_end = 65, 80
    for idx_arr, scale in [(hs300, 1.0), (zz500, 1.3), (cyb, 1.8)]:
        idx_arr[bull_start:bull_end] *= np.linspace(1.0, 1.5 * scale, bull_end - bull_start)
        # 均值化处理，使前后连贯
        idx_arr[bull_end:] *= idx_arr[bull_end - 1] / idx_arr[bull_end] if idx_arr[bull_end] != 0 else 1

    fig, ax = plt.subplots(figsize=(13, 7))

    colors = ['#e74c3c', '#3498db', '#9b59b6', '#27ae60']
    labels = ['沪深300', '中证500', '创业板指', '标普500（美元）']
    indices = [hs300, zz500, cyb, sp500]
    linestyles = ['-', '--', '-.', ':']

    for nav, color, label, ls in zip(indices, colors, labels, linestyles):
        ax.plot(years, nav, color=color, linewidth=2.2,
                label=label, linestyle=ls, zorder=4)
        # 标注终值
        end_val = nav[-1]
        ax.annotate(
            f'{end_val:.0f}',
            xy=(years[-1], end_val),
            xytext=(years[-1] + 0.1, end_val),
            fontproperties=font_prop, fontsize=9, color=color,
            va='center',
        )

    ax.axhline(y=100, color='gray', linewidth=1, linestyle=':', alpha=0.6)
    ax.text(2010.1, 102, '基准 = 100（2010年初）',
            fontproperties=font_prop, fontsize=9, color='gray')

    # 标注2015年牛市和2018年熊市
    ax.axvspan(2014.5, 2015.6, alpha=0.08, color='#e74c3c')
    ax.text(2014.55, 20, '2015\n牛市',
            fontproperties=font_prop, fontsize=8.5, color='#c0392b', alpha=0.8)
    ax.axvspan(2018.0, 2018.9, alpha=0.06, color='#2c3e50')
    ax.text(2018.05, 20, '2018\n调整',
            fontproperties=font_prop, fontsize=8.5, color='#2c3e50', alpha=0.8)

    ax.set_xlabel('年份', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('累计净值（基准=100）', fontproperties=font_prop, fontsize=13)
    ax.set_title('主要指数累计收益对比（2010-2023，模拟示意）',
                 fontproperties=font_prop, fontsize=14, fontweight='bold')
    ax.set_xlim(2010, 2024.5)
    ax.set_ylim(0, None)
    x_ticks = list(range(2010, 2024))
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([str(y) for y in x_ticks],
                       fontproperties=font_prop, rotation=45, fontsize=9)
    ax.legend(prop=font_prop, fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)

    ax.text(0.01, 0.02,
            '注：数据为教学演示用模拟数据，不代表真实历史行情，不构成投资建议',
            transform=ax.transAxes,
            fontproperties=font_prop, fontsize=8, color='gray',
            verticalalignment='bottom')

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch5_index_comparison.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图3：主动基金 vs 指数基金胜率（柱状图）
# ─────────────────────────────────────────────────────────────────────────────
def plot_active_vs_passive():
    periods = ['1年', '3年', '5年', '10年']
    # 主动基金跑赢指数的比例（合理模拟数据）
    active_win_rate = [42, 35, 25, 15]
    passive_win_rate = [100 - r for r in active_win_rate]

    x = np.arange(len(periods))
    width = 0.42

    fig, ax = plt.subplots(figsize=(10, 6.5))

    bars1 = ax.bar(x - width / 2, active_win_rate,
                   width, label='主动基金跑赢指数',
                   color='#e67e22', alpha=0.88, edgecolor='white', linewidth=1.2)
    bars2 = ax.bar(x + width / 2, passive_win_rate,
                   width, label='指数基金占优',
                   color='#3498db', alpha=0.88, edgecolor='white', linewidth=1.2)

    # 在柱子上方标注数值
    for bar in bars1:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.8,
                f'{h}%', ha='center', va='bottom',
                fontproperties=font_prop, fontsize=11.5, fontweight='bold',
                color='#d35400')
    for bar in bars2:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.8,
                f'{h}%', ha='center', va='bottom',
                fontproperties=font_prop, fontsize=11.5, fontweight='bold',
                color='#2471a3')

    # 50%基准线
    ax.axhline(y=50, color='gray', linewidth=1.2,
               linestyle='--', alpha=0.6, label='50% 基准线')
    ax.text(3.58, 51.5, '各半', fontproperties=font_prop,
            fontsize=9, color='gray')

    ax.set_xlabel('持有期限', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('比例（%）', fontproperties=font_prop, fontsize=13)
    ax.set_title('不同持有期：主动基金跑赢指数的比例（模拟示意）',
                 fontproperties=font_prop, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontproperties=font_prop, fontsize=13)
    ax.set_ylim(0, 110)
    ax.set_yticks(range(0, 101, 10))
    ax.set_yticklabels([f'{v}%' for v in range(0, 101, 10)],
                       fontproperties=font_prop, fontsize=10)
    ax.legend(prop=font_prop, fontsize=11, loc='upper right')
    ax.grid(True, alpha=0.25, axis='y')

    # 趋势说明文字
    ax.annotate(
        '持有期越长\n指数基金胜率越高',
        xy=(3, passive_win_rate[3]),
        xytext=(2.1, 95),
        fontproperties=font_prop, fontsize=10, color='#2471a3',
        arrowprops=dict(arrowstyle='->', color='#2471a3', lw=1.3),
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#eaf4fb', alpha=0.9),
    )

    ax.text(0.01, 0.02,
            '参考来源：S&P SPIVA报告、中国基金业协会数据（教学演示，非精确统计）',
            transform=ax.transAxes,
            fontproperties=font_prop, fontsize=8, color='gray',
            verticalalignment='bottom')

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch5_active_vs_passive.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 图4：PE/PB估值象限图（散点图）
# ─────────────────────────────────────────────────────────────────────────────
def plot_pe_pb_quadrant():
    # (名称, PE, PB, 颜色)  —— 模拟数据，代表某时点的估值水平
    indices = [
        ('沪深300',    12.5, 1.3,  '#e74c3c'),
        ('中证500',    22.0, 2.0,  '#3498db'),
        ('创业板指',   38.0, 4.5,  '#9b59b6'),
        ('上证50',     10.0, 1.1,  '#27ae60'),
        ('中证红利',    8.5, 0.85, '#f39c12'),
        ('中证1000',   30.0, 3.2,  '#1abc9c'),
        ('纳斯达克100', 32.0, 7.5,  '#e67e22'),
        ('标普500',    22.5, 4.2,  '#2c3e50'),
        ('恒生指数',    9.5, 1.0,  '#c0392b'),
    ]

    fig, ax = plt.subplots(figsize=(11, 8))

    # 绘制象限分割线
    pe_mid = 18.0
    pb_mid = 2.2
    ax.axvline(x=pe_mid, color='gray', linewidth=1.2,
               linestyle='--', alpha=0.6, zorder=1)
    ax.axhline(y=pb_mid, color='gray', linewidth=1.2,
               linestyle='--', alpha=0.6, zorder=1)

    # 象限背景色
    pe_min, pe_max = 5, 48
    pb_min, pb_max = 0.4, 9.5

    # 低PE低PB = 低估（绿色）
    ax.fill_between([pe_min, pe_mid], pb_min, pb_mid,
                    alpha=0.07, color='#27ae60')
    # 高PE高PB = 高估（红色）
    ax.fill_between([pe_mid, pe_max], pb_mid, pb_max,
                    alpha=0.07, color='#e74c3c')
    # 低PE高PB = 特殊（黄色）
    ax.fill_between([pe_min, pe_mid], pb_mid, pb_max,
                    alpha=0.05, color='#f39c12')
    # 高PE低PB = 混合（蓝色）
    ax.fill_between([pe_mid, pe_max], pb_min, pb_mid,
                    alpha=0.05, color='#3498db')

    # 象限标签
    ax.text(pe_min + 0.5, pb_max - 0.4, '低PE高PB\n（特殊情况）',
            fontproperties=font_prop, fontsize=9, color='#b7770d', alpha=0.8,
            va='top')
    ax.text(pe_mid + 0.5, pb_max - 0.4, '高PE高PB\n高估区',
            fontproperties=font_prop, fontsize=9.5, color='#c0392b', alpha=0.9,
            va='top', fontweight='bold')
    ax.text(pe_min + 0.5, pb_min + 0.05, '低PE低PB\n低估区',
            fontproperties=font_prop, fontsize=9.5, color='#1e8449', alpha=0.9,
            va='bottom', fontweight='bold')
    ax.text(pe_mid + 0.5, pb_min + 0.05, '高PE低PB\n（成长/价值分歧）',
            fontproperties=font_prop, fontsize=9, color='#21618c', alpha=0.8,
            va='bottom')

    # 绘制散点
    for name, pe, pb, color in indices:
        ax.scatter(pe, pb, s=260, color=color, zorder=5,
                   edgecolors='white', linewidths=1.8)
        # 智能偏移避免重叠
        x_off, y_off = 0.4, 0.12
        if name == '纳斯达克100':
            y_off = -0.3
        elif name == '恒生指数':
            x_off = -3.5
            y_off = 0.12
        elif name == '上证50':
            x_off = 0.4
            y_off = -0.28
        elif name == '中证红利':
            y_off = 0.15
        ax.text(pe + x_off, pb + y_off, name,
                fontproperties=font_prop, fontsize=10.5,
                color=color, fontweight='bold')

    # 分割线标注
    ax.text(pe_mid + 0.2, pb_min + 0.05,
            f'PE = {pe_mid}x（分割线）',
            fontproperties=font_prop, fontsize=8.5, color='gray',
            rotation=90, va='bottom')
    ax.text(pe_min + 0.2, pb_mid + 0.05,
            f'PB = {pb_mid}x（分割线）',
            fontproperties=font_prop, fontsize=8.5, color='gray',
            va='bottom')

    ax.set_xlabel('市盈率 PE（倍）——越低越便宜', fontproperties=font_prop, fontsize=13)
    ax.set_ylabel('市净率 PB（倍）——越低越便宜', fontproperties=font_prop, fontsize=13)
    ax.set_title('主要指数 PE / PB 估值象限图（模拟示意某时点数据）',
                 fontproperties=font_prop, fontsize=14, fontweight='bold')
    ax.set_xlim(pe_min, pe_max)
    ax.set_ylim(pb_min, pb_max)
    ax.grid(True, alpha=0.25)

    ax.text(0.01, 0.02,
            '注：数据为教学演示用模拟数据，不代表真实行情，分割线仅供参考，不构成投资建议',
            transform=ax.transAxes,
            fontproperties=font_prop, fontsize=8, color='gray',
            verticalalignment='bottom')

    fig.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'ch5_pe_pb_quadrant.png')
    fig.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'已生成：{out_path}')


# ─────────────────────────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('开始生成第五章配图...')
    plot_pe_history()
    plot_index_comparison()
    plot_active_vs_passive()
    plot_pe_pb_quadrant()
    print('全部图像生成完毕。')
