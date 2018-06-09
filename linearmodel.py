

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
    dates, closing_prices = np.loadtxt(
        filename, delimiter=',', usecols=(1, 6),
        unpack=True, dtype=np.dtype('M8[D], f8'),
        converters={1: dmy2ymd})
    return dates, closing_prices


def predict_prices(N, closing_prices):
    # 需要２Ｎ个数预测一个数
    predicted_prices = np.zeros(
        closing_prices.size - N * 2 + 1)
    #构建a b矩阵算出系数矩阵x
    for i in range(predicted_prices.size):
        a = np.zeros((N, N))
        for j in range(a.shape[0]):
            a[j, ] = closing_prices[i + j:i + j + N]
        b = closing_prices[i + N:i + N * 2]
#       除了x还有残差　置信
        x, _, _, _ = np.linalg.lstsq(a, b)
        predicted_prices[i] = b.dot(x)
    return predicted_prices


def init_chart(first_day, last_day):
    mp.gcf().set_facecolor(np.ones(3) * 240 / 255)
    mp.title('Stock Price Prediction', fontsize=20)
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


def draw_predicted_prices(N, dates, predicted_prices):
    # pd.to_datetime()把（）内的变成pd时间序列
    #pd.tseries.offsets.BDay(几天):
    # pd.时间序列.偏移量．交易日　
    # np.append(a,b):把b添加到a
    #np.datetime64(a,'D')把a转换为M8日期到天的格式 
    dates = np.append(dates, np.datetime64(
        (pd.to_datetime(str(dates[-1])).date() +
         pd.tseries.offsets.BDay()).strftime('%Y-%m-%d'),
        'D'))

    dates = dates[N * 2:].astype(md.datetime.datetime)

    mp.plot(dates[:-1], predicted_prices[:-1], 'o-',
            c='orangered', linewidth=3,
            label='Predicted Price')
    mp.plot(dates[-2:], predicted_prices[-2:], 'o--',
            c='orangered', linewidth=3)

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
    dates, closing_prices = read_data('aapl.csv')
    N = 5
    predicted_prices = predict_prices(N, closing_prices)
    init_chart(dates[0], dates[-1])
    draw_closing_prices(dates, closing_prices)
    draw_predicted_prices(N, dates, predicted_prices)
    show_chart()
    return 0


if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
