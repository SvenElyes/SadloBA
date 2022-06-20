import h5py
import glob
import numpy as np
import os
import vtk
from pyevtk.hl import pointsToVTK, imageToVTK
from vtkmodules.vtkCommonDataModel import (
    vtkDataSet,
    vtkDataObject,
    vtkPointSet,
    vtkImageData,
    vtkPolyData,
)
from vtkmodules.vtkIOXML import vtkXMLDataSetWriter
from vtkmodules.numpy_interface import dataset_adapter as dsa

# https://www.programcreek.com/python/?code=princeton-vl%2FDeepV2D%2FDeepV2D-master%2Fdeepv2d%2Fvis.py


temp_next_point = np.zeros((100000, 3))

for file in glob.glob("cleansc/*.hdf5"):

    print(file)

    f = h5py.File(f"{file}", "r")
    pID = np.asarray(f["ParticleIDs"])
    coord = np.asarray(f["Coordinates"])
    masses = np.asarray(f["Masses"])
    velocity = np.asarray(f["Velocities"])
    print(
        coord.shape,
    )
    # x,y,z =np.transpose(coord) cant transpose, as the arrays are not C or F contagious.?
    x = np.ascontiguousarray(coord[:, 0])
    y = np.ascontiguousarray(coord[:, 1])
    z = np.ascontiguousarray(coord[:, 2])

    # AssertionError: Bad array shape: (100000, 3)
    x_v = np.ascontiguousarray(velocity[:, 0])
    y_v = np.ascontiguousarray(velocity[:, 1])
    z_v = np.ascontiguousarray(velocity[:, 2])

    next_x = np.ascontiguousarray(temp_next_point[:, 0])
    next_y = np.ascontiguousarray(temp_next_point[:, 1])
    next_z = np.ascontiguousarray(temp_next_point[:, 2])
    # next_x,next_y,next_z =XXX
    # distance already
    for id, coo in zip(pID, coord):
        temp_next_point[id] = coo
    clean_filename = os.path.splitext(file)[0]
    pointsToVTK(
        f"{clean_filename}points",
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
