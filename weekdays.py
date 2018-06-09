

import os
import sys
import datetime as dt
import numpy as np


g_weekdays = ('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')


def dmy2weekday(dmy):
    return dt.datetime.strptime(
        str(dmy, encoding='utf-8'),
        '%d-%m-%Y').date().weekday()


def read_data(filename):
    #此时weekdays是［０，１，２，．．．］这样的数组
    weekdays, closing_prices = np.loadtxt(
        filename, delimiter=',', usecols=(1, 6),
        unpack=True, converters={1: dmy2weekday})
    return weekdays, closing_prices


def calc_average_prices(weekdays, closing_prices):
    average_prices = np.zeros(5)
    # np.take(数组，下标)－－－－＞指定下标的数组
    for weekday in range(average_prices.size):
        average_prices[weekday] = np.take(
            closing_prices,
            np.where(weekdays == weekday)).mean()
    return average_prices


def main(argc, argv, envp):
    weekdays, closing_prices = read_data('aapl.csv')
    average_prices = calc_average_prices(
        weekdays, closing_prices)
    max_index = np.argmax(average_prices)
    min_index = np.argmin(average_prices)
    for weekday, average_price in enumerate(
            average_prices):
        print(g_weekdays[weekday], ':', average_price,
              '(max)' if (weekday == max_index) else
              '(min)' if (weekday == min_index) else '')
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
