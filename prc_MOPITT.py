# -*- coding: utf-8 -*-
"""
Created on 30/06/2019 22:03
Project    CO
@author:   Dmitry
    Compare CO data
"""
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ["PROJ_LIB"] = "/home/dmitry/anaconda3/share/proj/"  # epsg file should be
from mpl_toolkits.basemap import Basemap
import h5py
import calendar
import math

import a_checkdir
import a_saveplot
import plt_timser


# === main class
class ProcMopitt():

    # --- init
    def __init__(self, case, years):
        # --- path
        self.mpt_r_dir = case.mpt_r_dir
        self.mpt_m_dir = case.mpt_m_dir
        self.plt_dir = case.plt_dir

        # --- calendar
        self.years = years
        self.months = case.months

        # --- 2d map for Japan
        self.map_lims = [26, 46, 126, 146, 4, 4]
        # --- 2d map for Krasnoyarsk
        self.map_lims = [40, 70, 70, 110, 10, 10]
        # --- Krasnoyarsk locations
        self.krs_coor = [56, 92.5]
        # --- no Krasnoyarsk locations
        self.nrs_coor = [66, 92.5]

        # ---
        self.pnt_lim = 1


    # --- main processing
    def proc_df(self, ifplot=False, info=False):

        rsm_time = 'm'
        frames = []

        # --- years and month
        for yr in range(self.years[0], self.years[1], 1):
            for mn in range(0, len(self.months), 1):
                # --- loop dates
                sdate = datetime.datetime(yr, mn + 1, 1, 0, 0)
                cdate = str(sdate.strftime("%Y%m"))

                pkf = self.mpt_m_dir + 'MOPITT_CO_' + cdate
                try:
                    df = pd.read_pickle(pkf)
                except IOError:
                    print("\t\tCould not read file:", pkf)
                    exit()
                frames.append(df)

        df = pd.concat(frames)

        min_lt = self.krs_coor[0] - self.pnt_lim/2.
        max_lt = self.krs_coor[0] + self.pnt_lim/2.
        min_ln = self.krs_coor[1] - self.pnt_lim/2.
        max_ln = self.krs_coor[1] + self.pnt_lim/2.

        # --- cat regions
        df_kr = df[(df['lat'] >= min_lt) & (df['lat'] <= max_lt) &
                   (df['lon'] >= min_ln) & (df['lon'] <= max_ln)]
        df_kr = df_kr.resample(rsm_time).mean()
        pds_kr = pd.Series(df_kr['CO, ppm'].values, index=df_kr.index)

        min_lt = self.nrs_coor[0] - self.pnt_lim/2.
        max_lt = self.nrs_coor[0] + self.pnt_lim/2.
        min_ln = self.nrs_coor[1] - self.pnt_lim/2.
        max_ln = self.nrs_coor[1] + self.pnt_lim/2.

        # --- cat regions
        df_nk = df[(df['lat'] >= min_lt) & (df['lat'] <= max_lt) &
                   (df['lon'] >= min_ln) & (df['lon'] <= max_ln)]
        df_nk = df_nk.resample(rsm_time).mean()
        pds_nk = pd.Series(df_nk['CO, ppm'].values, index=df_nk.index)

        # --- dif
        pds_dif = pd.Series(df_kr['CO, ppm'].values - df_nk['CO, ppm'].values, index=df_nk.index)

        # --- plot
        f_name = self.plt_dir + 'CO_' + cdate
        plt_timser.plot_ts([pds_kr, pds_nk], pds_dif, ['r', 'k'], ['Krs', 'Not'], [], f_name)


    # --- main processing
    def proc_raw(self, ifplot=False, info=False):

        # --- datarange for 2 dates
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + datetime.timedelta(n)


        # --- years and month
        for yr in range(self.years[0], self.years[1], 1):
            for mn in range(1, len(self.months), 13):
                frames = []

                # --- loop dates
                dt_st = datetime.datetime(yr, mn + 1, 1, 0, 0)
                dt_en = dt_st + datetime.timedelta(days=calendar.monthrange(yr, mn + 1)[1])

                for single_date in daterange(dt_st, dt_en):

                    # --- dates
                    cdate = str(single_date.strftime("%Y%m%d"))
                    print(f'\tRead MOPITT for:', cdate)

                    fname = self.mpt_r_dir + cdate[:4] + '/' + 'MOP02J-' + cdate + '-L2V16.2.3.he5'

                    try:
                        h5_var, h5_lat, h5_lon = self.h5_read(fname)

                        # --- df
                        frames.append(self.make_1d_df(h5_var, h5_lat, h5_lon, single_date))

                        # --- if plot
                        if ifplot:
                            pname = self.plt_dir + 'MOPITT_' + cdate
                            self.plot_map(h5_var, h5_lat, h5_lon, pname, cdate)

                        # --- get file info
                        if info:
                            self.h5_info(fname)

                    except IOError:
                        print("\t\tCould not read file:", fname)

                df = pd.concat(frames)
                df.set_index('index', inplace=True)
                pkf = self.mpt_m_dir + 'MOPITT_CO_' + cdate[:-2]
                a_checkdir.check_dir(pkf)
                df.to_pickle(pkf)


    # === make df
    def make_1d_df(self, h5_var, h5_lat, h5_lon, single_date):

        # --- df, ch4 in ppm
        df = pd.DataFrame({'index': [single_date]*len(h5_var), 'CO, ppm': h5_var, 'lat': h5_lat, 'lon': h5_lon})
        print('\t\tdf len:', len(df.index))
        # print(df.head())

        return df

        # # --- to pickle
        # pkf = self.mid_dir + 'MOPITTS-df/' + 'mpt_co'
        # a_checkdir.check_dir(pkf)
        # df.to_pickle(pkf)
        # exit()


    # --- read h5 file
    def h5_read(self, fname):

        with h5py.File(fname, mode='r') as fh5:
            # --- get var
            name = '/HDFEOS/SWATHS/MOP02/Data Fields/RetrievedCOTotalColumn'
            h5_var = fh5[name][:, 0]

            # --- units attribute is an array of string.
            fillvalue = fh5[name].attrs['_FillValue']

            h5_var[h5_var == fillvalue] = np.nan

            # --- get the geolocation data
            h5_lat = fh5['/HDFEOS/SWATHS/MOP02/Geolocation Fields/Latitude'][:]
            h5_lon = fh5['/HDFEOS/SWATHS/MOP02/Geolocation Fields/Longitude'][:]

            return h5_var, h5_lat, h5_lon


    # === plot map
    def plot_map(self, var1d, lats, lons, pname, cdate, title=False):
        # --- Build Map ---
        fig = plt.figure()
        plt.rc('font', family='serif')
        my_cmap = plt.get_cmap('jet')
        font_size = 10

        # --- limits
        map_lims = self.map_lims

        # --- map labels ---
        mp = Basemap(llcrnrlat=map_lims[0], urcrnrlat=map_lims[1],
                     llcrnrlon=map_lims[2], urcrnrlon=map_lims[3], projection='cyl', resolution='l')
        mp.drawcoastlines(color='grey')
        mp.drawcountries(color='grey')
        mp.drawparallels(np.arange(-90, 91, map_lims[4]), labels=[True, False, True, False],
                         fontsize=font_size, color='grey')
        mp.drawmeridians(np.arange(0, 360, map_lims[5]), labels=[False, True, False, True],
                         fontsize=font_size, color='grey')

        sc = mp.scatter(lons, lats, c=var1d, s=10, cmap=my_cmap, edgecolors=None, linewidth=0)
        cb = mp.colorbar()

        # --- title
        if title:
            plt.title(title + ' for ' + cdate)

        # --- save to plot
        a_saveplot.save_plot(pname, ext="png", close=True, verbose=False)
        plt.show()


    # --- read file info
    def h5_info(self, fname):
        # --- check file structure
        def traverse_datasets(hdf_file):
            def h5py_dataset_iterator(g, prefix=''):
                for key in g.keys():
                    item = g[key]
                    path = f'{prefix}/{key}'
                    if isinstance(item, h5py.Dataset):  # test for dataset
                        yield (path, item)
                    elif isinstance(item, h5py.Group):  # test for group (go down)
                        yield from h5py_dataset_iterator(item, path)


            with h5py.File(hdf_file, 'r') as f:
                for path, _ in h5py_dataset_iterator(f):
                    yield path


        # --- open
        f = h5py.File(fname, 'r')

        # --- read structure
        for dset in traverse_datasets(fname):
            print('Path:', dset)
            print('Shape:', f[dset].shape)
            print('Data type:', f[dset].dtype)
