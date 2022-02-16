__all__ = ["Model3DDoubleGyre"]

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


@smproxy.source(label="Model 3D Double Gyre")
class Model3DDoubleGyre(VTKPythonAlgorithmBase):
    def __init__(self):
        self._dimensions = [100, 50, 100]
        self._extent = [0.0, 2.0, 0.0, 1.0, 0.0, 1.0]
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=0, nOutputPorts=1)

    def FillOutputPortInformation(self, port, info):
        if port == 1:
            info.Set(vtkDataObject.DATA_TYPE_NAME(), "vtkImageData")
        elif port == 0:
            info.Set(vtkDataObject.DATA_TYPE_NAME(), "vtkImageData")
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        dim_spatial = len(self._dimensions)
        dim_spatial = min(3, dim_spatial)

        extent = [0] * 6
        for i in range(dim_spatial):
            extent[2 * i + 1] = self._dimensions[i] - 1
        image_origin = self._extent[: 2 * dim_spatial : 2]
        if len(image_origin) < 3:
            image_origin += [0.0] * (len(image_origin) - 3)
        image_spacing = [
            (self._extent[2 * i + 1] - self._extent[2 * i]) / (self._dimensions[i] - 1)
            for i in range(dim_spatial)
        ]
        if len(image_spacing) < 3:
            image_spacing += [0.0] * (len(image_spacing) - 3)

        out_info = outInfo.GetInformationObject(0)

        out_info.Set(vtkDataObject.ORIGIN(), image_origin, 3)
        out_info.Set(vtkDataObject.SPACING(), image_spacing, 3)

        return 1

    def double_gyre(self, data):
        """gets data and returns the vectors for the vector field,
        https://shaddenlab.berkeley.edu/uploads/LCS-tutorial/FTLE-interp.html#Eq13

        streamline function f (x,y)= sin( pi x )* sin(pi y)
        where u is the flow velocity parallel to and in the direction of the x-axis,
        and v is the flow velocity parallel to and in the direction of the y-axis. Thus, as δn → 0 and by rearranging, we have:

        u  = df/dy  = sin (pi * x ) * cos(pi y ) * pi
        v =  - df/dx = -pi * cos(pi * x) * sin (pi * y)

        Args:
            data ([type]): Input is the grid, with equidistance between the points.
        """
        x, y = data[0], data[1]
        u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.pi
        v = -1 * np.pi * np.cos(np.pi * x) * np.sin(np.pi * y)
        w = np.zeros(x.shape)
        result = np.stack([u, v, w], axis=-1)
        result = result.reshape(-1, 3)
        return result

    def RequestData(self, request, inInfo, outInfo):
        # make grid, calcualte the vectors at the grid postion
        executive = self.GetExecutive()
        out_info = outInfo.GetInformationObject(0)
        image_output = dsa.WrapDataObject(vtkImageData.GetData(outInfo, 0))

        coords = list(
            np.linspace(
                self._extent[2 * i], self._extent[2 * i + 1], self._dimensions[i]
            )
            for i in range(len(self._dimensions))
        )

        grid = np.meshgrid(*coords, indexing="ij")
        origin = np.array([a[0] for a in coords])

        # calculate Doouble Gyre
        results = self.double_gyre(grid)
        # image data output

        image_spacing = [
            coords[i][1] - coords[i][0] for i in range(len(self._dimensions))
        ]
        print("result shape:", results.shape)
        print("dimensions:", self._dimensions)
        print("spacing: ", image_spacing)
        print("origin:", origin)

        image_output.SetDimensions(self._dimensions)
        image_output.SetOrigin(origin)
        image_output.SetSpacing(image_spacing)
        # https://vcwiki.iwr.uni-heidelberg.de/viscompwiki/doku.php?id=knowledgebase:vtk-knowledge:vtkimagedata_numpy
        # but we already did that in the double_gyre function!
        image_output.PointData.append(results, "vector_field")

        return 1
