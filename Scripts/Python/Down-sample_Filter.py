# -*- coding: utf-8 -*-
"""


@author: Lukas Pekarek & Stefan Buck from Recoding Mechanisms in Infection (REMI) group lead by Neva Caliskan
"""




from tkinter import filedialog
import numpy as np
import h5py
from scipy import signal


save_to = "path/to/processed/data"  # Add the path where to save your processed data 
settings = {                    # adjust the parameters values according to your needs
    'downsample_value': '50',
    'filter_degree': '4',
    'filter_cut_off': '0.005',
    }


def getRAW_File_h5(import_file_path, settings): # a function loading the raw data 
    with h5py.File(import_file_path, "r") as raw_data:
        Force_1x = raw_data.get("Force HF/Force 1x")
        ForceY = np.array(Force_1x)
        Piezo_Distance = raw_data.get("Distance/Piezo Distance")
        DistanceX = np.array(Piezo_Distance)

    return ForceY, DistanceX


def preprocess_RAW(Force, Distance, settings): # function responsible for the pre-processing itself (downsampling + singal filtering)
    # Downsample
    Force_ds = Force[::int(settings['downsample_value'])]
    Distance_ds = Distance[::int(settings['downsample_value'])]

    # Filter
    b, a = signal.butter(int(settings['filter_degree']), float(settings['filter_cut_off']))
    filteredForce = signal.filtfilt(b, a, Force_ds)
    filteredDistance = signal.filtfilt(b, a, Distance_ds)
    filteredDistance_ready = filteredDistance * 1000

    Force_Distance = np.column_stack((filteredForce, filteredDistance_ready))

    return Force_Distance


import_file_path = filedialog.askopenfilename()
F, D = getRAW_File_h5(import_file_path, settings)
FD = preprocess_RAW(F, D, settings)
np.savetxt(save_to, FD, delimiter=",")
