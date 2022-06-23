from configparser import MAX_INTERPOLATION_DEPTH
from unittest import result
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonDataModel import (
    vtkDataSet,
    vtkDataObject,
    vtkUnstructuredGrid,
    vtkPointSet,
    vtkImageData,
    vtkPolyData,
    vtkKdTree,
)
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, vtkIntArray
from vtkmodules.numpy_interface import dataset_adapter as dsa

import numpy as np
from vtk.util import numpy_support
from .paraview_util import *
from .vectorfield import Vectorfield
from .calculateLD import calculate_Langrian_descriptor
from .util_arrays import get_array, find_array, field_from_association
import vtk

# TODO the first value in closest n neighbors is the point itself


@smproxy.filter(label="Clump")
# @smhint_replace_input(0)
@smproperty.input(name="Input", label="Coordinates", port_index=0)
# @smdomain_inputarray("input_array")
@smdomain.datatype(dataTypes=["vtkUnstructuredGrid"])
class clump(VTKPythonAlgorithmBase):
    def __init__(self):
        self._array_field = 0
        self._array_name = self._array_field = None
        self._neighborsnumber = 10
        self._centerat0 = []
        self._time_slices = []
        self._point_arrays = []
        self._time_steps = None
        self._current_time_index = 0
        self.number_of_points = None
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=1,
            nOutputPorts=1,
            inputType="vtkUnstructuredGrid",
            outputType="vtkUnstructuredGrid",
        )

    @smproperty.intvector(name="Number of neighbors", default_values=10)
    def SetNeighborsnumber(self, neighborsnumber):
        self._neighborsnumber = neighborsnumber
        self.Modified()

    @smproperty.intvector(name="Points to check (STEPSIZE)", default_values=100)
    def SetPointstocheck(self, ptc):
        self.number_of_points = ptc
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

    """"
    def RequestInformation(self, request, inInfo, outInfo):
        # https://docs.paraview.org/en/latest/ReferenceManual/pythonProgrammableFilter.html
        # https://vcgitlab.iwr.uni-heidelberg.de/prtl/prtl/-/blob/master/python/pyprtl/ndfields/prtlSpaceTimeField.py
        executive = self.GetExecutive()

        self._time_slices = [[] for _ in self._point_arrays]
        self._current_time_index = 0
        self._time_steps = None

        in_extent = None
        if (
            len(inInfo) > 0
            and inInfo[0]
            and inInfo[0].GetNumberOfInformationObjects() > 0
        ):
            in_info = inInfo[0].GetInformationObject(0)
            # in_extent = list(in_info.Get(executive.WHOLE_EXTENT()))
            if in_info.Has(executive.TIME_STEPS()):
                self._time_steps = in_info.Get(executive.TIME_STEPS())
                # gives an tuple  with all the timesteps.(0.0, 1.0, 2.0, ... 1335.0)

        return 1
    """

    def RequestData(self, request, inInfo, outInfo):

        # https://gitlab.kitware.com/paraview/paraview/blob/master/Examples/Plugins/PythonAlgorithm/PythonAlgorithmExamples.py
        # https://python.hotexamples.com/de/examples/vtk/-/vtkKdTree/python-vtkkdtree-function-examples.html
        # https://vcgitlab.iwr.uni-heidelberg.de/prtl/prtl/-/blob/master/python/pyprtl/dependent_vectors/prtlAppendDataArrays.py
        executive = self.GetExecutive()
        in_info = inInfo[0].GetInformationObject(0)
        out_info = outInfo.GetInformationObject(0)
        current_time = in_info.Get(executive.UPDATE_TIME_STEP())
        # print("current time,", current_time)
        inp = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(inInfo[0], 0))
        PDkeys = inp.PointData.keys()
        FDkeys = inp.FieldData.keys()
        # print("PD Keys", PDkeys, "FDkeys", FDkeys)
        coordinates = numpy_support.vtk_to_numpy(inp.GetPoints())
        output = dsa.WrapDataObject(vtkUnstructuredGrid.GetData(outInfo, 0))

        points_to_check = np.arange(
            0, 99999, self.number_of_points, dtype=int
        )  # the pointIDs we want to analyze. #TODO make the maximum of points dependent of numb erof points in input

        # We need to create a Vtk Points instance to build the KDTree from our coordiates

        vpoints = vtk.vtkPoints()
        vpoints.SetNumberOfPoints(coordinates.shape[0])
        for i in range(coordinates.shape[0]):
            vpoints.SetPoint(i, coordinates[i])
        kDTree = vtkKdTree()
        kDTree.BuildLocatorFromPoints(vpoints)

        # Build Neigbors array
        neighbors = vtk.vtkIntArray()
        neighbors.SetNumberOfComponents(self._neighborsnumber)
        neighbors.SetNumberOfTuples(inp.GetNumberOfPoints())
        neighbors.SetName("neighbors")

        # because we have problems with the neigbors array for values we didnt set, we introduce an array containing the boolaen information

        neighbors_set = np.zeros(coordinates.shape[0])
        # Build Center Point Array. Center Point is the average of the main point and 2 of its closests neigbors.
        center = vtk.vtkPoints()
        center.SetNumberOfPoints(coordinates.shape[0])  # points_to_check.shape[0]

        """
        We are iterating over the points in the points_to_check array. For each point we 
        1. Find the N closest Neigbors with the kDTree structure.
        2. Find the center of Mass for the iterating point and assigning the center point to it.
        3. Appending the neigbor Ids to the neigbor array to our point, we are analyzing.
        """
        for pointId in range(inp.GetNumberOfPoints()):
            if pointId in points_to_check:

                point = [0, 0, 0]
                inp.GetPoint(pointId, point)
                neighborIds = vtk.vtkIdList()
                kDTree.FindClosestNPoints(
                    int(self._neighborsnumber), point, neighborIds
                )  # Does this also give us the point itself back?

                npneighbors = np.array(
                    [neighborIds.GetId(i) for i in range(neighborIds.GetNumberOfIds())]
                )

                intersection = [i for i in npneighbors if i in points_to_check]
                if pointId not in npneighbors:

                    npneighbors.append(pointId)

                neighbor_coord = vtk.vtkPoints()
                neighbor_coord.SetNumberOfPoints(npneighbors.shape[0])
                for i in range(npneighbors.shape[0]):
                    neighbor_coord.SetPoint(i, coordinates[i])

                polydata = vtk.vtkPolyData()
                polydata.SetPoints(neighbor_coord)

                centerOfMass = vtk.vtkCenterOfMass()
                centerOfMass.SetInputData(polydata)
                centerOfMass.SetUseScalarsAsWeights(False)
                centerOfMass.Update()

                G = centerOfMass.GetCenter()

                center.SetPoint(pointId, G)
                neighbors.SetTuple(pointId, npneighbors)

                neighbors_set[pointId] = 1

        output.ShallowCopy(inp.VTKObject)
        neighbors_np = numpy_support.vtk_to_numpy(neighbors)
        center_np = numpy_support.vtk_to_numpy(
            center.GetData()
        )  # https://stackoverflow.com/questions/5497216/convert-vtkpoints-to-numpy-array
        output.PointData.append(neighbors_np, "neighbors")
        output.PointData.append(center_np, "center")
        output.PointData.append(neighbors_set, "neighbors_set")
        out_info.Set(vtkDataObject.DATA_TIME_STEP(), current_time)

        return 1
