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