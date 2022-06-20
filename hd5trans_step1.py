import string
import h5py

import argparse

import glob

"""
parser = argparse.ArgumentParser(description='input file name to be cleaned up')
parser.add_argument("-s","--string", type=str, required=True,
                    help='name of file')
                    
args = parser.parse_args()
filename = args.string"""
for file in glob.glob("snapshots/*.hdf5"):
    print(file)
    print(type(file))

    filename = file
    f = h5py.File(filename, "r")
    header = f["Header"]
    ptype = f["PartType0"]
    print(list(ptype.keys()))

    pID = ptype["ParticleIDs"]
    comp = ptype["CompositionType"]
    coord = ptype["Coordinates"]
    masses = ptype["Masses"]
    vel = ptype["Velocities"]
    pChildID = ptype["ParticleChildIDsNumber"]
    filename = filename.split("/")[1]
    print(filename)
    """
    print("Particle IDs")
    print(list(pID.shape))
    print(pID[0:10])

    print("Composition Type")
    print(list(comp.shape))
    print(comp[0:10])


    print("Coordinates")
    print(list(coord.shape))
    print(coord[0:10])


    print("Masses")
    print(list(masses.shape))
    print(masses[0:10])


    print("vel")
    print(list(vel.shape))
    print(vel[0:10])


    print("pChildID")
    print(list(pChildID.shape))
    print(pChildID[0:10])
    """

    with h5py.File(f"cleansc/clean_{filename}", "w") as hf:
        hf.create_dataset("ParticleIDs", data=pID)
        hf.create_dataset("Coordinates", data=coord)
        hf.create_dataset("Velocities", data=vel)
        hf.create_dataset("Masses", data=masses)
