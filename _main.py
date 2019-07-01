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

# === main
if __name__ == '__main__':


    # --- time start
    led = a_esttime.a_esttime(0)

    # --- set settings
    print(f'\nSet settings')
    case = set_case.SetCase()

    # --- MOPITT
    print(f'\nProcess MOPITT')
    years = [2015, 2016]
    obj = prc_MOPITT.ProcMopitt(case, years)
    obj.proc_raw()
    #obj.proc_df()


    # --- time end
    led = a_esttime.a_esttime(led)
