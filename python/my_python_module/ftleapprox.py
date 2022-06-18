# Analyzing how and if the points interact with the centerpoint.
from configparser import MAX_INTERPOLATION_DEPTH
from operator import ne
from tempfile import tempdir
from unittest import result
import math
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


@smproxy.filter(label="FTLEApprox")
# @smhint_replace_input(0)
@smproperty.input(name="Input", label="Coordinates2", port_index=0)
# @smdomain_inputarray("input_array")
@smdomain.datatype(dataTypes=["vtkUnstructuredGrid"])
class ftleapprox(VTKPythonAlgorithmBase):
    def __init__(self):
        self._array_field = 0
        self._array_name = self._array_field = None
        self._h_index = 5
        self._centerat0 = []
        self._h_ball = []
        self._time_steps = None
        self._current_time_index = 0
        self.intervall_timesteps = np.arange(0, 1356, 50, dtype=float)

        # TODO make the maximum depend on max timesteps, and make type to int
        self.control_center = []
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=1,
            nOutputPorts=1,
            inputType="vtkUnstructuredGrid",
            outputType="vtkUnstructuredGrid",
        )

    @smproperty.doublevector(name="SetNumberofH", default_values=5)
    def SetNeigborsnumber(self, h_index):
        self.h_index = int(
            h_index
        )  # defines the nth number of neighbors, which marks the
        # TODO h hindex has to be smaller than the numbe rof neigbors in INPUT
        # TODO change the type in property
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
        inp = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(inInfo[0], 0))

        # t (time that has been elapsed since setting the controlling )
        idx = (
            np.abs(self.intervall_timesteps - current_time)
        ).argmin()  # idx tells us the last timestep, controll point was set
        time_ellapsed = current_time - self.intervall_timesteps[idx]
        # FTLE ~~ 1/T * log A/h
        # h breite des balls am Ersten Zeitpunk. A Breite des Balls am Ende
        neighbors = numpy_support.vtk_to_numpy(inp.PointData["neighbors"])

        a_ball = np.zeros(neighbors.shape[0])
        ftle = np.ones(neighbors.shape[0])  # shoudl the values we dont dompute be 0 ?
        neigborssum = np.sum(neighbors, axis=1)
        # only do this every xth timestep
        print("current time", current_time)
        print(f"{neighbors.shape[0]} neigbors shape")
        if (current_time in self.intervall_timesteps) == True:
            print("Current time is in Time Intervall")
            self._h_ball = np.zeros(neighbors.shape[0])
            for index, (point, sum) in enumerate(zip(neighbors, neigborssum)):
                if sum != 0:
                    h_point = [0, 0, 0]
                    inp.GetPoint(point[self.h_index], h_point)
                    control_point = [0, 0, 0]
                    inp.GetPoint(index, control_point)
                    distance = LA.norm(np.subtract(h_point, control_point))
                    self._h_ball[index] = distance

        # compute A.
        for index, (point, sum) in enumerate(zip(neighbors, neigborssum)):
            if sum != 0:
                print(f"{index} index")
                a_point = [0, 0, 0]
                inp.GetPoint(point[self.h_index], a_point)
                control_point = [0, 0, 0]
                inp.GetPoint(index, control_point)
                distance = LA.norm(np.subtract(a_point, control_point))
                a_ball[index] = distance

        """
        for index, (point, sum) in enumerate(zip(neighbors, neigborssum)):
            if sum != 0 and current_time not in self.intervall_timesteps:
                # this for and if loop checks if we computed the neigbors for the point in a previous filter. Such we can assing only to those an approx FTLE
                print("Current time", current_time, "time ellapsed", time_ellapsed)
                print("hball shape", self._h_ball.shape)
                print("index,", index)
                print("h ball ", self._h_ball[index])

                print("a ball", a_ball[index])
                x = a_ball[index] / self._h_ball[index]
                print("x", x)
                # TODO check if h_ball is 0
                if time_ellapsed == 0 or self._h_ball[index] == 0:

                    print("0 INciident")
                    break
                else:
                    FTLE_value = (1 / time_ellapsed) * math.log(
                        a_ball[index] / self._h_ball[index]
                    )
                    print("FTLE", FTLE_value)
                    ftle[index] = FTLE_value
        """
        output.ShallowCopy(inp.VTKObject)
        # output.PointData.append(ftle, "ftle")

        return 1
