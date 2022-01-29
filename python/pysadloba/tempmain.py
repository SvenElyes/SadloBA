"""A file designed to test the LD calcualtion before trying to plug it into paraviews pipeline/framework

"""
from vectorfield import Vectorfield
import calculateLD
import numpy as np
import scipy.interpolate as spint


def main():
    origin = (0, 0)
    spacing = (1.0, 1.0)
    dimensions = (3, 3)
    data_x = np.random.rand(dimensions[0] ** 2)
    data_y = np.random.rand(dimensions[1] ** 2)
    data = np.column_stack((data_x, data_y))

    boundary = None

    vectorfield = Vectorfield(origin, spacing, boundary, dimensions, data)
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

    calculateLD.calculate_Langrian_descriptor(vectorfield, seeds, 0.1, 0, 1, 0.1)


if __name__ == "__main__":
    main()
