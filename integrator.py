import vectorfield
import numpy as np

import LD 
from vtkmodules.vtkCommonDataModel import vtkDataSet, vtkDataObject, vtkPointSet, vtkImageData
from vtkmodules.numpy_interface import dataset_adapter as dsa

'''
Was sind input seeds?
what does the @smproperty_inputarrat do exactly
VtkImageData inherits from VtkDataSet !
VtkPointSet inherits from Vtk DataSet ! '''

@smproxy.filter(label='Lagrangian Descriptor')
@smhint_replace_input(0)
@smproperty.input(name='InputSeeds', label='Seeding Points', port_index=1)
@smdomain.datatype(dataTypes=['vtkPointSetData'])
@smproperty.input(name='Input', label='Vector Field', port_index=0)
@smdomain_inputarray('input_array')
@smdomain.datatype(dataTypes=['vtkDataSet']

class lagragianDescriptor(VTKPythonAlgorithmBase):
    def __init__(self):
        self._array_field = 0
        self.step_size = 0.1
        self.num_steps = 10
        self._array_name = self._array_field = None
        VTKPythonAlgorithmBase.__init__(self,
                                nInputPorts=1, nOutputPorts=1, inputType='vtkImageData', outputType='vtkImageData') 

    
   
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
        output = dsa.WrapDataObject(vtkPointSet.GetData(outInfo, 0))

        if not inp or not output:
            return 0
        output.ShallowCopy(inp.VTKObject)

        J = util.get_array(inp, self._array_field, self._array_name)
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
