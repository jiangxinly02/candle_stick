# 平均真实波幅（波动率指标）
import os
import sys
import numpy as np


def read_data(filename):
    dates, highest_prices, lowest_prices, \
        closing_prices = np.loadtxt(
            filename, delimiter=',', usecols=(1, 4, 5, 6),
            unpack=True, dtype=np.dtype('U10, f8, f8, f8'))
    return dates, highest_prices, lowest_prices, \
        closing_prices


def true_range(highest_prices, lowest_prices,
               closing_prices):
    hc = highest_prices - closing_prices
    cl = closing_prices - lowest_prices
    hl = highest_prices - lowest_prices
    tr = np.maximum(np.maximum(hc, cl), hl)
    return tr


def average_true_range(tr):
    atr = np.zeros(tr.size)
    for i in range(atr.size):
        atr[i] = tr.mean() if i == 0 else (
            atr[i - 1] * (tr.size - 1) + tr[i]) / tr.size
    return atr


def show_atr(dates, atr):
    for i, date in enumerate(dates[1:]):
        print(date, atr[i])


def main(argc, argv, envp):
    dates, highest_prices, lowest_prices, \
        closing_prices = read_data('aapl.csv')
    N = 20
    dates = dates[-N - 1:]
    highest_prices = highest_prices[-N:]
    lowest_prices = lowest_prices[-N:]
    closing_prices = closing_prices[-N - 1:-1]
    tr = true_range(highest_prices, lowest_prices,
                    closing_prices)
    atr = average_true_range(tr)
    show_atr(dates, atr)
    return 0

if __name__ == '__main__':
    sys.exit(main(len(sys.argv), sys.argv, os.environ))
