# Analyzing how and if the points interact with the centerpoint.
from configparser import MAX_INTERPOLATION_DEPTH
import enum
from tempfile import tempdir
from unittest import result
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonDataModel import (
    vtkDataSet,
    vtkDataObject,
    vtkPointSet,
    vtkUnstructuredGrid,
    vtkImageData,
    vtkPolyData,
    vtkKdTree,
)
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, vtkIntArray
from vtkmodules.numpy_interface import dataset_adapter as dsa
from numpy import linalg as LA
import numpy as np
from vtk.util import numpy_support
from .paraview_util import *
from .vectorfield import Vectorfield
from .calculateLD import calculate_Langrian_descriptor
from .util_arrays import get_array, find_array, field_from_association
import vtk
import copy


@smproxy.filter(label="Shortest Distance")
# @smhint_replace_input(0)
@smproperty.input(name="Input", label="Coordinates2", port_index=0)
# @smdomain_inputarray("input_array")
@smdomain.datatype(dataTypes=["vtkUnstructuredGrid"])
class shortestdistance(VTKPythonAlgorithmBase):
    def __init__(self):
        self._array_field = 0
        self._array_name = self._array_field = None

        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=1,
            nOutputPorts=1,
            inputType="vtkUnstructuredGrid",
            outputType="vtkUnstructuredGrid",
        )

    @smproperty.intvector(name="Number of Neighbors", default_values=10)
    def SetNeigborsnumber(self, neigborsnumber):
        self.neigborsnumber = neigborsnumber
        self.Modified()

    def RequestDataObject(self, request, inInfo, outInfo):
        inp = vtkDataSet.GetData(inInfo[0], 0)
        if not inp:
            return 0
        for i in range(self.GetNumberOfOutputPorts()):
            output = vtkDataSet.GetData(outInfo, i)
            if not output or not output.IsA(inp.GetClassName()):
                outInfo.GetInformationObject(i).Set(
                    vtkDataObject.DATA_OBJECT(), inp.NewInstance()
                )
        return 1

    def RequestData(self, request, inInfo, outInfo):
        executive = self.GetExecutive()
        inp = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(inInfo[0], 0))
        output = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfo, 0))
        in_info = inInfo[0].GetInformationObject(0)
        out_info = outInfo.GetInformationObject(0)
        current_time = in_info.Get(executive.UPDATE_TIME_STEP())
        max_time = in_info.Get(executive.TIME_STEPS())

        inp = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(inInfo[0], 0))
        neighbors = numpy_support.vtk_to_numpy(inp.PointData["neighbors"])
        neighbors_set = numpy_support.vtk_to_numpy(inp.PointData["neighbors_set"])
        coordinates = numpy_support.vtk_to_numpy(inp.GetPoints())

        distances = np.zeros(neighbors.shape[0])
        print(f"neighbors set shape {neighbors_set.shape}")
        for pointID, (point, neighborIDs) in enumerate(zip(coordinates, neighbors)):
            if neighbors_set[pointID] == 1:
                # get the closest neighbor
                closest_neighborID = neighborIDs[1]  # first value is the point itself
                closest_neighbor = [0, 0, 0]
                inp.GetPoint(closest_neighborID, closest_neighbor)

                # get the distance to the point
                temp_distance = LA.norm(np.subtract(point, closest_neighbor))
                distances[pointID] = temp_distance
                print(f"point {point} neighbor {closest_neighbor}")

        output.ShallowCopy(inp.VTKObject)
        output.PointData.append(distances, "distances")

        return 1
