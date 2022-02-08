"""A file designed to test the LD calcualtion before trying to plug it into paraviews pipeline/framework

"""
from vectorfield import Vectorfield
from calculateLD import calculate_Langrian_descriptor
import numpy as np
import scipy.interpolate as spint


def main():
    origin = (0, 0)
    spacing = (1.0, 1.0)
    dimensions = (5, 5)
    data_x = np.random.rand(dimensions[0] ** 2) * (
        dimensions[0]
    )  # generates dimension squared values between 0 and dimension
    data_y = np.random.rand(dimensions[1] ** 2) * (dimensions[1])
    data = np.column_stack((data_x, data_y))

    boundary = None
    print("data: \n", data)
    vectorfield = Vectorfield(origin, spacing, boundary, dimensions, data)

    print("test interpolate \n", vectorfield.interpolate((3, 2)))
    seeds = np.array(
        [
            [0.0, 0.0],
            [0.0, 1.0],
            [0.0, 2.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [1.0, 2.0],
            [2.0, 0.0],
            [2.0, 1.0],
            [2.0, 2.0],
        ]
    )

    scalar_field, new_points = calculate_Langrian_descriptor(
        vectorfield, seeds, 0.1, 0, 1, 0.1
    )


if __name__ == "__main__":
    main()
