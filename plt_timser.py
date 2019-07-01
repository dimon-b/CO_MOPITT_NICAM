#!/usr/bin/env python
"""
Created on 19/05/28 12:20
Project    ACTM-GOSAT
@author:   Dmitry
    Plot time series of dataset
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import a_saveplot
import matplotlib.dates as mdates


# === plot time series
def plot_ts(df_set, colors, labels, lims, fname):
    # --- Build Map ---
    fig = plt.figure(figsize=(10, 7))
    plt.rc('font', family='serif')
    font_size = 12
    mpl.rcParams.update({'font.size': font_size})

    # --- panel 1
    plt.subplot(211)
    axes = plt.gca()
    df1 = df_set[0]
    df2 = df_set[1]

    # --- remove nan
    x = df1.values
    y = df2.values
    print(df1.head())
    df1.plot(color=colors[0], ls='-', label=labels[0])
    df2.plot(color=colors[1], ls='--', label=labels[1])

    plt.grid()
    plt.ylabel('CO$, ppm')
    plt.xlabel('')
    plt.ylim(lims[0])
    #axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    #axes.set_xlim(['20101231 00:00:00', '20140115 00:00:00'])
    #fig.autofmt_xdate()
    plt.legend(loc="upper left", ncol=5, prop={'size': font_size - 3}, fancybox=True, shadow=True)

    # # --- panel 2
    # plt.subplot(212)
    # axes = plt.gca()
    # #for j in range(0, len(df_pl)):
    # df = df_pl[j]
    # std = float(np.nanstd(df.values))
    # std = ' (' + str(round(std, 2)) + ')'
    # #std = ''
    # df.plot(color=colors[j], ls='-', label=labels[j] + std)
    #
    # plt.grid()
    # plt.ylabel('$\Delta$CO$, ppm')
    # plt.xlabel('')
    # plt.ylim(lims[1])
    # #axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    # #axes.set_xlim(['20101231 00:00:00', '20140115 00:00:00'])
    # #fig.autofmt_xdate()
    # plt.legend(loc="upper left", ncol=5, prop={'size': font_size - 3}, fancybox=True, shadow=True)

    # --- save
    a_saveplot.save_plot(fname, ext="png", close=True, verbose=False)
    plt.show()