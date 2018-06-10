# 用多项式拟合２只股票价差随日期变化的函数，得到坐标轴上的点再拟合

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


def calc_diffs(bhp_closing_prices, vale_closing_prices):
    return bhp_closing_prices - vale_closing_prices


def fit_polys(fit_x, fit_y, fit_d, poly_x):
    fit_p = np.polyfit(fit_x, fit_y, fit_d)
    poly_y = np.polyval(fit_p, poly_x)
    return poly_y


def find_peeks(fit_x, fit_y, fit_d, min_x, max_x):
    # 求得拟合的函数fit_p
    fit_p = np.polyfit(fit_x, fit_y, fit_d)
    # fit_p求导
    der_p = np.polyder(fit_p)
    # 求到函数为０的根，数学格式为a+-bi
    roots = np.roots(der_p)
    # 取实数根的实部
    reals = roots[np.isreal(roots)].real
    peeks = [[min_x, np.polyval(fit_p, min_x)]]
    for real in reals:
        if min_x < real and real < max_x:
            peeks.append([real, np.polyval(fit_p, real)])
    peeks.append([max_x, np.polyval(fit_p, max_x)])
    peeks.sort()
    peeks = np.array(peeks)
    return peeks


def init_chart(first_day, last_day):
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Polynomial Fitting', fontsize=20)
    mp.xlabel('Trading Days From %s To %s' % (
        first_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y'),
        last_day.astype(md.datetime.datetime).strftime(
            '%d %b %Y')), fontsize=14)
    mp.ylabel('Price Difference (USD) Of BHP & VALE',
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


def draw_diffs(dates, diffs):
    dates = dates.astype(md.datetime.datetime)
    # 参数s表示方点不连接
    mp.plot(dates, diffs, 's', c='limegreen',
            label='Price Difference')


def draw_polys(dates, polys, degree):
    dates = dates.astype(md.datetime.datetime)
    mp.plot(dates, polys, 'o-', c='dodgerblue',
            linewidth=3, label='Polynomial (%d)' % degree)


def draw_peeks(peeks):
    dates, peeks = np.hsplit(peeks, 2)
    # find_peeks解得的根是浮点数，即dates是浮点数
    dates = dates.astype(int).astype('M8[D]').astype(
        md.datetime.datetime)
    # 参数＇＾＇表示三角点不连接
    mp.plot(dates, peeks, '^', c='orangered', label='Peek')
    # 借用写文字的注解函数把箭头画出来
    for i in range(1, dates.size):
        # lw:线宽，有线宽就需要边缘色ec
        mp.annotate(
            '', xytext=(dates[i - 1], peeks[i - 1]),
            xy=(dates[i], peeks[i]), size=30,
            arrowprops=dict(
                arrowstyle='fancy',
                connectionstyle='arc3',
                fc='orangered',
                ec='none',
                lw=0))
    mp.gcf().autofmt_xdate()
    mp.legend()


def show_chart():
    mng = mp.get_current_fig_manager()
    if 'Windows' in platform.system():
        mng.window.state('zoomed')
    else:
        mng.resize(*mng.window.maxsize())
    mp.show()


def main(argc, argv, envp):
    dates, bhp_closing_prices = read_data('BHP.csv')
    dates, vale_closing_prices = read_data('VALE.csv')
    diffs = calc_diffs(bhp_closing_prices,
                       vale_closing_prices)
    # 将日期转换成想对于计算机元年的天数
    days = dates.astype(int)
    degree = 5
    polys = fit_polys(days, diffs, degree, days)
    peeks = find_peeks(days, diffs, degree,
                       days[0], days[-1])
    init_chart(dates[0], dates[-1])
    draw_diffs(dates, diffs)
    draw_polys(dates, polys, degree)
    draw_peeks(peeks)
    show_chart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
