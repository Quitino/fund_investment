"""
第九章：技术分析入门 - 图表生成脚本
生成所有技术分析相关图表
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
import os

# 字体设置
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
matplotlib.rcParams['axes.unicode_minus'] = False

# 输出目录
OUT_DIR = '/mnt/data2/fund_investment/docs/pic'
os.makedirs(OUT_DIR, exist_ok=True)

# 配色方案
RED = '#E74C3C'
GREEN = '#27AE60'
BLUE = '#2980B9'
ORANGE = '#E67E22'
PURPLE = '#8E44AD'
GRAY = '#95A5A6'
DARK = '#2C3E50'
LIGHT_GRAY = '#ECF0F1'
YELLOW = '#F1C40F'

# ============================================================
# 图1：K线结构解析
# ============================================================
def plot_candlestick_anatomy():
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_facecolor('#F8F9FA')
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    # 标题
    ax.text(5, 9.5, 'K线结构解析', fontsize=18, fontweight='bold',
            ha='center', va='center', color=DARK, fontproperties=font_prop)

    # ---- 红K线（上涨）----
    # 参数
    r_x = 2.5          # 中心x
    r_open = 3.5       # 开盘价（y坐标）
    r_close = 6.0      # 收盘价
    r_high = 7.2       # 最高价
    r_low = 2.3        # 最低价
    body_w = 0.7

    # 上影线
    ax.plot([r_x, r_x], [r_close, r_high], color=RED, linewidth=2.5, zorder=3)
    # 下影线
    ax.plot([r_x, r_x], [r_low, r_open], color=RED, linewidth=2.5, zorder=3)
    # 实体（收盘>开盘，填红色）
    rect_r = mpatches.FancyBboxPatch(
        (r_x - body_w/2, r_open), body_w, r_close - r_open,
        boxstyle="square,pad=0", facecolor=RED, edgecolor=RED, linewidth=1.5, zorder=4)
    ax.add_patch(rect_r)

    # 标注
    ax.annotate('最高价\n' + f'（上影线顶端）',
                xy=(r_x, r_high), xytext=(0.1, 7.8),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('收盘价\n（实体顶端）',
                xy=(r_x + body_w/2, r_close), xytext=(0.1, 6.3),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('实体\n（涨幅大小）',
                xy=(r_x, (r_open + r_close)/2), xytext=(0.1, 4.7),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('开盘价\n（实体底端）',
                xy=(r_x + body_w/2, r_open), xytext=(0.1, 3.2),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('最低价\n（下影线底端）',
                xy=(r_x, r_low), xytext=(0.1, 1.8),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')

    ax.text(r_x, 0.8, '阳线（红K线）\n收盘价 > 开盘价', fontsize=11, fontweight='bold',
            ha='center', va='center', color=RED, fontproperties=font_prop)

    # 双向箭头标注实体高度
    ax.annotate('', xy=(r_x + body_w/2 + 0.3, r_close),
                xytext=(r_x + body_w/2 + 0.3, r_open),
                arrowprops=dict(arrowstyle='<->', color=RED, lw=1.5))
    ax.text(r_x + body_w/2 + 0.7, (r_open + r_close)/2,
            '实体\n长度', fontsize=8, ha='left', va='center',
            color=RED, fontproperties=font_prop)

    # ---- 绿K线（下跌）----
    g_x = 7.5
    g_open = 6.0       # 开盘价（高）
    g_close = 3.5      # 收盘价（低）
    g_high = 7.2
    g_low = 2.3

    # 上影线
    ax.plot([g_x, g_x], [g_open, g_high], color=GREEN, linewidth=2.5, zorder=3)
    # 下影线
    ax.plot([g_x, g_x], [g_close, g_low], color=GREEN, linewidth=2.5, zorder=3)
    # 实体（开盘>收盘，填绿色）
    rect_g = mpatches.FancyBboxPatch(
        (g_x - body_w/2, g_close), body_w, g_open - g_close,
        boxstyle="square,pad=0", facecolor=GREEN, edgecolor=GREEN, linewidth=1.5, zorder=4)
    ax.add_patch(rect_g)

    ax.annotate('最高价',
                xy=(g_x, g_high), xytext=(9.8, 7.8),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('开盘价\n（实体顶端）',
                xy=(g_x + body_w/2, g_open), xytext=(9.8, 6.3),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('实体',
                xy=(g_x, (g_open + g_close)/2), xytext=(9.8, 4.7),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('收盘价\n（实体底端）',
                xy=(g_x + body_w/2, g_close), xytext=(9.8, 3.2),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')
    ax.annotate('最低价',
                xy=(g_x, g_low), xytext=(9.8, 1.8),
                fontsize=9, color=DARK, fontproperties=font_prop,
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5),
                ha='center', va='center')

    ax.text(g_x, 0.8, '阴线（绿K线）\n收盘价 < 开盘价', fontsize=11, fontweight='bold',
            ha='center', va='center', color=GREEN, fontproperties=font_prop)

    # 分割线
    ax.axvline(x=5, color=GRAY, linestyle='--', alpha=0.5, linewidth=1)

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch9_candlestick_anatomy.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {path}')


# ============================================================
# 图2：常见K线形态
# ============================================================
def draw_candle(ax, x, open_y, close_y, high_y, low_y, body_w=0.35):
    """在ax上绘制一根K线"""
    is_up = close_y >= open_y
    color = RED if is_up else GREEN
    ax.plot([x, x], [min(open_y, close_y), low_y], color=color, linewidth=2, zorder=3)
    ax.plot([x, x], [max(open_y, close_y), high_y], color=color, linewidth=2, zorder=3)
    body_bottom = min(open_y, close_y)
    body_height = abs(close_y - open_y) if abs(close_y - open_y) > 0.01 else 0.02
    rect = mpatches.FancyBboxPatch(
        (x - body_w/2, body_bottom), body_w, body_height,
        boxstyle="square,pad=0", facecolor=color, edgecolor=color, linewidth=1.5, zorder=4)
    ax.add_patch(rect)


def plot_candlestick_patterns():
    fig, axes = plt.subplots(2, 3, figsize=(14, 10))
    fig.patch.set_facecolor('#FFFFFF')
    fig.suptitle('常见K线形态', fontsize=18, fontweight='bold',
                 color=DARK, fontproperties=font_prop, y=0.98)

    patterns = [
        {
            'name': '锤子线',
            'signal': '看涨反转',
            'desc': '下跌趋势末端出现\n长下影线、小实体\n预示底部反转',
            'candles': [
                # (x, open, close, high, low)
                (0.5, 5.0, 4.5, 5.2, 3.5),   # 下跌背景
                (1.5, 4.5, 4.0, 4.6, 2.8),
                (2.5, 4.1, 3.8, 4.2, 2.2),
                (3.5, 3.9, 4.1, 4.15, 2.3),  # 锤子线（关键）
            ],
            'highlight': 3,
            'color': RED,
        },
        {
            'name': '上吊线',
            'signal': '看跌反转',
            'desc': '上涨趋势末端出现\n长下影线、小实体\n预示顶部反转',
            'candles': [
                (0.5, 3.0, 3.5, 3.6, 2.9),
                (1.5, 3.5, 4.0, 4.1, 3.4),
                (2.5, 4.0, 4.6, 4.7, 3.9),
                (3.5, 4.7, 4.9, 5.0, 3.3),  # 上吊线
            ],
            'highlight': 3,
            'color': GREEN,
        },
        {
            'name': '看涨吞没',
            'signal': '看涨反转',
            'desc': '阴线后出现更大阳线\n阳线实体完全包裹阴线\n强力反转信号',
            'candles': [
                (0.5, 5.0, 4.5, 5.1, 4.4),
                (1.5, 4.6, 4.0, 4.7, 3.9),
                (2.5, 4.1, 3.6, 4.2, 3.5),
                (3.5, 3.4, 4.8, 4.85, 3.35),  # 吞没阳线
            ],
            'highlight': 3,
            'color': RED,
        },
        {
            'name': '看跌吞没',
            'signal': '看跌反转',
            'desc': '阳线后出现更大阴线\n阴线实体完全包裹阳线\n强力看跌信号',
            'candles': [
                (0.5, 3.0, 3.5, 3.6, 2.9),
                (1.5, 3.5, 4.1, 4.2, 3.4),
                (2.5, 4.0, 4.6, 4.7, 3.9),
                (3.5, 4.8, 3.4, 4.85, 3.35),  # 吞没阴线
            ],
            'highlight': 3,
            'color': GREEN,
        },
        {
            'name': '晨星',
            'signal': '看涨反转',
            'desc': '三K线组合：大阴线\n+小实体（星）+大阳线\n底部反转强力信号',
            'candles': [
                (0.5, 5.5, 5.0, 5.6, 4.9),
                (1.5, 5.0, 4.4, 5.1, 4.3),
                (2.5, 4.1, 3.9, 4.15, 3.85),  # 星（小实体）
                (3.5, 3.8, 5.2, 5.3, 3.75),   # 大阳线
            ],
            'highlight': [2, 3],
            'color': RED,
        },
        {
            'name': '暮星',
            'signal': '看跌反转',
            'desc': '三K线组合：大阳线\n+小实体（星）+大阴线\n顶部反转强力信号',
            'candles': [
                (0.5, 2.5, 2.9, 3.0, 2.4),
                (1.5, 2.9, 3.4, 3.5, 2.8),
                (2.5, 3.5, 3.7, 3.75, 3.45),  # 星
                (3.5, 3.8, 2.5, 3.85, 2.45),  # 大阴线
            ],
            'highlight': [2, 3],
            'color': GREEN,
        },
    ]

    for idx, (ax, pat) in enumerate(zip(axes.flat, patterns)):
        ax.set_facecolor('#F8F9FA')
        ax.set_xlim(0, 4.2)
        ax.set_ylim(1.5, 6.0)
        ax.axis('off')

        for i, (x, o, c, h, l) in enumerate(pat['candles']):
            draw_candle(ax, x, o, c, h, l)

        # 高亮关键K线
        highlights = pat['highlight'] if isinstance(pat['highlight'], list) else [pat['highlight']]
        for hi in highlights:
            hx = pat['candles'][hi][0]
            ax.axvspan(hx - 0.4, hx + 0.4, alpha=0.15, color=YELLOW)

        signal_color = RED if '看涨' in pat['signal'] else GREEN
        ax.set_title(f"{pat['name']}", fontsize=13, fontweight='bold',
                     color=DARK, fontproperties=font_prop, pad=8)
        ax.text(2.1, 1.8, f"信号：{pat['signal']}", fontsize=9, fontweight='bold',
                ha='center', va='center', color=signal_color, fontproperties=font_prop,
                bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_GRAY, edgecolor=signal_color, alpha=0.8))
        ax.text(2.1, 6.0, pat['desc'], fontsize=8,
                ha='center', va='top', color=DARK, fontproperties=font_prop,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    path = os.path.join(OUT_DIR, 'ch9_candlestick_patterns.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {path}')


# ============================================================
# 图3：均线系统
# ============================================================
def plot_moving_average():
    np.random.seed(42)
    n = 120
    # 生成一段有趋势的价格序列
    t = np.arange(n)
    price = 100 + 0.3 * t + 8 * np.sin(t / 15) + 6 * np.sin(t / 8) + np.cumsum(np.random.randn(n) * 0.5)
    price = price - price.min() + 80

    def ma(arr, w):
        result = np.full(len(arr), np.nan)
        for i in range(w-1, len(arr)):
            result[i] = arr[i-w+1:i+1].mean()
        return result

    ma5  = ma(price, 5)
    ma10 = ma(price, 10)
    ma20 = ma(price, 20)
    ma60 = ma(price, 60)

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#F8F9FA')

    ax.plot(t, price, color=DARK, linewidth=1.2, alpha=0.7, label='价格', zorder=2)
    ax.plot(t, ma5,  color='#E74C3C', linewidth=1.5, label='MA5',  alpha=0.9)
    ax.plot(t, ma10, color='#E67E22', linewidth=1.5, label='MA10', alpha=0.9)
    ax.plot(t, ma20, color='#27AE60', linewidth=2.0, label='MA20', alpha=0.9)
    ax.plot(t, ma60, color='#2980B9', linewidth=2.5, label='MA60', alpha=0.9)

    # 找金叉（MA5从下穿过MA20）
    golden_crosses = []
    death_crosses = []
    for i in range(1, len(ma5)):
        if np.isnan(ma5[i]) or np.isnan(ma20[i]):
            continue
        if ma5[i-1] < ma20[i-1] and ma5[i] >= ma20[i]:
            golden_crosses.append(i)
        elif ma5[i-1] > ma20[i-1] and ma5[i] <= ma20[i]:
            death_crosses.append(i)

    for gc in golden_crosses[:3]:
        ax.annotate('金叉', xy=(gc, ma5[gc]),
                    xytext=(gc - 8, ma5[gc] - 12),
                    fontsize=9, color=RED, fontweight='bold', fontproperties=font_prop,
                    arrowprops=dict(arrowstyle='->', color=RED, lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDECEA', edgecolor=RED, alpha=0.9))

    for dc in death_crosses[:3]:
        ax.annotate('死叉', xy=(dc, ma5[dc]),
                    xytext=(dc + 5, ma5[dc] + 12),
                    fontsize=9, color=GREEN, fontweight='bold', fontproperties=font_prop,
                    arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F8F0', edgecolor=GREEN, alpha=0.9))

    ax.set_title('均线系统：MA5 / MA10 / MA20 / MA60', fontsize=15, fontweight='bold',
                 color=DARK, fontproperties=font_prop, pad=12)
    ax.set_xlabel('交易日', fontsize=11, fontproperties=font_prop)
    ax.set_ylabel('价格（元）', fontsize=11, fontproperties=font_prop)
    ax.legend(loc='upper left', fontsize=10, prop=font_prop, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')

    # 说明文字框
    info_text = ('金叉：短期均线向上穿越长期均线，看涨信号\n'
                 '死叉：短期均线向下穿越长期均线，看跌信号\n'
                 'MA20/MA60常作为中长期支撑/压力参考位')
    ax.text(0.02, 0.02, info_text, transform=ax.transAxes, fontsize=8.5,
            va='bottom', ha='left', fontproperties=font_prop,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=GRAY, alpha=0.85))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch9_moving_average.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {path}')


# ============================================================
# 图4：量价关系
# ============================================================
def plot_volume_price():
    np.random.seed(7)
    n = 80
    t = np.arange(n)

    # 构造几个典型场景
    price = np.zeros(n)
    volume = np.zeros(n)

    # 段1（0-19）：量增价涨（健康上涨）
    price[:20] = 100 + np.cumsum(np.random.randn(20)*0.5 + 0.4)
    volume[:20] = 50 + np.arange(20)*1.5 + np.random.randn(20)*5

    # 段2（20-39）：量缩价涨（注意）
    price[20:40] = price[19] + np.cumsum(np.random.randn(20)*0.3 + 0.2)
    volume[20:40] = np.linspace(80, 30, 20) + np.random.randn(20)*4

    # 段3（40-59）：量增价跌（出货）
    price[40:60] = price[39] + np.cumsum(np.random.randn(20)*0.5 - 0.4)
    volume[40:60] = np.linspace(40, 100, 20) + np.random.randn(20)*6

    # 段4（60-79）：量缩价跌（筑底）
    price[60:80] = price[59] + np.cumsum(np.random.randn(20)*0.3 - 0.1)
    volume[60:80] = np.linspace(90, 30, 20) + np.random.randn(20)*3

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), gridspec_kw={'height_ratios': [3, 1.5]})
    fig.patch.set_facecolor('#FFFFFF')
    fig.suptitle('量价关系分析', fontsize=15, fontweight='bold',
                 color=DARK, fontproperties=font_prop, y=0.98)

    # 颜色分段
    seg_colors_price = [BLUE, '#27AE60', RED, ORANGE]
    seg_vol_colors = [BLUE, '#27AE60', RED, ORANGE]
    seg_labels = ['量增价涨\n（健康上涨）', '量缩价涨\n（注意）', '量增价跌\n（出货信号）', '量缩价跌\n（筑底阶段）']
    segs = [(0, 20), (20, 40), (40, 60), (60, 80)]

    # 价格折线
    ax1.set_facecolor('#F8F9FA')
    for (s, e), c in zip(segs, seg_colors_price):
        ax1.plot(t[s:e], price[s:e], color=c, linewidth=2.2, zorder=3)
    ax1.set_ylabel('价格（元）', fontsize=11, fontproperties=font_prop)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(labelbottom=False)

    # 标注场景标签
    for (s, e), label, c in zip(segs, seg_labels, seg_colors_price):
        mid = (s + e) // 2
        ax1.text(mid, ax1.get_ylim()[1] if ax1.get_ylim()[1] > 0 else price[mid]+5,
                 label, ha='center', va='bottom', fontsize=9, color=c,
                 fontproperties=font_prop,
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=c, alpha=0.85))

    # 分割线
    for s, e in segs[1:]:
        ax1.axvline(x=s, color=GRAY, linestyle=':', alpha=0.7)

    # 成交量柱状图
    ax2.set_facecolor('#F8F9FA')
    bar_colors = []
    for i in range(n):
        seg_idx = i // 20
        bar_colors.append(seg_vol_colors[seg_idx])
    ax2.bar(t, volume, color=bar_colors, alpha=0.7, width=0.8)
    ax2.set_ylabel('成交量', fontsize=11, fontproperties=font_prop)
    ax2.set_xlabel('交易日', fontsize=11, fontproperties=font_prop)
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    for s, e in segs[1:]:
        ax2.axvline(x=s, color=GRAY, linestyle=':', alpha=0.7)

    # 重新标注（让ax1的标签可见，先调整ylim）
    ax1.set_ylim(price.min() - 3, price.max() + 10)
    for (s, e), label, c in zip(segs, seg_labels, seg_colors_price):
        mid = (s + e) // 2
        ax1.text(mid, price.max() + 2, label, ha='center', va='bottom', fontsize=9, color=c,
                 fontproperties=font_prop,
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor=c, alpha=0.85))

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch9_volume_price.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {path}')


# ============================================================
# 图5：MACD指标
# ============================================================
def compute_ema(arr, period):
    k = 2.0 / (period + 1)
    ema = np.full(len(arr), np.nan)
    # 用前period个点的均值作为初始值
    ema[period-1] = arr[:period].mean()
    for i in range(period, len(arr)):
        ema[i] = arr[i] * k + ema[i-1] * (1 - k)
    return ema


def plot_macd():
    np.random.seed(123)
    n = 150
    t = np.arange(n)
    price = 100 + np.cumsum(np.random.randn(n) * 1.0 + 0.05)
    # 让价格有明显波动
    price += 10 * np.sin(t / 20) + 5 * np.sin(t / 10)
    price = np.maximum(price, 50)

    ema12 = compute_ema(price, 12)
    ema26 = compute_ema(price, 26)
    dif = ema12 - ema26
    dea = compute_ema(dif[~np.isnan(dif)], 9)
    # 对齐长度
    dif_full = dif.copy()
    dea_full = np.full(n, np.nan)
    start_idx = np.where(~np.isnan(dif))[0][0]
    dea_full[start_idx + 8:] = dea[8:]

    macd_hist = 2 * (dif_full - dea_full)

    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor('#FFFFFF')
    fig.suptitle('MACD 技术指标', fontsize=15, fontweight='bold',
                 color=DARK, fontproperties=font_prop, y=0.99)

    gs = gridspec.GridSpec(3, 1, height_ratios=[2.5, 1.5, 1.5], hspace=0.05)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2], sharex=ax1)

    for ax in [ax1, ax2, ax3]:
        ax.set_facecolor('#F8F9FA')
        ax.grid(True, alpha=0.3, linestyle='--')

    # 价格
    ax1.plot(t, price, color=DARK, linewidth=1.5, label='价格')
    ax1.set_ylabel('价格（元）', fontsize=10, fontproperties=font_prop)
    ax1.tick_params(labelbottom=False)

    # DIF / DEA
    ax2.plot(t, dif_full, color=RED, linewidth=1.5, label='DIF（快线）', zorder=3)
    ax2.plot(t, dea_full, color=BLUE, linewidth=1.5, label='DEA（慢线/信号线）', zorder=3)
    ax2.axhline(y=0, color=GRAY, linewidth=1, linestyle='--')
    ax2.set_ylabel('DIF/DEA', fontsize=10, fontproperties=font_prop)
    ax2.legend(loc='upper left', fontsize=8, prop=font_prop)
    ax2.tick_params(labelbottom=False)

    # MACD柱
    valid = ~np.isnan(macd_hist)
    colors_hist = [RED if v > 0 else GREEN for v in macd_hist[valid]]
    ax3.bar(t[valid], macd_hist[valid], color=colors_hist, alpha=0.8, width=1)
    ax3.axhline(y=0, color=GRAY, linewidth=1, linestyle='--')
    ax3.set_ylabel('MACD柱', fontsize=10, fontproperties=font_prop)
    ax3.set_xlabel('交易日', fontsize=10, fontproperties=font_prop)

    # 找金叉死叉
    valid_idx = np.where(~np.isnan(dif_full) & ~np.isnan(dea_full))[0]
    golden = []
    death = []
    for ii in range(1, len(valid_idx)):
        i = valid_idx[ii]
        j = valid_idx[ii-1]
        if dif_full[j] < dea_full[j] and dif_full[i] >= dea_full[i]:
            golden.append(i)
        elif dif_full[j] > dea_full[j] and dif_full[i] <= dea_full[i]:
            death.append(i)

    for gc in golden[:2]:
        ax2.annotate('金叉', xy=(gc, dif_full[gc]),
                     xytext=(gc + 5, dif_full[gc] + 3),
                     fontsize=8, color=RED, fontproperties=font_prop,
                     arrowprops=dict(arrowstyle='->', color=RED, lw=1),
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#FDECEA', edgecolor=RED, alpha=0.9))
        ax1.axvline(x=gc, color=RED, linestyle=':', alpha=0.6)

    for dc in death[:2]:
        ax2.annotate('死叉', xy=(dc, dif_full[dc]),
                     xytext=(dc + 5, dif_full[dc] - 3),
                     fontsize=8, color=GREEN, fontproperties=font_prop,
                     arrowprops=dict(arrowstyle='->', color=GREEN, lw=1),
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#E8F8F0', edgecolor=GREEN, alpha=0.9))
        ax1.axvline(x=dc, color=GREEN, linestyle=':', alpha=0.6)

    # 添加背离标注（找一个明显的顶背离区间）
    # 在后半段找价格新高但MACD不创新高
    mid = n // 2
    price_2nd_high = np.argmax(price[mid:]) + mid
    dif_at_2nd = dif_full[price_2nd_high]
    ax1.text(price_2nd_high, price[price_2nd_high] + 3,
             '顶背离参考位\n（价格新高,MACD未新高）',
             ha='center', fontsize=8, color=PURPLE, fontproperties=font_prop,
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#F3E5F5', edgecolor=PURPLE, alpha=0.9))

    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch9_macd.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {path}')


# ============================================================
# 图6：RSI + 布林带
# ============================================================
def compute_rsi(prices, period=14):
    rsi = np.full(len(prices), np.nan)
    deltas = np.diff(prices)
    for i in range(period, len(prices)):
        gains = deltas[i-period:i]
        avg_gain = np.mean(gains[gains > 0]) if len(gains[gains > 0]) > 0 else 0
        avg_loss = -np.mean(gains[gains < 0]) if len(gains[gains < 0]) > 0 else 0
        if avg_loss == 0:
            rsi[i] = 100
        else:
            rs = avg_gain / avg_loss
            rsi[i] = 100 - 100 / (1 + rs)
    return rsi


def plot_rsi_bollinger():
    np.random.seed(88)
    n = 100
    t = np.arange(n)
    # 构造有高低波动的价格
    price = 100 + 15 * np.sin(t / 12) + 5 * np.sin(t / 5) + np.cumsum(np.random.randn(n) * 0.3)

    # 布林带
    period_bb = 20
    ma20_bb = np.array([price[max(0,i-period_bb+1):i+1].mean() for i in range(n)])
    std20 = np.array([price[max(0,i-period_bb+1):i+1].std() for i in range(n)])
    upper = ma20_bb + 2 * std20
    lower = ma20_bb - 2 * std20

    # RSI
    rsi = compute_rsi(price, 14)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), gridspec_kw={'height_ratios': [3, 1.5]})
    fig.patch.set_facecolor('#FFFFFF')
    fig.suptitle('布林带（Bollinger Bands）+ RSI 指标', fontsize=15, fontweight='bold',
                 color=DARK, fontproperties=font_prop, y=0.99)

    ax1.set_facecolor('#F8F9FA')
    ax2.set_facecolor('#F8F9FA')

    # 布林带填充
    ax1.fill_between(t, lower, upper, alpha=0.15, color=BLUE, label='布林带通道')
    ax1.plot(t, upper, color=BLUE, linewidth=1.5, linestyle='--', label='上轨（+2σ）', alpha=0.8)
    ax1.plot(t, lower, color=BLUE, linewidth=1.5, linestyle='--', label='下轨（-2σ）', alpha=0.8)
    ax1.plot(t, ma20_bb, color=ORANGE, linewidth=1.5, linestyle='-', label='中轨（MA20）', alpha=0.9)
    ax1.plot(t, price, color=DARK, linewidth=1.8, label='价格', zorder=5)

    # 标注触及上下轨
    touch_upper = np.where(price >= upper - 1)[0]
    touch_lower = np.where(price <= lower + 1)[0]
    for i in touch_upper[:2]:
        ax1.annotate('触及上轨\n（可能超买）', xy=(i, price[i]),
                     xytext=(i + 4, price[i] + 5),
                     fontsize=8, color=RED, fontproperties=font_prop,
                     arrowprops=dict(arrowstyle='->', color=RED, lw=1.2),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDECEA', edgecolor=RED, alpha=0.9))
    for i in touch_lower[:2]:
        ax1.annotate('触及下轨\n（可能超卖）', xy=(i, price[i]),
                     xytext=(i + 4, price[i] - 8),
                     fontsize=8, color=GREEN, fontproperties=font_prop,
                     arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2),
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F8F0', edgecolor=GREEN, alpha=0.9))

    ax1.set_ylabel('价格（元）', fontsize=11, fontproperties=font_prop)
    ax1.legend(loc='upper left', fontsize=9, prop=font_prop, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.tick_params(labelbottom=False)

    # RSI
    ax2.plot(t, rsi, color=PURPLE, linewidth=1.8, label='RSI(14)')
    ax2.axhline(y=70, color=RED, linestyle='--', linewidth=1.5, alpha=0.8, label='超买线（70）')
    ax2.axhline(y=30, color=GREEN, linestyle='--', linewidth=1.5, alpha=0.8, label='超卖线（30）')
    ax2.axhline(y=50, color=GRAY, linestyle=':', linewidth=1, alpha=0.6)
    ax2.fill_between(t, 70, np.minimum(rsi, 100), where=rsi > 70,
                     alpha=0.2, color=RED, label='超买区')
    ax2.fill_between(t, np.maximum(rsi, 0), 30, where=rsi < 30,
                     alpha=0.2, color=GREEN, label='超卖区')

    ax2.text(98, 72, '超买区（>70）', ha='right', fontsize=9, color=RED,
             fontproperties=font_prop)
    ax2.text(98, 25, '超卖区（<30）', ha='right', fontsize=9, color=GREEN,
             fontproperties=font_prop)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel('RSI', fontsize=11, fontproperties=font_prop)
    ax2.set_xlabel('交易日', fontsize=11, fontproperties=font_prop)
    ax2.legend(loc='upper left', fontsize=8, prop=font_prop, framealpha=0.9)
    ax2.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    path = os.path.join(OUT_DIR, 'ch9_rsi_bollinger.png')
    plt.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'Saved: {path}')


# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    print('开始生成第九章图表...')
    plot_candlestick_anatomy()
    plot_candlestick_patterns()
    plot_moving_average()
    plot_volume_price()
    plot_macd()
    plot_rsi_bollinger()
    print('所有图表生成完毕！')
    print(f'图表保存在：{OUT_DIR}')
