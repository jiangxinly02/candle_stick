# 示例读取csv文件，画Ｋ线图，难点：numpy无法读取＇日－月－年＇格
# 式的日期，所以需要进行一系列的转换　　在定义draw_**()中，
# 需要把日期转换成matplotlib能够识别的md.datetime.datetime格式


import os
import sys
import platform
# python在linux和windows全屏显示图例的方法不一样，所以需要导入platform
import datetime as dt
import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md


def dmy2ymd(dmy):
	# 将'日－月－年'格式的日期转换为numpy能够识别的'年-月-日'
	# 如果在linux系统下则默认'utf-8'格式
    return dt.datetime.strptime(
        str(dmy, encoding='utf-8'),
        '%d-%m-%Y').date().strftime('%Y-%m-%d')


def read_data(filename):
    dates, opening_prices, highest_prices, \
        lowest_prices, closing_prices = np.loadtxt(
            filename, delimiter=',',
            usecols=(1, 3, 4, 5, 6), unpack=True,
            dtype=np.dtype('M8[D], f8, f8, f8, f8'),
            converters={1: dmy2ymd})
    return dates, opening_prices, highest_prices, \
        lowest_prices, closing_prices


def init_chart(first_day, last_day):
	# 设置背景色
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Candlestick Chart', fontsize=20)
    # 将first_day修改为md认识的时间格式，然后指定字符串格式为dby
    mp.xlabel('Trading Days From %s To %s' % (
        first_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y'),
        last_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y')), fontsize=14)
    mp.ylabel('Stock Price (USD) Of Apple Inc.',
              fontsize=14)
    # 获得xy轴
    ax = mp.gca()
    # 设置星期一为x轴主刻度
    ax.xaxis.set_major_locator(
        md.WeekdayLocator(byweekday=md.MO))
    # 设置日期为次定位器
    ax.xaxis.set_minor_locator(md.DayLocator())
    # 设置以什么样的格式来显示这些刻度
    ax.xaxis.set_major_formatter(
        md.DateFormatter('%d %b %Y'))
    # 以下代码基本初始化通用
    mp.tick_params(which='both', top=True, right=True,
                   labelright=True, labelsize=10)
    mp.grid(linestyle=':')


def draw_chart(dates, opening_prices, highest_prices,
               lowest_prices, closing_prices):
	# 转换日期格式为mp可以识别的格式
    dates = dates.astype(md.datetime.datetime)
    # 1e-2表示一美分
    up = closing_prices - opening_prices >= 1e-2
    down = opening_prices - closing_prices >= 1e-2
    # fc为填充色，ec为边缘色，'3f4'为３个float4字节组成的元素
    fc = np.zeros(dates.size, dtype='3f4')
    ec = np.zeros(dates.size, dtype='3f4')
    fc[up], fc[down] = (1, 1, 1), (0, 0.5, 0)
    ec[up], ec[down] = (1, 0, 0), (0, 0.5, 0)
    # mp.bar参数说明（对应ｘ每个刻度为坐标，宽度取绝对值，长度，
    # 底部，对其方式，填充色，边缘色）
    mp.bar(dates, highest_prices - lowest_prices, 0,
           lowest_prices, align='center', color=fc,
           edgecolor=ec)
    mp.bar(dates, closing_prices - opening_prices, 0.8,
           opening_prices, align='center', color=fc,
           edgecolor=ec)
    # 主刻度label斜体显示
    mp.gcf().autofmt_xdate()


def show_chart():
    mng = mp.get_current_fig_manager()
    if 'Windows' in platform.system():
        mng.window.state('zoomed')
    else:
        mng.resize(*mng.window.maxsize())
    mp.show()


def main(argc, argv, envp):
    dates, opening_prices, highest_prices, \
        lowest_prices, closing_prices = read_data(
            'aapl.csv')
    init_chart(dates[0], dates[-1])
    draw_chart(dates, opening_prices, highest_prices,
               lowest_prices, closing_prices)
    show_chart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
