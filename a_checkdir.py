#!/usr/bin/env python
"""
Created on 05/04/2019 15:15
@author:   Dmitry
    Check directory
"""

def check_dir(file_path):
    import os

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)