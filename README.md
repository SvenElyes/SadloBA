# SadloBA
Bachelor Arbeit bei Prof. Sadlo https://vcg.iwr.uni-heidelberg.de/people/sadlo/

# First Project

Erstes Ziel ist mit paraview vertraut zu werden. Dafuer ein kleines Plugin(?) schreiben dass sich die zeitliche Entwicklung von  Partikel betrachtet. Als Input wuerden wir ein Vektorfeld (uniform equidistanzes Grid) nehmen. In paraview wird das in der Klasse Imagedata realisiert.  Der Output ist die Laenge der Pfade, die die Partikel in einer gewissen Zeit zuruecklegen. Dies wird in einem Skalarfeld ausgegeben. Wahrscheinlich nehmen wir hier auch die Imagedata Klasse in Paraview.

# Literature

Lagrangian descriptor: https://www.sciencedirect.com/science/article/pii/S1007570413002037
How to write a Plugin: https://github.com/CGAL/cgal-paraview-plugins
Example of vectorfields : https://github.com/champsproject/ldds/blob/develop/ldds/testing_scripts.py

# Strategy
1. Programming a LD in python.
2. Try implementing it in paraview
3. Try programming in C++

# Questions
What is a standalone? https://vcgitlab.iwr.uni-heidelberg.de/vcg-public/paraview-vtk-template


 It's pretty late, but looping on numpy array is usually expensive because python interpreter and numpy code have to exchange the data every time the loop is executed



# HDF5

The simulation data is given in HDF5 format and can be found here:
https://www.dropbox.com/sh/ufwxaa19vs1xb9p/AABdAg7qD1CtFUGtRS7uN-7Na?dl=0

There are trouble loading the files directly into paraview as their strucutre is nested.
Thus first the files have to be transformed via following python scripts:

hd5trans_step1.py (link this) : 
Will look in the "snapshots" directory and will find all files with ending with .hdf5.
Will then create new .hdf5 files in a subdirectory called cleansc. The files will have following structure : clean_{filename}.
In the meantime will only have those arrays ParticleIDs ,Coordinates, Velocities, Masses

hd5trans_step2.py (link this):

Will take all .hdf5 files from the /cleansc subdirectoy and uses the pyevtk library(link this) to create file with an unstructerd grid file format.
In additiona  new array is introduced under the name next_position, in which the position of the particle at the following time step is also recorded.

hd5trans_step3.py (link this):
Not in the state to be used. Attempts to also add an arrayh with the previous coordintes.

test4.py (link this):

test to show how plugins work. Maybe remove this.



# PLUGINs

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

Clump.py

First, load in the group of simulation snapshots created with the hdf5 python scripts

To reduce computational time, the anaylzation will only partake on a small subset of points.
First all N (this is variable and can be changed) neigbors will be computed and their ID will be saved in the "neighbors" data Field.
Then the center point of those neighbors is being computed and saved in an arary called "center"


Centerpointanalysis.py

Has to be called on top of the Clump filter.

Takes the center array, computed in the clump filter and tries to compute its evolution over time.

First approach:
every x time steps the center point is saved and then, in the following timesteps until the new center is set again, the distance between the saved center and the new center is computed and written in the Data Array "distance"

FTLEApprox.py
Has to becalled after Clump Filter
FTLE ~~ 1/T * log A/h are we trying to compute. With h being the distance from a point to its nth neighbor at time step t0 and A being the distance between the nth neigbar and the point at time tn. T is the number of time steps.
The n (whcih neighbor) is variable.