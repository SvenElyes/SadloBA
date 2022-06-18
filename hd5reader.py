import string
import h5py
import numpy as np
import argparse

import glob

"""
parser = argparse.ArgumentParser(description='input file name to be cleaned up')
parser.add_argument("-s","--string", type=str, required=True,
                    help='name of file')
                    
args = parser.parse_args()
filename = args.string"""

f0 = h5py.File("snapshot_000.hdf5", "r")
f1 = h5py.File("snapshot_1356.hdf5", "r")

header0 = f0["Header"]
ptype0 = f0["PartType0"]
header1 = f1["Header"]
ptype1 = f1["PartType0"]


pID0 = ptype0["ParticleIDs"]
"""
comp = ptype["CompositionType"]
coord = ptype["Coordinates"]
masses = ptype["Masses"]
vel = ptype["Velocities"]
"""
pChildID0 = ptype0["ParticleChildIDsNumber"]
piDGeneration0 = ptype0["ParticleIDGenerationNumber"]


pID1 = ptype1["ParticleIDs"]
pChildID1 = ptype1["ParticleChildIDsNumber"]
piDGeneration1 = ptype1["ParticleIDGenerationNumber"]


# check if both lists have only distinct elements.
print("len pid0", len(pID0), "len pid1", len(set(pID0)))
print("len pid1", len(pID1), "len pid1", len(set(pID1)))
if len(pID0) == len(set(pID0)):
    print("Distinct snapshot 0000")

if len(pID1) == len(set(pID1)):
    print("Distinct snapshot 1305")

if set(pID0) == set(pID1):
    print("Same Elements in both IDS")

# check if both lists have only distinct elements.
print("len pChildID0", len(pChildID0), "len pChildID0", len(set(pChildID0)))
print("len pChildID1", len(pChildID1), "len pChildID1", len(set(pChildID1)))

if len(pChildID0) == len(set(pChildID0)):
    print("Distinct children snapshot 0000")

if len(pChildID1) == len(set(pChildID1)):
    print("Distinct children snapshot 1305")

print(set(pChildID0), set(pChildID1))
if set(pChildID0) == set(pChildID1):
    print("Same children Elements in both IDS")


# check if both lists have only distinct elements.
print(
    "len piDGeneration0",
    len(piDGeneration0),
    "len piDGeneration0",
    len(set(piDGeneration0)),
)
print("len pChildID1", len(piDGeneration1), "len pChildID1", len(set(piDGeneration1)))

if len(piDGeneration0) == len(set(piDGeneration0)):
    print("Distinct children snapshot 0000")

if len(piDGeneration1) == len(set(piDGeneration1)):
    print("Distinct children snapshot 1305")

print(set(piDGeneration0), set(piDGeneration1))
if set(piDGeneration0) == set(piDGeneration1):
    print("Same children Elements in both IDS")
