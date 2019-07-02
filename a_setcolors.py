# -*- coding: utf-8 -*-
"""
Created on 22/04/2019 19:19
@author:   Dmitry
    Set colors
"""

import matplotlib


# === set colors
def set_colors(i_lens=0, i_cmap=''):
    if i_cmap == '':
        colors = ['Cyan', 'Orange', 'Blue', 'Red', 'Yellow', 'Lime', 'Green', 'Purple', 'Magenta', 'Grey']
    else:
        cmap = matplotlib.cm.get_cmap(i_cmap)
        colors = []
        for iss in range(0, i_lens):
            colors.append(cmap(iss / i_lens))

    return colors
