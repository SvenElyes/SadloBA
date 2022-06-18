# distance from start?

import h5py
import glob
import numpy as np
import os
import vtk
from pyevtk.hl import pointsToVTK
from vtkmodules.vtkCommonDataModel import (
    vtkDataSet,
    vtkDataObject,
    vtkPointSet,
    vtkImageData,
    vtkPolyData,
)
from vtkmodules.vtkIOXML import vtkXMLDataSetWriter
from vtkmodules.numpy_interface import dataset_adapter as dsa


temp_prev_point = np.zeros((100000, 3))
filelist = glob.glob("cleansc/*.vtu")
for file in sorted(filelist):

    f = h5py.File(f"{file}", "r")
    coord = np.asarray(f["Coordinates"])
    pID = np.asarray(f["ParticleIDs"])

    prev_x = np.ascontiguousarray(temp_prev_point[:, 0])
    prev_y = np.ascontiguousarray(temp_prev_point[:, 1])
    prev_z = np.ascontiguousarray(temp_prev_point[:, 2])

    for id, coo in zip(pID, coord):
        temp_prev_point[id] = coo

    clean_filename = os.path.splitext(file)[0]
    pointsToVTK(
        f"{clean_filename}pointswp",
        x,
        y,
        z,
        data={
            "particleID": pID,
            "masses": masses,
            "velocity": (x_v, y_v, z_v),
            "next_position": (next_x, next_y, next_z),
        },
    )
