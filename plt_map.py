#!/usr/bin/env python
"""
Created on 19/02/07 03:10
Project    Analysis
@author:   Dmitry
    Plot map data
"""

import matplotlib.pyplot as plt
import os

os.environ["PROJ_LIB"] = "C:\\Users\\admin\Anaconda3\envs\\v-env\Library\share"  # epsg file should be
from mpl_toolkits.basemap import Basemap
import numpy as np
import a_saveplot


# --- plot region map
def plot_map(var2d, lats, lons, map_lims, plot_name, title, cbar_lims, map_marks):
    # --- Build Map ---
    fig = plt.figure()
    plt.rc('font', family='serif')
    my_cmap = plt.get_cmap('rainbow')
    font_size = 10

    # --- map labels ---
    mp = Basemap(projection='gall', llcrnrlat=map_lims[0], urcrnrlat=map_lims[1],
                 llcrnrlon=map_lims[2], urcrnrlon=map_lims[3], resolution='l')
    mp.drawcoastlines(color='k')
    mp.drawcountries(color='k')
    mp.drawparallels(np.arange(-90, 91, map_lims[4]), labels=[True, False, True, False], fontsize=font_size,
                     color='grey')
    mp.drawmeridians(np.arange(0, 360, map_lims[5]), labels=[False, True, False, True], fontsize=font_size,
                     color='grey')

    # --- color bar min/max
    if cbar_lims == []:
        # --- min-max
        minn = np.nanmin(var2d)
        maxx = np.nanmax(var2d)
        print('Map min/max', minn, maxx)
        var2d[var2d > maxx] = maxx
        vp = np.linspace(minn, maxx, 100, endpoint=True)
        vc = np.linspace(minn, maxx, 11, endpoint=True)
    else:
        vp = np.linspace(cbar_lims[0], cbar_lims[1], 100, endpoint=True)
        vc = np.arange(cbar_lims[0], cbar_lims[1]*1.001, cbar_lims[2])

    # --- map plot
    x, y = np.meshgrid(lons, lats)
    x, y = mp(x, y)
    # print(var2d.shape)
    # print(x.shape)
    # print(y.shape)

    sc1 = mp.contourf(x, y, var2d, vp, cmap=my_cmap)
    fig.autofmt_xdate()

    # --- plot grid marks
    if map_marks != []:
        put_marks(mp, map_marks)

    # --- cbar
    axcbar = fig.add_axes([0.15, 0.19, 0.7, 0.03])
    cbar = fig.colorbar(sc1, orientation='horizontal', ticks=vc, cax=axcbar)
    cbar.ax.tick_params(labelsize=font_size)
    cbar.update_ticks()

    # --- title
    plt.suptitle(title, y=0.85, fontsize=font_size)

    # --- save to plot
    a_saveplot.save_plot(plot_name, ext="png", close=True, verbose=False)
    plt.show()


# --- plot region map with data interpolation
def plot_map_int(var2d, mask, lats, lons, map_lims, cbar_lims, plot_name, title, map_marks):
    # --- Build Map ---
    fig = plt.figure()
    plt.rc('font', family='serif')
    my_cmap = plt.get_cmap('jet')
    font_size = 12

    # --- map labels ---
    mp = Basemap(projection='cyl', llcrnrlat=map_lims[0], urcrnrlat=map_lims[1],
                 llcrnrlon=map_lims[2], urcrnrlon=map_lims[3], resolution='l')
    mp.drawcoastlines(color='grey')
    mp.drawcountries(color='grey')
    mp.drawparallels(np.arange(-90, 91, map_lims[4]), labels=[True, False, True, False], fontsize=font_size,
                     color='grey')
    mp.drawmeridians(np.arange(0, 360, map_lims[5]), labels=[False, True, False, True], fontsize=font_size,
                     color='grey')

    # --- color bar min/max
    if cbar_lims == []:
        # --- min-max
        minn = np.nanmin(var2d)
        maxx = np.nanmax(var2d)
        print('Map min/max', minn, maxx)
        var2d[var2d > maxx] = maxx
        vp = np.linspace(minn, maxx, 100, endpoint=True)
        vc = np.linspace(minn, maxx, 11, endpoint=True)
    else:
        vp = np.linspace(cbar_lims[0], cbar_lims[1], 100, endpoint=True)
        vc = np.arange(cbar_lims[0], cbar_lims[1]*1.001, cbar_lims[2])

    # --- map plot
    x, y = np.meshgrid(lons, lats)
    x, y = mp(x, y)
    # print(var2d.shape)
    # print(x.shape)
    # print(y.shape)
    import scipy.interpolate as interpolate
    vals = ~np.isnan(var2d)
    f = interpolate.Rbf(x[vals], y[vals], var2d[vals], function='cubic')
    interpolated = f(x, y) + mask

    interpolated[interpolated < cbar_lims[0]] = cbar_lims[0]
    interpolated[interpolated > cbar_lims[1]] = cbar_lims[1]

    sc1 = mp.contourf(x, y, interpolated, vp, cmap=my_cmap)

    # --- title
    if title:
        plt.suptitle(title, y=1.05, fontsize=font_size)

    # --- plot grid marks
    if map_marks != []:
        put_marks(mp, map_marks, font_size)

    # --- cbar
    axcbar = fig.add_axes([0.125, 0.14, 0.775, 0.03])
    cbar = fig.colorbar(sc1, orientation='horizontal', ticks=vc, cax=axcbar)
    cbar.ax.tick_params(labelsize=font_size)
    cbar.update_ticks()

    # --- save to plot
    a_saveplot.save_plot(plot_name, ext="png", close=True, verbose=False)
    plt.show()


# === plot scatter map
def plot_map_sc(var1d, lats, lons, map_lims, var_lims, plot_name, title, map_marks):
    # --- Build Map ---
    fig = plt.figure()
    plt.rc('font', family='serif')
    my_cmap = plt.get_cmap('jet')
    font_size = 12

    # --- map labels ---
    mp = Basemap(projection='cyl', llcrnrlat=map_lims[0], urcrnrlat=map_lims[1],
                 llcrnrlon=map_lims[2], urcrnrlon=map_lims[3], resolution='l')
    mp.drawcoastlines(color='grey')
    mp.drawcountries(color='grey')
    mp.drawparallels(np.arange(-90, 91, map_lims[4]), labels=[True, False, True, False],
                     fontsize=font_size, color='grey')
    mp.drawmeridians(np.arange(0, 360, map_lims[5]), labels=[False, True, False, True],
                     fontsize=font_size, color='grey')

    x, y = mp(lons, lats)
    sc2 = mp.scatter(x, y, c=var1d, s=13, marker='s', cmap=my_cmap)

    plt.clim(var_lims[0], var_lims[-1])

    # --- title
    if title:
        plt.title(title, y=1.05, fontsize=font_size)

    # --- plot grid marks
    if map_marks != []:
        put_marks(mp, map_marks, font_size)

    # --- cbar
    axcbar = fig.add_axes([0.125, 0.14, 0.775, 0.03])
    cbar = fig.colorbar(sc2, orientation='horizontal', ticks=var_lims, cax=axcbar)
    cbar.ax.tick_params(labelsize=font_size)
    cbar.update_ticks()

    # --- save to plot
    a_saveplot.save_plot(plot_name, ext="png", close=True, verbose=False)
    plt.show()


# --- map marks
def put_marks(mp, map_marks, font_size):
    for j in range(0, len(map_marks), 1):
        msite = map_marks[j][0]
        mlat = map_marks[j][1]
        mlon = map_marks[j][2]
        slat = map_marks[j][1] - 0.25
        slon = map_marks[j][2] + 0.25

        x, y = mp(mlon, mlat)
        mp.plot(x, y, 'o', color='magenta', markersize=4)
        x, y = mp(slon, slat)
        plt.text(x, y, msite, color='k', weight='bold', fontsize=font_size - 4)
