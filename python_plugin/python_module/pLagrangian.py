from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonDataModel import vtkDataSet, vtkDataObject, vtkPointSet, vtkImageData
from vtkmodules.numpy_interface import dataset_adapter as dsa

import numpy as np

from .paraview_util import smproxy, smproperty, smdomain, smhint


'''
Was sind input seeds?
what does the @smproperty_inputarrat do exactly
What are cells?
Is the input VtkImageData , the value(scalar) at each cell and do we compute the gradient or do we have a vector at each point
VtkImageData inherits from VtkDataSet !
VtkPointSet inherits from Vtk DataSet ! 
What does request data object/ Request INformation do?'''

@smproxy.filter(label='Lagrangian Descriptor')
@smhint_replace_input(0)
@smproperty.input(name='InputSeeds', label='Seeding Points', port_index=1)
@smdomain.datatype(dataTypes=['vtkPolyData'])
@smproperty.input(name='Input', label='Vector Field', port_index=0)
@smdomain_inputarray('input_array')
@smdomain.datatype(dataTypes=['vtkDataSet']
class lagragianDescriptor(VTKPythonAlgorithmBase):
    def __init__(self):
        self._array_field = 0
        self.time_step = 1
        self.start_time = 0
        self.end_time = 10
        self.tau = 0.1
        self._array_name = self._array_field = None
        VTKPythonAlgorithmBase.__init__(self,
                                nInputPorts=1, nOutputPorts=1, inputType='vtkImageData', outputType='vtkImageData') 

    @smproperty.doublevector(name='T', default_values=10.0)
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
                    vtkDataObject.DATA_OBJECT(), inp.NewInstance())
        return 1


    def RequestData(self,request,inInfo, outInfo):
        inp = dsa.WrapDataObject(vtkImageData.GetData(inInfo[0], 0))
        output = dsa.WrapDataObject(vtkImageData.GetData(outInfo, 0))
        
               
        array = util.get_array(inp, self._array_field, self._array_name)

        if not inp or not output:
            return 0
         
        dimensions = inp.GetDimensions()[:2]
        origin = inp.GetBounds()[::2][:2]
        spacing = inp.GetSpacing()[:2]

        vectorfield= Vectorfield(origin, spacing,boundary,v)
        image.GetPointData().GetScalars().DeepCopy(vtk_array)
        
        output.ShallowCopy(inp.VTKObject) 
        x_min,x_max,Nx,y_min,y_max,Ny= 
        grid =[(x_min,x_max,Nx,y_min,y_max,Ny)]
        results = ld.calculate_Langragian_Descriptor(vectorfield, grid, self.tau, self.start_time, self.end_time, self.time_step)
        
        output.SetDimensions(dimensions)
        output.SetOrigin(origin)
        output.SetSpacing(spacing)
        output.PointData.append(results, self._array_name)
        output.GetPointData().SetActiveScalars(self._array_name)

        #What does the get_array function do exactly?

        #DO THE STUFF HERE











































def lagragian_descriptor(
    position, integration_time_steps, integration_time, vectorfield
):
"""Explanation of a particle that moves through the vector field. We start at POSITION. at POSITION we have vector x1. Now we normalize the vector x1 with inegration time. Meaning after one unit of
    time, the particle is now at POSITION2. There we look at the present vectorx2. To get that vector, we have to interpolate between the grid points. We do that process for integration_time_steps.
    pass
"""
    total_distance= 0
    for steps:
        temp_position,temp_distance = do_Step(position,vector,time_step)
        position=temp_position
        total_distance = total_distance + temp_distance


    return total_distance



def do_Step(position,vector,time_step,):

    norm = np.linalg.norm(vector)
    if norm == 0: 
       return False
    normed_vector = vector / norm
    new_position = position + normed_vector *time_step
    return new_position, euclidean_distance
