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



TOdo : Vectorfield, time dependent
       Bounding Box
       """


class Vectorfield:
    # just a 2x2 Matrix for the beginning.
    # introduce ways to map to Physical Space and back
    def __init__(self, u, v):

        self.v = np.columnstack(u, v)
        return v

    def multiply(self,x):
        return self.v.multiply(x)

    def maptoPhysical()
        pass
def do_step(vectorfield,x,dt):
    #using Runge Kutta 4 to get the new point
    #use L2 Norm to get the length of the trajectory from t0 to t1.
    return newpoint, length

grid_coordinates = [(-1, 1, 100), (-1, 1, 100)]  # [(xmin,xmax,Nx),(ymin,ymax,Ny)]

def calculate_Langrian_descriptor(vectorfield, grid, tau, start_time, end_time, time_step):

    _,_,Nx = grid[0]
    _,_,Ny = grid[1]
    number_of_steps =int ( (end_time-start_time) / time_step )
    position_matrix = np.zeros((Nx,Ny,number_of_steps))
    length_matrix = np.zeros((Nx,Ny,number_of_steps))
    position_matrix [:,:,0]= grid
    length_matrix [:,:0] = 0 #arclength is 0
    for current_step in range (1,number_of_steps):
        for point in position_matrix[:,:(current_step-1)]
            newpoint,length = do_step(vector_field,point,time_step)
            position_matrix[x,y,currentstep] = newpoint
            length_matrix [x,y,currentstep] = length + length_matrix[x,y,current_step-1]
    
    result = length_matrix[:,:number_of_steps] #the last line has the length of all original grid points
    return result





