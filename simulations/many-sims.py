import csv

from sage.all import *
from sage.all import Integer
from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup
from sage.groups.braid import BraidGroup

import sys
sys.path.append('..')
from compare import generate

# Warning: these parameters may require multiple days to complete.
def main():

    FILENAME = "many-sims.csv"

    with open(FILENAME, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["group", "pk", "sk", "exchange", "attack", "guesses", "cardinality"])
        f.flush()

    generate(FILENAME, PermutationGroup, SymmetricGroup(8), "S8", 10, [5], [1, 2, 3, 4, 5, 6, 7])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 100, [1,2,3,4,5], [1,2,3,4,5])
    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 25, [5], [6,7,8,9,10,11,12])

    generate(FILENAME, CubeGroup, CubeGroup(), "Rubik", 25, [1,2,3,4,5], [1, 2, 3, 4, 5])
    generate(FILENAME, CubeGroup, CubeGroup(), "Rubik", 25, [5], [1, 2, 3, 4, 5, 6, 7])

    generate(FILENAME, QuaternionGroup, QuaternionGroup(), "Quaternion", 25, [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6])

    generate(FILENAME, HeisenbergGroup, HeisenbergGroup(n=5, R=Integer(sys.maxsize)), "Heisenberg5", 25, [4,5,6,7], [1, 2, 3, 4, 5, 6])

    generate(FILENAME, BraidGroup, BraidGroup(2), "Braid2", 3, [1,2,3,4,5], [1, 2, 3, 4, 5])
    generate(FILENAME, BraidGroup, BraidGroup(3), "Braid3", 3, [1,2,3,4,5], [1, 2, 3, 4, 5])
    generate(FILENAME, BraidGroup, BraidGroup(3), "Braid3", 3, [5], [6,7,8,9,10])
    generate(FILENAME, BraidGroup, BraidGroup(4), "Braid4", 3, [1,2,3,4], [1,2,3,4])
    generate(FILENAME, BraidGroup, BraidGroup(5), "Braid5", 3, [5], [1, 2, 3, 4, 5])

    generate(FILENAME, PermutationGroup, SymmetricGroup(16), "S16", 3, [1,2,3,4,5,6,7,8,9,10], [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])


if __name__ == "__main__":
    main()
