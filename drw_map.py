# -*- coding: utf-8 -*-
"""
Created on 17/06/2019 15:15
Project    ACTM-GOSAT
@author:   Dmitry
    Draw GOSAT map for region
"""

import numpy as np
import numpy.ma as ma
import pandas as pd
import datetime
import math
from scipy import interpolate

import plt_map


# === main class
class DrwMap():

    # --- init
    def __init__(self, case, years):
        #
        # ========== path ==========
        self.mpt_m_dir = case.mpt_m_dir
        self.plt_dir = case.plt_dir + 'latlon/'

        # --- year and month
        self.years = years
        self.months = case.months

        # --- map grid
        self.map_grid = 10
        self.map_lats = np.arange(-90, 90, self.map_grid)
        self.map_lons = np.arange(0, 360, self.map_grid)
        self.map_nlat = len(self.map_lats)
        self.map_nlon = len(self.map_lons)

        self.var_lims_1d = [1.2e18, 1.4e18, 1.6e18, 1.8e18, 2.0e18, 2.2e18, 2.4e18, 2.6e18, 2.8e18]

        self.var_lims_2d = [1.2e18, 2.8e18, 0.2e18]

        # --- 2d map for Siberia
        self.map_lims = [50, 70.0, 75, 115.0, 10, 10]

        # --- cities
        self.cts_coor = [
            ['NSK', 55.1, 83.0],
            ['TMK', 56.5, 85.0],
            ['KEM', 55.4, 86.1],
            ['NKZ', 53.8, 87.1],
            ['BRN', 53.3, 83.8],
            ['BRT', 56.1, 101.6],
            ['IRK', 52.3, 104.3],
            ['KRS', 56.0, 92.9],
            ['TUR', 65.8, 88.0],
            ['NVY', 66.1, 76.7],
            ['ULU', 51.8, 107.6],
            ['NRL', 69.3, 88.2],
            # ['CHB', 55.2, 61.4],
            # ['EKT', 56.8, 60.6],
        ]


    # === map
    def map_co(self):

        # --- stat info init
        stat_inf = []

        # --- pd settings
        pd.set_option('expand_frame_repr', False)

        # --- loops for years and mons
        for yr in range(self.years[0], self.years[1], 1):
            for mn in range(0, len(self.months), 12):

                # --- loop dates
                sdate = datetime.datetime(yr, mn + 1, 1, 0, 0)
                cdate = str(sdate.strftime("%Y%m"))

                pkf = self.mpt_m_dir + 'MOPITT_xCO_' + cdate
                try:
                    mpt_r = pd.read_pickle(pkf)
                except IOError:
                    print("\t\tCould not read file:", pkf)
                    exit()

                # --- indexes for domain
                idy0 = (np.abs(self.map_lats - self.map_lims[0])).argmin() - 1
                idy1 = (np.abs(self.map_lats - self.map_lims[1])).argmin() + 1
                idx0 = (np.abs(self.map_lons - self.map_lims[2])).argmin() - 1
                idx1 = (np.abs(self.map_lons - self.map_lims[3])).argmin() + 1

                # --- domain limits on the grid
                print(f'\t\t\tDomain limit indexes {idy0}, {idy1}, {idx0}, {idx1}')
                print(f'\t\t\tDomain limit coordinates {self.map_lats[idy0]}, {self.map_lats[idy1]}, '
                      f'{self.map_lons[idx0]}, {self.map_lons[idx1]}')

                # --- gridded arrays
                grd_co = np.zeros((self.map_nlat, self.map_nlon), dtype=np.float)
                grd_co.fill(np.nan)

                # --- re-gridding
                for ix in range(idx0, idx1):
                    for iy in range(idy0, idy1):
                        min_lt = self.map_lats[iy] - self.map_grid/2.
                        max_lt = self.map_lats[iy] + self.map_grid/2.
                        min_ln = self.map_lons[ix] - self.map_grid/2.
                        max_ln = self.map_lons[ix] + self.map_grid/2.

                        # --- df over selected grid
                        df = mpt_r[(mpt_r['lat'] >= min_lt) & (mpt_r['lat'] <= max_lt) &
                                   (mpt_r['lon'] >= min_ln) & (mpt_r['lon'] <= max_ln)]
                        grd_co[iy, ix] = df.mean(axis=0).values[0]

                # --- grid plot
                grd = 1
                if grd:
                    var_lims = self.var_lims_2d
                    sites = self.cts_coor

                    # --- MOPITT
                    title = ''  # f'MOPITT CO'
                    plot_name = self.plt_dir + 'grd_MOPITT_xCO_Sib_' + cdate[:6] + '_' + str(self.map_grid)
                    print(f'\t\t\tMOPITT data min: {np.nanmin(grd_co):.2}, '
                          f'max: {np.nanmax(grd_co):.2}')
                    mask = 0
                    plt_map.plot_map_int(grd_co, mask, self.map_lats, self.map_lons, self.map_lims,
                                         var_lims, plot_name, title, sites)

                # --- scatter plot
                scr = 1
                if scr:
                    # --- grid
                    x, y = np.meshgrid(self.map_lons, self.map_lats)
                    lons = x.flatten()
                    lats = y.flatten()

                    var_lims = self.var_lims_1d
                    sites = self.cts_coor

                    # --- MOPITT
                    g_s_ch4 = np.array((grd_co).flatten())
                    title = ''  # f'MOPITT CO'
                    plot_name = self.plt_dir + 'scr_MOPITT_xCO_Sib_' + cdate[:6] + '_' + str(self.map_grid)
                    print(f'\t\t\tMOPITT data min: {np.nanmin(g_s_ch4):.2}, max {np.nanmax(g_s_ch4):.2}')
                    plt_map.plot_map_sc(g_s_ch4, lats, lons, self.map_lims,
                                        var_lims, plot_name, title, sites)
