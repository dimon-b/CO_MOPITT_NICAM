# -*- coding: utf-8 -*-
"""
Created on 30/06/2019 22:03
Project    CO
@author:   Dmitry
    Compare CO data
"""

import calendar


# === main class
class SetCase():

    # --- init
    def __init__(self):
        # --- path
        self.path = '../'
        self.mpt_r_dir = '/acnas5/MOPITT/V6/TIR-NIR/'
        self.mpt_m_dir = self.path + 'mid_dir/MOPITT-df/'
        self.out_dir = self.path + 'out_data/'
        self.mid_dir = self.path + 'mid_dir/'
        self.plt_dir = self.path + 'plots/'

        # --- calendar
        self.months = calendar.month_abbr[:]
        del self.months[0]
