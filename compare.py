from sage.all import *
from sage.all import Integer
from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup
from sage.groups.braid import BraidGroup

from aag import AAGExchangeObject
from attack import bruteforce
import time

import numpy as np

from tqdm import tqdm

import csv

def timing(group_type, group_object, pk_length, sk_length):
    alice = AAGExchangeObject[group_type](group_object)
    bob = AAGExchangeObject[group_type](group_object)

    startExchangeTime = time.time_ns()

    # choose random subset of bg to be publicKey
    alice.generatePublicKey(pk_length)
    bob.generatePublicKey(pk_length)

    # choose random subset-permutation of each publicKey to be privateKey
    alice.generatePrivateKey(sk_length)
    bob.generatePrivateKey(sk_length)

    # derive shared key
    aliceSharedKey = alice.deriveSharedKey(True, bob)
    bobSharedKey = bob.deriveSharedKey(False, alice)

    endExchangeTime = time.time_ns()
    exchangeTime = (endExchangeTime - startExchangeTime) / 1000000 # to ms

    # Execute bruteforce attack
    atb = alice.transition(bob)
    bta = bob.transition(alice)
    startAttackTime = time.time_ns()
    bfSharedKey, guesses = bruteforce(alice.publicKey, bob.publicKey, sk_length, atb, bta)
    endAttackTime = time.time_ns()
    attackTime = (endAttackTime - startAttackTime) / 1000000 # to ms

    # Check correctness
    if (not (aliceSharedKey == bobSharedKey == bfSharedKey)):
        print("RUNTIME ERROR")
        print("\tAlice's K:", aliceSharedKey)
        print("\tBob's K  :", bobSharedKey)
        print("\tEve's K  :", bfSharedKey)

    return exchangeTime, attackTime, guesses

def generate(group_type, group, group_name, number_of_points, public_sizes, private_sizes):
    with open('simulations/all.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        for pub in tqdm(public_sizes, desc='Public',leave=False, position=1):
            for priv in tqdm(private_sizes, desc='Private', leave=False, position=2):
                for _ in tqdm(range(number_of_points), leave=False, desc='Points', position=3):
                    exchangeTime, attackTime, guesses = timing(group_type, group, pub, priv)
                    writer.writerow([group_name, pub, priv, exchangeTime, attackTime, guesses, group.cardinality()])
                    f.flush()

def generate_permutation():
    public_sizes = [5]
    private_sizes = [1,2,3,4,5]

    pg = SymmetricGroup(16)

    NUMBER_OF_POINTS = 3

    with open('simulations/permutation.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["pk", "sk", "exchange", "attack"])

        for pub in tqdm(public_sizes, desc='Public', position=0):
            for priv in tqdm(private_sizes, desc='Private', leave=False, position=1):
                if pub >= priv:
                    for _ in tqdm(range(NUMBER_OF_POINTS), leave=False, desc='Points', position=2):
                        exchangeTime, attackTime = timing(PermutationGroup, pg, pub, priv)
                        writer.writerow([pub, priv, exchangeTime, attackTime])
                        f.flush()


def generate_permutation_many():
    public_sizes = [5]
    private_sizes = [1,2,3,4,5]
    sk_sizes = [1,2,3,4,5]
    pk_size = 6

    #cube = PermutationGroup(["(3,2,6,7)(4,1,5,8)", "(1,2,6,5)(4,3,7,8)", "(1,2,3,4)(5,6,7,8)"])
    #s16 = PermutationGroup([[(1,2)],[(1,3)],[(1,4)],[(1,5)],[(1,6)],[(1,7)],[(1,8)],[(1,9)],[(1,10)],[(1,11)],[(1,12)],[(1,13)],[(1,14)],[(1,15)],[(1,16)]])
    s3 = SymmetricGroup(3)
    s4 = SymmetricGroup(4)
    s5 = SymmetricGroup(5)
    s6 = SymmetricGroup(6)
    s7 = SymmetricGroup(7)
    s8 = SymmetricGroup(8)
    d5 = DihedralGroup(5)
    d6 = DihedralGroup(6)
    d7 = DihedralGroup(7)

    groups = [s3, s4, s5, s6, s7, s8, d5, d6, d7]
    group_names = ["s3", "s4", "s5", "s6", "s7", "s8", "d5", "d6", "d7"]

    NUMBER_OF_POINTS = 25

    with open('simulations/many_groups.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["group", "pk", "sk", "exchange", "attack", "cardinality"])
        for group, group_name in tqdm(zip(groups, group_names), position=0, desc='Groups'):
            pg = group
            pg_type = PermutationGroup
            for pub in tqdm(public_sizes, desc='Public',leave=False, position=1):
                for priv in tqdm(private_sizes, desc='Private', leave=False, position=2):
                    if pub >= priv:
                        for _ in tqdm(range(NUMBER_OF_POINTS), leave=False, desc='Points', position=3):
                            exchangeTime, attackTime = timing(pg_type, pg, pub, priv)
                            writer.writerow([group_name, pub, priv, exchangeTime, attackTime, group.cardinality()])
                            f.flush()

def generate_cube():
    counter = 0.00
    public = [1,2,3,4,5]
    private = private = [1,2,3,4,5]
    constant_public = 10
    constant_private =  5
    cube = CubeGroup()

    arr = np.array([[0,0,0,0]])
    # for pub in public:
    #     for i in range(20):
    #         cube = CubeGroup()
    #         cubeExchangeTime, cubeAttackTime = timing(CubeGroup, cube, pub, constant_private)
    #         arr = np.append(arr, [[cubeExchangeTime.microseconds, cubeAttackTime.microseconds, pub, constant_private]], axis=0)
    #         counter = counter + 1
    #         print(arr)
    #         print(counter / 300.00, '% done', sep='')
    for priv in private:
        for _ in range(1):
            cube = CubeGroup()
            cubeExchangeTime, cubeAttackTime = timing(CubeGroup, cube, constant_public, priv)
            arr = np.append(arr, [[cubeExchangeTime.microseconds, cubeAttackTime.microseconds, constant_public, priv]], axis=0)
    #         counter = counter + 1
    #         print(counter / 300.00, '% done', sep='')
    # print(arr)
    arr.tofile('simulations/cube.csv', sep = ',')

def generate_braid():
    counter = 0.00
    public = [1,2,3,4,5]
    private = [1,2,3,4,5]
    constant_public = 10
    constant_private = 5
    braid = BraidGroup(5)

    arr = np.array([[0,0,0,0]])
    # for pub in public:
    #     for i in range(3):
    #         braidExchangeTime, braidAttackTime = timing(BraidGroup, braid, pub, constant_private)
    #         arr = np.append(arr, [[braidExchangeTime.microseconds, braidAttackTime.microseconds, pub, constant_private]], axis=0)
    #         counter = counter + 1
    #         print(arr)
    #         print(counter / 300.00, '% done', sep='')
    for priv in private:
        for _ in range(3):
            braidExchangeTime, braidAttackTime = timing(BraidGroup, braid, constant_public, priv)
            arr = np.append(arr, [[braidExchangeTime.microseconds, braidAttackTime.microseconds, constant_public, priv]], axis=0)
    #         counter = counter + 1
    #         print(counter / 300.00, '% done', sep='')
    # print(arr)
    arr.tofile('simulations/braid.csv', sep = ',')

def generate_heisenberg():
    counter = 0.00
    public = [10,20,30,40,50]
    private = [1,2,3,4,5]
    constant_public = 5
    constant_private =  10
    hg = HeisenbergGroup(n=Integer(3), R=Integer(sys.maxsize))

    arr = np.array([[0,0,0,0]])
    # for pub in public:
    #     for i in range(3):
    #         hgExchangeTime, hgAttackTime = timing(HeisenbergGroup, hg, pub, constant_private)
    #         arr = np.append(arr, [[hgExchangeTime.microseconds, hgAttackTime.microseconds, pub, constant_private]], axis=0)
    #         counter = counter + 1
    #         print(arr)
    #         print(counter / 300.00, '% done', sep='')
    for priv in private:
        for _ in range(3):
            hgExchangeTime, hgAttackTime = timing(HeisenbergGroup, hg, constant_public, priv)
            arr = np.append(arr, [[hgExchangeTime, hgAttackTime, constant_public, priv]], axis=0)
            # counter = counter + 1
            # print(counter / 300.00, '% done', sep='')
    # print(arr)
    arr.tofile('simulations/heisenberg.csv', sep = ',')

def main():
    #writer.writerow(["group", "pk", "sk", "exchange", "attack", "guesses", "cardinality"])

    #generate(PermutationGroup, SymmetricGroup(8), "S8", 10, [5], [1, 2, 3, 4, 5, 6, 7])
    #generate(PermutationGroup, SymmetricGroup(16), "S16", 10, [5], [1, 2, 3, 4, 5, 6, 7])
    #generate(CubeGroup, CubeGroup(), "Rubik", 15, [5], [1, 2, 3, 4, 5])
    #generate(CubeGroup, CubeGroup(), "Rubik", 5, [5], [6, 7])
    #generate(PermutationGroup, SymmetricGroup(8), "S8", 15, [5], [6, 7])
    #generate(BraidGroup, BraidGroup(5), "Braid5", 3, [5], [1, 2, 3, 4, 5])

    #generate(BraidGroup, BraidGroup(2), "Braid2", 3, [5], [1, 2, 3, 4, 5])
    #generate(BraidGroup, BraidGroup(3), "Braid3", 3, [5], [1, 2, 3, 4, 5])
    #generate(BraidGroup, BraidGroup(4), "Braid4", 3, [5], [1, 2, 3, 4, 5]) # dnf

    generate(QuaternionGroup, QuaternionGroup(), "Quaternion", 50, [5], [1, 2, 3, 4, 5])
    
    #generate_permutation()
    # generate_cube()
    # generate_braid()
    # generate_heisenberg()


if __name__ == "__main__":
    main()
