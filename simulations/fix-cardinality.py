import csv

from sage.all import *
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup

import sys
sys.path.append('..')
from src.compare import generate

# Warning: these parameters may require multiple days to complete.
def main():

    FILENAME = "fix-cardinality.csv"

    with open(FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["group", "pk", "sk", "exchange", "attack", "guesses", "cardinality"])
        f.flush()

    # S16
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [2], [4])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [8], [2])

    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [2], [6])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [8], [3])

    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [2], [8])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [8], [4])

    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [2], [10])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [8], [5])

    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [2], [12])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [8], [6])

    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [2], [14])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [8], [7])

    # Rubik's Cube
    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [2], [4])
    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [8], [2])

    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [2], [6])
    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [8], [3])

    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [2], [8])
    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [8], [4])

    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [2], [10])
    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [8], [5])

    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [2], [12])
    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [8], [6])

    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [2], [14])
    generate(FILENAME, CubeGroup, CubeGroup(16), "Rubik", 100, [8], [7])

if __name__ == "__main__":
    main()
