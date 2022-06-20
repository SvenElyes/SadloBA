# Analyzing how and if the points interact with the centerpoint.
from configparser import MAX_INTERPOLATION_DEPTH
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


@smproxy.filter(label="CenterPointAnalysis")
# @smhint_replace_input(0)
@smproperty.input(name="Input", label="Coordinates2", port_index=0)
# @smdomain_inputarray("input_array")
@smdomain.datatype(dataTypes=["vtkUnstructuredGrid"])
class centerpoint(VTKPythonAlgorithmBase):
    def __init__(self):
        self._array_field = 0
        self._array_name = self._array_field = None
        self._neighborsnumber = 10
        self._centerat0 = []
        self._time_steps = None
        self._current_time_index = 0

        self.intervall_timesteps_length = None
        self.intervall_timesteps = []
        self.intervall_set_flag = False

        self.cutfoff = None
        self.control_center = []
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

    @smproperty.intvector(name="Length of Time Intervall", default_values=50)
    def SetTimeIntervall(self, itl):

        self.intervall_timesteps_length = itl
        self.Modified()

    @smproperty.doublevector(name="Cutoff", default_values=1.0)
    def SetCutoff(self, cutoff):

        self.cutoff = cutoff
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
        if self.intervall_set_flag == False:
            # TODO make the maximum depend on max timesteps
            self.intervall_timesteps = np.arange(
                0, 1356, self.intervall_timesteps_length, dtype=int
            )
            self.intervall_set_flag == True

        inp = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(inInfo[0], 0))
        center = numpy_support.vtk_to_numpy(inp.PointData["center"])
        coordinates = numpy_support.vtk_to_numpy(inp.GetPoints())
        differences = np.zeros(center.shape[0])
        # We want to check every self.intervall_timesteps_length time steps if the points moved closer or farther away from the center point.
        # For clarifiction. Every 100 Time steps we assign a new center point and analyze this one for the next 100
        if (current_time in self.intervall_timesteps) == True:
            self.control_center = copy.deepcopy(center)

        # analyze the center
        for idx, (point, controlpoint) in enumerate(zip(center, self.control_center)):

            if LA.norm(point) > self.cutoff:
                print(f"{point} point and {controlpoint} controlpoint")
                temp_diff = LA.norm(
                    np.subtract(point, controlpoint)
                )  # The distance between the control point and the normal point
                differences[idx] = temp_diff
        output.ShallowCopy(inp.VTKObject)
        output.PointData.append(differences, "distance")

        return 1
