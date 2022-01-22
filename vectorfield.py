"""Implementation of an vectorfield.
"""


class Vectorfield:
    def __init__(self, spacing, grid_size, data, bounds, nComponents, field):
        self.spacing = spacing
        self.grid_size = grid_size
        self.data = data  # in which shape is our data supposed to be?
        self.bounds = bounds
        self.nComponents = nComponents
        self.field = field

    # in the provided example https://vcgitlab.iwr.uni-heidelberg.de/vcg-public/paraview_tutorial/-/blob/master/FlowMap/integrator/vector_field_and_integrator.h
    # there are 3 arrays, each discribing one component.
    # the field will arrive as a vtkImageData. Do we need to wrap it into a numpy array first to use. or do we wrap before calling the function.

    def mapGridToPhysicalSpace():
        pass

    def mapPhysicalSpacetoGrid():
        pass

    def isOutOfBounds_Grid():
        pass

    def isOutOfBounds_Physical():
        pass

    def buildIndexFromPosition():
        pass

    def buildIndexFromCoordinates():
        pass

    def buildCoordinatesFromIndex():
        pass

    # ADD ALL FUNCTIONS
