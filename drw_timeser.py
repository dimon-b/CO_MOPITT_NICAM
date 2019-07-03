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

import a_setcolors
import plt_timser


# === main class
class DrwTmser():

    # --- init
    def __init__(self, case, years):
        # --- path
        self.mpt_m_dir = case.mpt_m_dir
        self.plt_dir = case.plt_dir

        # --- calendar
        self.years = years
        self.months = case.months

        # --- Krasnoyarsk locations
        self.krs_coor = [56, 92.5]
        # --- no Krasnoyarsk locations
        self.nkr_coor = [50, 92.5]
        self.nkr_coor = [60, 95.0]

        # ---
        self.krs_lim = 2
        self.nkr_lim = 5

        # --- cities
        self.cts_coor = [
            ['NSK', 55.1, 83.0],
            ['TMK', 56.5, 85.0],
            ['KEM', 55.4, 86.1],
            ['NKZ', 53.8, 87.1],
            ['LSB', 58.2, 92.5],
            ['BRK', 56.1, 101.6],
            ['IRK', 52.3, 104.3],
            ['KRS', 56.0, 92.9]
            # ['CHB', 55.2, 61.4],
            # ['EKT', 56.8, 60.6],
            # ['BRN', 53.3, 83.8],
        ]
        self.cts_lim = 1


    # --- processing for cities
    def proc_cts(self):

        rsm_time = 'm'

        frames = []
        index = []
        for i in range(len(self.cts_coor)):
            frames.append([])

        # --- years and month
        for yr in range(self.years[0], self.years[1], 1):
            for mn in range(0, len(self.months), 1):
                # --- loop dates
                sdate = datetime.datetime(yr, mn + 1, 1, 0, 0)
                cdate = str(sdate.strftime("%Y%m"))

                pkf = self.mpt_m_dir + 'MOPITT_xCO_' + cdate
                print(f'\tRead MOPITT df file:', pkf)
                try:
                    df = pd.read_pickle(pkf)

                    # --- city
                    set_cts = []
                    for st in range(0, len(self.cts_coor)):
                        min_lt = self.cts_coor[st][1] - self.cts_lim/2.
                        max_lt = self.cts_coor[st][1] + self.cts_lim/2.
                        min_ln = self.cts_coor[st][2] - self.cts_lim/2.
                        max_ln = self.cts_coor[st][2] + self.cts_lim/2.

                        # --- cat regions
                        df_ct = df[(df['lat'] >= min_lt) & (df['lat'] <= max_lt) &
                                   (df['lon'] >= min_ln) & (df['lon'] <= max_ln)]
                        df_ct = df_ct.resample(rsm_time).mean()

                        try:
                            frames[st].append(df_ct['xCO'].values[0])
                        except:
                            frames[st].append(np.nan)

                    index.append(df_ct.index[0])

                except IOError:
                    print("\t\tCould not read file:", pkf)

        # --- labels
        labels = []
        set_cts = []
        for st in range(0, len(self.cts_coor)):
            labels.append(self.cts_coor[st][0])
            pd_ct = pd.Series(frames[st], index=index)
            #print(pd_ct)
            set_cts.append(pd_ct)

        # --- colors
        colors = a_setcolors.set_colors(len(self.cts_coor), 'jet')
        set_dif = set_cts

        # --- plot
        f_name = self.plt_dir + 'xCO_cites_' + str(self.cts_lim) + 'grad'
        plt_lims = [[1.6e18, 3.2e18], []]
        plt_timser.plot_ts(set_cts, set_dif, colors, labels, plt_lims, f_name)


    # --- processing df for regions
    def proc_df(self):

        rsm_time = '15d'
        frames = []

        # --- years and month
        for yr in range(self.years[0], self.years[1], 1):
            for mn in range(0, len(self.months), 1):
                # --- loop dates
                sdate = datetime.datetime(yr, mn + 1, 1, 0, 0)
                cdate = str(sdate.strftime("%Y%m"))

                pkf = self.mpt_m_dir + 'MOPITT_xCO_' + cdate
                try:
                    df = pd.read_pickle(pkf)
                except IOError:
                    print("\t\tCould not read file:", pkf)
                    exit()
                frames.append(df)

        df = pd.concat(frames)

        min_lt = self.krs_coor[0] - self.krs_lim/2.
        max_lt = self.krs_coor[0] + self.krs_lim/2.
        min_ln = self.krs_coor[1] - self.krs_lim/2.
        max_ln = self.krs_coor[1] + self.krs_lim/2.

        # --- cat regions
        df_kr = df[(df['lat'] >= min_lt) & (df['lat'] <= max_lt) &
                   (df['lon'] >= min_ln) & (df['lon'] <= max_ln)]
        df_kr = df_kr.resample(rsm_time).mean()
        pds_kr = pd.Series(df_kr['xCO'].values, index=df_kr.index)

        min_lt = self.nkr_coor[0] - self.nkr_lim/2.
        max_lt = self.nkr_coor[0] + self.nkr_lim/2.
        min_ln = self.nkr_coor[1] - self.nkr_lim/2.
        max_ln = self.nkr_coor[1] + self.nkr_lim/2.

        # --- cat regions
        df_nk = df[(df['lat'] >= min_lt) & (df['lat'] <= max_lt) &
                   (df['lon'] >= min_ln) & (df['lon'] <= max_ln)]
        df_nk = df_nk.resample(rsm_time).mean()
        pds_nk = pd.Series(df_nk['xCO'].values, index=df_nk.index)

        # --- dif
        pds_dif = pd.Series(df_kr['xCO'].values - df_nk['xCO'].values, index=df_nk.index)
        # pds_dif = pds_kr

        # --- plot
        f_name = self.plt_dir + 'xCO_' + cdate
        plt_timser.plot_ts([pds_kr, pds_nk], pds_dif, ['r', 'k'], ['Krs', 'Not'], [], f_name)
