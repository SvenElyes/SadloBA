# Create "Starting Points",
__all__ = ["imageDataSeeds"]
import vtk
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonDataModel import (
    vtkDataSet,
    vtkDataObject,
    vtkPointSet,
    vtkImageData,
    vtkPolyData,
)
import numpy as np
from vtkmodules.vtkCommonDataModel import vtkDataObject, vtkStructuredGrid, vtkImageData
from vtkmodules.numpy_interface import dataset_adapter as dsa
from .paraview_util import *


@smproxy.source(label="ImageDataSeeds")
class imageDataSeeds(VTKPythonAlgorithmBase):
    """Generate seeds offset in complex eigenplane. Input needs to have Eigenvalue and Eigenvector arrays."""

    def __init__(self):
        self._num_seeds = 25
        self._offset = 0.01
        self._resolution = 20
        self._minx = 0
        self._miny = 0
        self._maxx = 10
        self._maxy = 10
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=0,
            nOutputPorts=1,
            outputType="vtkPolyData",
        )
        # Is point set or poly data better.?

    def FillOutputPortInformation(self, port, info):
        if port == 1:
            info.Set(vtkDataObject.DATA_TYPE_NAME(), "vtkPolyData")
        elif port == 0:
            info.Set(vtkDataObject.DATA_TYPE_NAME(), "vtkPolyData")
        return 1

    @smproperty.intvector(label="Seeds per Point", default_values=4)
    def SetNumSeeds(self, num):
        """Number of seeds per point"""
        self._num_seeds = num
        self.Modified()

    @smproperty.intvector(label="Resolution", default_values=20)
    def SetResolution(self, r):
        self._resolution = r
        self.Modified()

    def RequestData(self, request, inInfo, outInfo):
        # https://kitware.github.io/vtk-examples/site/Python/GeometricObjects/Point/
        output = dsa.WrapDataObject(vtkPolyData.GetData(outInfo, 0))

        x = np.linspace(self._minx, self._maxx, self._resolution)
        y = np.linspace(self._miny, self._maxy, self._resolution)
        xv, yv = np.meshgrid(x, y)
        zip_coords = zip(xv, yv)
        seeds = np.stack([xv, yv], axis=-1).reshape((2, -1), order="F").transpose()
        output = dsa.WrapDataObject(vtkPolyData())
        output.PointData.append(seeds, "Coordinates")
        print("seed shape:", seeds.shape)

        return 1
