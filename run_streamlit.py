# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 17:38:34 2026

@author: BBarsch
"""

import subprocess
import os 
#file = "app.py"
#file = "app_plots.py"
#file = "app_profiler.py"
file = "app_profiler_menus.py"


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_PHOTO = os.path.join(BASE_DIR, "Reatile Prof Photo - Copy (1).jpg")
DEV_ECON_PDF  = os.path.join(BASE_DIR, "EDEV ESSAY ASSIGNMENT.pdf")
INT_ECON_PDF  = os.path.join(BASE_DIR, "Reatile Seekoei - 2021109463.pdf")
EOY_PDF       = os.path.join(BASE_DIR, "ReatileSeekoei_EoY_Oct2025.pdf")



subprocess.Popen(
    ["streamlit", "run", file], shell=True
)