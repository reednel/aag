from sage.all import *
from sage.all import Integer
from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup
from sage.groups.braid import BraidGroup

from aag import AAGExchangeObject
from attack import bruteforce
import time
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np

from tqdm import tqdm

import csv

def timing(group_type, group_object, pk_length, sk_length):

    alice = AAGExchangeObject[group_type](group_object)
    bob = AAGExchangeObject[group_type](group_object)

    startExchangeTime = time.time()

    # choose random subset of bg to be publicKey
    alice.generatePublicKey(pk_length)
    bob.generatePublicKey(pk_length)

    # choose random subset-permutation of each publicKey to be privateKey
    alice.generatePrivateKey(sk_length)
    bob.generatePrivateKey(sk_length)

    # derive shared key
    aliceSharedKey = alice.deriveSharedKey(True, bob)
    bobSharedKey = bob.deriveSharedKey(False, alice)

    endExchangeTime = time.time()
    exchangeTime = timedelta(seconds=((endExchangeTime - startExchangeTime)))

    # Execute bruteforce attack
    atb = alice.transition(bob)
    bta = bob.transition(alice)
    startAttackTime = time.time()
    bfSharedKey = bruteforce(alice.publicKey, bob.publicKey, sk_length, atb, bta)
    endAttackTime = time.time()
    attackTime = timedelta(seconds=((endAttackTime - startAttackTime)))

    # Check correctness
    if (not (aliceSharedKey == bobSharedKey == bfSharedKey)):
        print("RUNTIME ERROR")
        print("\tAlice's K:", aliceSharedKey)
        print("\tBob's K  :", bobSharedKey)
        print("\tEve's K  :", bfSharedKey)

    return exchangeTime, attackTime

def generate_permutation():
    key_sizes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    s16 = [[(1,2)],[(1,3)],[(1,4)],[(1,5)],[(1,6)],[(1,7)],[(1,8)],[(1,9)],[(1,10)],[(1,11)],[(1,12)],[(1,13)],[(1,14)],[(1,15)],[(1,16)]]

    pg = PermutationGroup(s16)

    NUMBER_OF_POINTS = 100

    with open('simulations/permutation_all2.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["pk", "sk", "exchange", "attack"])

        for pub in tqdm(key_sizes, desc='Public', position=0):
            for priv in tqdm(range(1, pub), desc='Private', leave=False, position=1):
                if pub >= priv:
                    for i in tqdm(range(NUMBER_OF_POINTS), leave=False, desc='Points', position=2):
                        pgExchangeTime, pgAttackTime = timing(PermutationGroup, pg, pub, priv)
                        writer.writerow([pub, priv, pgExchangeTime.microseconds, pgAttackTime.microseconds])
                        f.flush()


def generate_permutation_many():
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

        for group, group_name in tqdm(zip(groups, group_names), desc='Groups', position=0):
            pub = pk_size
            for priv in tqdm(sk_sizes, desc='Private', leave=False, position=1):
                if pub >= priv:
                    for i in tqdm(range(NUMBER_OF_POINTS), leave=False, desc='Points', position=2):
                        pgExchangeTime, pgAttackTime = timing(PermutationGroup, group, pub, priv)
                        writer.writerow([group_name, pub, priv, pgExchangeTime.microseconds, pgAttackTime.microseconds, group.cardinality()])
                        f.flush()

def generate_cube():
    counter = 0.00
    public = [10,20,30,40,50]
    private = [10,20,30,40,50]
    constant_public = 60
    constant_private =  10
    cube = CubeGroup()

    arr = np.array([[0,0,0,0]])
    for pub in public:
        for i in range(20):
            cube = CubeGroup()
            cubeExchangeTime, cubeAttackTime = timing(CubeGroup, cube, pub, constant_private)
            arr = np.append(arr, [[cubeExchangeTime.microseconds, cubeAttackTime.microseconds, pub, constant_private]], axis=0)
            counter = counter + 1
            print(arr)
            print(counter / 300.00, '% done', sep='')
    for priv in private:
        for i in range(20):
            cube = CubeGroup()
            cubeExchangeTime, cubeAttackTime = timing(CubeGroup, cube, constant_public, priv)
            arr = np.append(arr, [[cubeExchangeTime.microseconds, cubeAttackTime.microseconds, constant_public, priv]], axis=0)
            counter = counter + 1
            print(counter / 300.00, '% done', sep='')
    print(arr)
    arr.tofile('simulations/cube.csv', sep = ',')

def generate_braid():
    counter = 0.00
    public = [10,20,30,40,50]
    private = [10,20,30,40,50]
    constant_public = 60
    constant_private =  10
    braid = BraidGroup(5)

    arr = np.array([[0,0,0,0]])
    for pub in public:
        for i in range(3):
            braidExchangeTime, braidAttackTime = timing(BraidGroup, braid, pub, constant_private)
            arr = np.append(arr, [[braidExchangeTime.microseconds, braidAttackTime.microseconds, pub, constant_private]], axis=0)
            counter = counter + 1
            print(arr)
            print(counter / 300.00, '% done', sep='')
    for priv in private:
        for i in range(3):
            braidExchangeTime, braidAttackTime = timing(BraidGroup, braid, constant_public, priv)
            arr = np.append(arr, [[braidExchangeTime.microseconds, braidAttackTime.microseconds, constant_public, priv]], axis=0)
            counter = counter + 1
            print(counter / 300.00, '% done', sep='')
    print(arr)
    arr.tofile('simulations/braid.csv', sep = ',')

def generate_heisenberg():
    counter = 0.00
    public = [10,20,30,40,50]
    private = [10,20,30,40,50]
    constant_public = 60
    constant_private =  10
    hg = HeisenbergGroup(n=Integer(5), R=Integer(10000))

    arr = np.array([[0,0,0,0]])
    for pub in public:
        for i in range(3):
            hgExchangeTime, hgAttackTime = timing(HeisenbergGroup, hg, pub, constant_private)
            arr = np.append(arr, [[hgExchangeTime.microseconds, hgAttackTime.microseconds, pub, constant_private]], axis=0)
            counter = counter + 1
            print(arr)
            print(counter / 300.00, '% done', sep='')
    for priv in private:
        for i in range(3):
            hgExchangeTime, hgAttackTime = timing(HeisenbergGroup, hg, constant_public, priv)
            arr = np.append(arr, [[hgExchangeTime.microseconds, hgAttackTime.microseconds, constant_public, priv]], axis=0)
            counter = counter + 1
            print(counter / 300.00, '% done', sep='')
    print(arr)
    arr.tofile('simulations/braid.csv', sep = ',')

def main():
    # hg = HeisenbergGroup(n=Integer(5), R=Integer(10000))

    #generate_permutation()
    generate_permutation_many()
    #generate_braid()

        #plt.scatter(pg2ExchangeTime.microseconds, pg2AttackTime.microseconds, s=30, c='red')
    # bg = BraidGroup(5)
    # bgExchangeTime, bgAttackTime = timing(BraidGroup, bg, 11, 7)

    # rg = CubeGroup()
    # rgExchangeTime, rgAttackTime = timing(CubeGroup, rg, 11, 7)

    #plt.scatter(pgExchangeTime.microseconds, pgAttackTime.microseconds, s=30, c='red')
    #plt.text(pgXPlot, pgYPlot, "Permutation Group")
    #plt.scatter(pg2ExchangeTime.microseconds, pg2AttackTime.microseconds, s=30, c='red')
    #plt.title("Permutation Group")
    #plt.ylabel("Attack Time (μ)")
    #maybe plot with logorithmic scale
    #plt.xlabel("Exchange Time (μ)")
    #plt.savefig("test.png", format='png')



if __name__ == "__main__":
    main()