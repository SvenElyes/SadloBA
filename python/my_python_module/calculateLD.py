__all__ = ['calculate_Langrian_descriptorpt']
import numpy as np


"""So we have a vectorfield.
We can visualize it as a Matrix. If we want the vector at point (x,y), we just
multiply the point as transposed vector with the matrix.

( -.5 1   )  (2)  = (3 ) . Vector at (2,4) is (3,-4)
(  -1  -.5)  (4)    (-4)

We then definen a grid, for which we want to compute the LD for all the grid points.
We definen the minimum and maximum x and y value, but also the amount of grid points per dimension

x_min,x_max= =-1,1    Nx = 100 ->    we have a grid with 100x100=10000 points.
y_min, y_max = -1,1   Ny = 100 -> 

We can always move the vectorfield in the space, by introducing 3 vectors pointing 
to 3 points of the new vectorfield and interpolating our values.



So after defining our vectorfield and our grid, we can start calculating our LD.
For the integration, we need certain parameters to be set though:

We have a certain state at time t in which we have our start condition set f(u,t)= y0
The integration will take place from the lower bound t-tau towards our upper bound t+tau.
We can divide our LD_calculation from (t-tau - tau) and (tau - t+tau) and call it forward and backward calculation.

We can also define our step size h, which will later determine, how delicate our integration will be carried out and 
how many integration steps we will do later.

for (int i = 0; i < integration_time_steps; ++i) {
    success = integrator.DoStep(current_position, integration_time, current_position);


Now lets get to calculating the LD for the vectorfield.
We take each point in our grid. We assume we are at the time t. Now we use integration,to get the 
new position of all our former grid points. We save their new positions in the first row of an Matrix  of the shape (10000,integration_steps)


We also save the length in a Matrix with the shape (10000,integrationsteps). 
We then repeat this step over an over. Usually we could just override the old points and lengths, but maybe their evolution would be nice to see.
We calculate the length with the L2 Norm. (sqrt. x1**2 + x2**2 + ...
At the end we have a Skalarfield, with each of the pathlengths (the last row of the lenght Matrix).



27. Jan:

We have to define the vectorfield different. Because our input data wont be the vectors describing a Matrix, but rather just data points, we have to describe our
Vectorfield different. This vectorfield class will also come with an Interpolator function, which will give us the values between the datapoints provided.
This vectorfield will have following parameters. 4 Adjacent datapoints (in a Square Form ) will define a cell. 
Origin : Describing the point, which will be (0,0) in our Vectorfield
Spacing:
Boundary:
Dimensions : We will not use this at first, as we will use a 2D Vectorfield 
data : Our datapoints which will be used to interpolate.
The Interpolator function will have the ability to to the do_step function: It will give us the approximate position of x after experiecing the vectorfield for dt time


Our result is a Scalar Field, which will have the length of each of the points we start with. We update it after each step



TOdo : Vectorfield, time dependent
       Bounding Box
       Warum mit cells und local indexen?
       """


def calculate_Langrian_descriptor(
    vectorfield, seeds, tau, start_time, end_time, time_step
):
    # seeds_rows, seeds_cols = seeds.shape[0], seeds.shape[1]
    number_of_steps = int((end_time - start_time) / time_step)
    # saves the position of all the points, after each step dt
    scalar_field = np.zeros((seeds.shape[0], 1))
    original_seeds = seeds.copy()
    print(seeds)
    print("seedshape:", seeds.shape)
    print("Number of steps:", number_of_steps)
    for current_step in range(1, number_of_steps):
        for idx, point in enumerate(seeds):

            newpoint, length = vectorfield.do_step(point, time_step)

            seeds[idx] = newpoint
            scalar_field[idx] = length + scalar_field[idx]
    print(scalar_field)
    for o, p, s in zip(original_seeds, seeds, scalar_field):
        print("original point:", o, "point:", p, "sclara", s)
    return scalar_field, seeds
