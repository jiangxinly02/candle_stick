import os
import sys
import platform
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as mp
import matplotlib.dates as md


def dmy2ymd(dmy):
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


def calc_pivots(highest_prices, lowest_prices,
                closing_prices):
    '''计算基准位pivots'''
    pivots = (highest_prices + lowest_prices +
              closing_prices) / 3
    spreads = highest_prices - lowest_prices
    supports = pivots - spreads
    resistances = pivots + spreads
    return pivots, supports, resistances


def fit_line(fit_x, fit_y, line_x):
    # 类型都是１维度和fit_x一样　
    ones = np.ones_like(fit_x)
    a = np.vstack([fit_x, ones]).T
    b = fit_y
    x = np.linalg.lstsq(a, b)[0]
    k, b = x[0], x[1]
    line_y = k * line_x + b
    return line_y


def init_chart(first_day, last_day):
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Trend Line', fontsize=20)
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


def draw_candlestick(
        dates, opening_prices, highest_prices,
        lowest_prices, closing_prices):
    dates = dates.astype(md.datetime.datetime)
    up = closing_prices - opening_prices >= 1e-2
    down = opening_prices - closing_prices >= 1e-2
    fc = np.zeros(dates.size, dtype='3f4')
    ec = np.zeros(dates.size, dtype='3f4')
    fc[up], fc[down] = (1, 1, 1), (0.85, 0.85, 0.85)
    ec[up], ec[down] = (0.85, 0.85, 0.85), (0.85, 0.85, 0.85)
    mp.bar(dates, highest_prices - lowest_prices, 0,
           lowest_prices, align='center', color=fc,
           edgecolor=ec)
    mp.bar(dates, closing_prices - opening_prices, 0.8,
           opening_prices, align='center', color=fc,
           edgecolor=ec)
    mp.gcf().autofmt_xdate()


def draw_pivots(dates, pivots, supports, resistances):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(dates, pivots, 's', c='dodgerblue',
            label='Pivot')
    mp.plot(dates, supports, 's', c='limegreen',
            label='Support')
    mp.plot(dates, resistances, 's', c='orangered',
            label='Resistance')


def draw_trend_line(dates, predays, trend_line):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(
        dates[:-predays], trend_line[:-predays],
        'o-', c='dodgerblue', linewidth=3,
        label='Trend Line')
    mp.plot(
        dates[-predays - 1:], trend_line[-predays - 1:],
        'o:', c='dodgerblue', linewidth=3)


def draw_support_line(dates, predays, support_line):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(
        dates[:-predays], support_line[:-predays],
        'o-', c='limegreen', linewidth=3,
        label='Support Line')
    mp.plot(
        dates[-predays - 1:], support_line[-predays - 1:],
        'o:', c='limegreen', linewidth=3)


def draw_resistance_line(dates, predays, resistance_line):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(
        dates[:-predays], resistance_line[:-predays],
        'o-', c='orangered', linewidth=3,
        label='Resistance Line')
    mp.plot(
        dates[-predays - 1:], resistance_line[-predays - 1:],
        'o:', c='orangered', linewidth=3)


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
    pivots, supports, resistances = calc_pivots(
        highest_prices, lowest_prices, closing_prices)
    predays = 5
    for i in range(predays):
        dates = np.append(dates, np.datetime64(
            (pd.to_datetime(str(dates[-1])).date() +
             pd.tseries.offsets.BDay()).strftime('%Y-%m-%d'),
            'D'))
    days = dates.astype(int)
    trend_line = fit_line(
        days[:-predays], pivots, days)
    support_line = fit_line(
        days[:-predays], supports, days)
    resistance_line = fit_line(
        days[:-predays], resistances, days)
    init_chart(dates[0], dates[-1])
    draw_candlestick(
        dates[:-predays], opening_prices, highest_prices,
        lowest_prices, closing_prices)
    draw_pivots(dates[:-predays], pivots, supports, resistances)
    draw_trend_line(dates, predays, trend_line)
    draw_support_line(dates, predays, support_line)
    draw_resistance_line(dates, predays, resistance_line)
    show_chart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
