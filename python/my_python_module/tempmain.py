"""file to test our 2ddouble Gyre"""
import numpy as np
import matplotlib.pyplot as plt


def double_gyre(data):
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
    print("x:", x.shape)
    print("y:", y.shape)
    u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.pi
    v = -1 * np.pi * np.cos(np.pi * x) * np.sin(np.pi * y)
    w = np.zeros(x.shape)
    print("len u:", len(u))
    print("len(v):", len(v))
    print(w)
    print("u:", u)
    print("v:", v)
    # return u, v
    result = np.stack([u, v, w], axis=-1)
    result = result.reshape(-1, 3)
    return result


def main():
    """
    nx, ny = (10, 5)
    x = np.linspace(0, 2, nx)
    y = np.linspace(0, 1, ny)
    xv, yv = np.meshgrid(x, y)
    """
    coords = list(np.linspace(0, 10, 10) for i in range(3))
    print(type(coords))

    print(np.asarray(coords))
    # data = [xv, yv]
    # u, v = double_gyre(data)
    # result = double_gyre(data)
    # print(result.shape)
    # plt.quiver(xv, yv, u, v)
    # plt.show()
    # result = result.reshape(-1, 3)
    # print(result)


if __name__ == "__main__":
    main()
