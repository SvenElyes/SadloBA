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
        print("dim_v:", dim_v)
        grid_max = origin + (dimensions - 1) * spacing
        print("grid_max:", grid_max)
        x = np.linspace(origin[0], grid_max[0], dimensions[0])
        y = np.linspace(origin[1], grid_max[1], dimensions[1])
        z = np.linspace(origin[2], grid_max[2], dimensions[2])
        grid_coords = [x, y, z]
        self.grid_coords = grid_coords
        u = data.reshape(list(dimensions) + [dim_v], order="F")
        print(
            "Building interpolator with following data \n grid coords:\n",
            grid_coords,
            "which has following type ",
            type(grid_coords),
            "and length",
            len(grid_coords),
            "\n data shape:\n",
            data.shape,
            "and u shape",
            u.shape,
        )
        self.interpolator = RegularGridInterpolator(
            grid_coords, u, bounds_error=False, fill_value=np.nan
        )

    def interpolate(self, point):
        # point has to be shape (x,y,z)
        print("\n Interpolate has been called, with following point :", point)
        result_skalar = self.interpolator(point)
        print("and the result was: ", result_skalar)
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
        print(
            "Do_STEP with following parameters. \n Start point x_old:",
            x_old,
            "dt:\n",
            dt,
        )
        k1 = self.interpolator(x_old)
        print("k1 shape ", k1.shape)
        k2 = self.interpolator(x_old + k1 * dt / 2.0)
        k3 = self.interpolator(x_old + k2 * dt / 2.0)
        k4 = self.interpolator(x_old + k3 * dt)
        integral = k1 / 6.0 + k2 / 3.0 + k3 / 3.0 + k4 / 6.0

        x_new = x_old + dt * integral
        length = np.linalg.norm(dt * integral)

        return x_new, length
