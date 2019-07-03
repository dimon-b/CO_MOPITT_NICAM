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
def plot_ts(pds_set, pds_dif, colors, labels, lims, fname):
    # --- Build Map ---
    plt.figure(figsize=(10, 7))
    plt.rc('font', family='serif')
    font_size = 12
    mpl.rcParams.update({'font.size': font_size})

    # --- panel 1
    axes = plt.gca()
    for j in range(0, len(pds_set)):
        df1 = pds_set[j]
        df1.plot(color=colors[j], ls='-', label=labels[j])

    plt.grid()
    plt.ylabel('xCO, $molec \cdot cm^{-2}$')
    plt.xlabel('')
    plt.ylim(lims[0])
    #axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    #axes.set_xlim(['20141231 00:00:00', '20151231 00:00:00'])
    plt.legend(loc="upper left", ncol=9, prop={'size': font_size - 3}, fancybox=True, shadow=True)

    # --- save
    a_saveplot.save_plot(fname, ext="png", close=True, verbose=False)
