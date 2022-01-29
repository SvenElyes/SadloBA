from scipy.interpolate import RegularGridInterpolator
import numpy as np


class Vectorfield:
    def __init__(self, origin, spacing, boundary, dimensions, data):
        self.origin = origin
        self.spacing = spacing  # spacing (width,height,length) of the cubical cells that compose the data set.
        self.boundary = boundary
        self.dimensions = dimensions  # It is the number of points on each axis
        self.data = data  # data is in the shape (Spacing*Spacing , [a,b]). As vtkImageData describes a uniform grid, we can assume the x y position of the vector [a b]

        dimensions = np.array(dimensions)
        origin = np.array(origin)
        spacing = np.array(spacing)
        """
        print("dimension", dimensions)
        print("origin", origin)
        print("spacing", spacing)
        print("len datashape:", len(data.shape))
        """
        dim_v = data.shape[1] if len(data.shape) > 1 else 1
        # print("dim_v:", dim_v)
        grid_max = origin + (dimensions - 1) * spacing
        x = np.linspace(origin[0], grid_max[0], dimensions[0])
        y = np.linspace(origin[1], grid_max[1], dimensions[1])
        grid_coords = [x, y]
        # print("grid_coords:", grid_coords)
        # print("data.shape", data.shape)
        self.grid_coords = grid_coords
        u = data.reshape(list(dimensions) + [dim_v], order="F")

        # print(u.shape)
        self.vectorfield = RegularGridInterpolator(
            grid_coords, u, bounds_error=False, fill_value=np.nan
        )

    def interpolate(self, point):
        # point has to be shape (x,y)
        result_skalar = self.vectorfield(point)
        return result_skalar

    def get_data(self):
        return self.data

    def get_grid_coords(self):
        return self.grid_coords

    def get_dimensions(self):
        return self.dimensions

    def get_spacing(self):
        return self.spacing

    def boundary_function(self):
        pass
        # check if value is inside defined boundary

    def do_step(self, x_old, dt):

        k1 = self.vectorfield(x_old)
        k2 = self.vectorfield(x_old + k1 * dt / 2.0)
        k3 = self.vectorfield(x_old + k2 * dt / 2.0)
        k4 = self.vectorfield(x_old + k3 * dt)
        integral = k1 / 6.0 + k2 / 3.0 + k3 / 3.0 + k4 / 6.0

        x_new = x_old + dt * integral
        length = np.linalg.norm(dt * integral)

        return x_new, length
