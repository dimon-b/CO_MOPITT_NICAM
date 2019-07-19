# -*- coding: utf-8 -*-
"""
Created on 30/06/2019 22:03
Project    CO
@author:   Dmitry
    Compare CO data
"""

import a_esttime
import set_case
import prc_MOPITT
import drw_map
import drw_timeser

# === main
if __name__ == '__main__':


    # --- time start
    led = a_esttime.a_esttime(0)

    # --- set settings
    print(f'\nSet settings')
    case = set_case.SetCase()

    # --- MOPITT raw
    rd = 0
    if rd:
        print(f'\nProcessing h5 MOPITT files')
        years = [2009, 2010]
        obj = prc_MOPITT.ProcMopitt(case, years)
        obj.proc_raw()

    # --- MOPITT cites
    ts = 0
    if ts:
        print(f'\nTime series of MOPITT')
        years = [2009, 2016]
        obj = drw_timeser.DrwTmser(case, years)
        obj.proc_cts()

    # --- MOPITT map
    mp = 1
    if mp:
        print(f'\nMap MOPITT')
        years = [2015, 2016]
        obj = drw_map.DrwMap(case, years)
        obj.map_co()

    # --- time end
    led = a_esttime.a_esttime(led)
