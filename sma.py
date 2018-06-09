# 简单移动均线

import os
import sys
import platform
import datetime as dt
import numpy as np
import matplotlib.pyplot as mp
import matplotlib.dates as md


def dmy2ymd(dmy):
    return dt.datetime.strptime(
        str(dmy, encoding='utf-8'),
        '%d-%m-%Y').date().strftime('%Y-%m-%d')


def read_data(filename):
    dates, closing_prices = np.loadtxt(
        filename, delimiter=',', usecols=(1, 6),
        unpack=True, dtype=np.dtype('M8[D], f8'),
        converters={1: dmy2ymd})
    return dates, closing_prices


def calc_sma(N, closing_prices):
    '''
    计算简单移动均线方法２：
    weights = np.ones(N)
    weights /= weights.sum()
    sma = np.convolve(closing_prices, weights, 'valid')
    '''
    sma = np.zeros(closing_prices.size - (N - 1))
    for i in range(sma.size):
        sma[i] = closing_prices[i:i + N].mean()
    return sma


def init_chart(first_day, last_day):
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Simple Movine Average', fontsize=20)
    mp.xlabel('Trading Days From %s To %s' % (
        first_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y'),
        last_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y')), fontsize=14)
    mp.ylabel('Stock Price (USD) Of Apple Inc.',
              fontsize=14)
    ax = mp.gca()
    ax.xaxis.set_major_locator(
        md.WeekdayLocator(byweekday=md.MO))
    ax.xaxis.set_minor_locator(md.DayLocator())
    ax.xaxis.set_major_formatter(
        md.DateFormatter('%d %b %Y'))

    mp.tick_params(which='both', top=True, right=True,
                   labelright=True, labelsize=10)
    mp.grid(linestyle=':')


def draw_closing_prices(dates, closing_prices):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(dates, closing_prices, 'o-', c='lightgray',
            label='Closing Price')


def draw_sma(N, dates, sma):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(dates, sma, label='SMA-%d' % N)
    # 刻度值斜体显示
    mp.gcf().autofmt_xdate()
    
    # 显示图例　右上角说明，可以改变说明的位置
    mp.legend()


def show_chart():
    mng = mp.get_current_fig_manager()
    if 'Windows' in platform.system():
        mng.window.state('zoomed')
    else:
        mng.resize(*mng.window.maxsize())
    mp.show()


def main(argc, argv, envp):
    dates, closing_prices = read_data('aapl.csv')
    init_chart(dates[0], dates[-1])
    draw_closing_prices(dates, closing_prices)
    N = 5
    sma = calc_sma(N, closing_prices)
    draw_sma(N, dates[N - 1:], sma)
    N = 10
    sma = calc_sma(N, closing_prices)
    draw_sma(N, dates[N - 1:], sma)
    N = 15
    sma = calc_sma(N, closing_prices)
    draw_sma(N, dates[N - 1:], sma)
    show_chart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
