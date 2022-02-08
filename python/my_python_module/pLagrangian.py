from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonDataModel import (
    vtkDataSet,
    vtkDataObject,
    vtkPointSet,
    vtkImageData,
    vtkPolyData,
)
from vtkmodules.numpy_interface import dataset_adapter as dsa

import numpy as np

from .paraview_util import *
from .vectorfield import Vectorfield
from .calculateLD import calculate_Langrian_descriptor


"""
what does the @smproperty_inputarrat do exactly
What are cells?
Is the input VtkImageData , the value(scalar) at each cell and do we compute the gradient or do we have a vector at each point
VtkImageData inherits from VtkDataSet !
VtkPointSet inherits from Vtk DataSet ! 
What does request data object/ Request INformation do?"""


@smproxy.filter(label="Lagrangian Descriptor")
# @smhint_replace_input(0)
@smproperty.input(name="InputSeeds", label="Seeding Points", port_index=1)
@smdomain.datatype(dataTypes=["vtkPolyData"])
@smproperty.input(name="Input", label="Vector Field", port_index=0)
# @smdomain_inputarray("input_array")
# @smdomain_inputarray("input_array2", optional="1")
@smdomain.datatype(dataTypes=["vtkDataSet"])
class lagragianDescriptor(VTKPythonAlgorithmBase):
    def __init__(self):
        self._array_field = 0
        self.time_step = 1
        self.start_time = 0
        self.end_time = 10
        self.tau = 0.1
        self._array_name = self._array_field = None
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=1,
            nOutputPorts=1,
            inputType="vtkImageData",
            outputType="vtkImageData",
        )

    @smproperty.doublevector(name="T", default_values=10.0)
    def SetTau(self, tau):
        self.tau = tau
        self.Modified()

    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        self._array_field = field
        self._array_name = name
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
        inp = dsa.WrapDataObject(
            vtkImageData.GetData(inInfo[0], 0)
        )  # holds the points which descirbe the vectorfield and the parameters of our vectorfield
        inp_pd = dsa.WrapDataObject(
            vtkPolyData.GetData(inInfo[1], 0)
        )  # holds the points in the vectorfield, which we want to analyze and get their pathlenght
        output = dsa.WrapDataObject(
            vtkImageData.GetData(outInfo, 0)
        )  # holds the length of each of our points from port 1

        data = util.get_array(inp, self._array_field, self._array_name)

        if not inp or not output:
            return 0

        dimensions = list(inp.GetDimensions())
        origin = list(inp.GetBounds()[::2])
        spacing = list(inp.GetSpacing())

        dimensions = np.array(dimensions)
        origin = np.array(origin)
        spacing = np.array(spacing)
        boundary = None  # TODO
        vectorfield = Vectorfield(origin, spacing, boundary, data)

        seeds = inp_pd.Points
        seeds = seeds[:, :2]

        output.ShallowCopy(inp.VTKObject)
        results = calculate_Langrian_descriptor(
            vectorfield, seeds, self.tau, self.start_time, self.end_time, self.time_step
        )

        output.SetDimensions(dimensions)
        output.SetOrigin(origin)
        output.SetSpacing(spacing)
        output.PointData.append(results, self._array_name)
        output.GetPointData().SetActiveScalars(self._array_name)

        # What does the get_array function do exactly?

        # DO THE STUFF HERE
