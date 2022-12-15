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
    exchangeTime = (endExchangeTime - startExchangeTime) / 1000000

    # Execute bruteforce attack
    atb = alice.transition(bob)
    bta = bob.transition(alice)
    startAttackTime = time.time_ns()
    bfSharedKey = bruteforce(alice.publicKey, bob.publicKey, sk_length, atb, bta)
    endAttackTime = time.time_ns()
    attackTime = (endAttackTime - startAttackTime) / 1000000

    # Check correctness
    if (not (aliceSharedKey == bobSharedKey == bfSharedKey)):
        print("RUNTIME ERROR")
        print("\tAlice's K:", aliceSharedKey)
        print("\tBob's K  :", bobSharedKey)
        print("\tEve's K  :", bfSharedKey)

    return exchangeTime, attackTime

def generate_permutation():
    key_sizes = [1,2,3,4,5]
    PERMSIZE = 16
    Sn = [[(0, i)] for i in range(PERMSIZE)]
    pg = PermutationGroup(Sn)

    NUMBER_OF_POINTS = 3

    with open('simulations/permutation.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerow(["pk", "sk", "exchange", "attack"])

        for pub in tqdm(key_sizes, desc='Public', position=0):
            for priv in tqdm(range(1, pub), desc='Private', leave=False, position=1):
                if pub >= priv:
                    for i in tqdm(range(NUMBER_OF_POINTS), leave=False, desc='Points', position=2):
                        exchangeTime, attackTime = timing(PermutationGroup, pg, pub, priv)
                        writer.writerow([pub, priv, exchangeTime, attackTime])
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
    generate_permutation()
    # generate_cube()
    # generate_braid()
    # generate_heisenberg()


if __name__ == "__main__":
    main()