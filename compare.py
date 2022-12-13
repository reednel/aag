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
    counter = 0.00
    public = [1,2,3,4,5]
    private = [1,2,3,4,5]
    constant_public = 5
    constant_private = 5
    s16 = [[(1,2)],[(1,3)],[(1,4)],[(1,5)],[(1,6)],[(1,7)],[(1,8)],[(1,9)],[(1,10)],[(1,11)],[(1,12)],[(1,13)],[(1,14)],[(1,15)],[(1,16)]]
    pg = PermutationGroup(s16)
    #pgExchangeTime, pgAttackTime = timing(PermutationGroup, pg, 23, 13)

    #pgXPlot = pgExchangeTime.microseconds + 3
    #pgYPlot = pgAttackTime.microseconds + 3


    pg2 = PermutationGroup(s16)
    #pg2ExchangeTime, pg2AttackTime = timing(PermutationGroup, pg2, 23, 13)
    #pg2XPlot = pg2ExchangeTime.microseconds + 3
    #pg2YPlot = pg2AttackTime.microseconds + 3

    NUMBER_OF_POINTS = 200

    arr = np.array([[0,0,0,0]])
    for pub in public:
        for i in tqdm(range(NUMBER_OF_POINTS)):
            pg2 = PermutationGroup(s16)
            pg2ExchangeTime, pg2AttackTime = timing(PermutationGroup, pg2, pub, constant_private)
            arr = np.append(arr, [[pg2ExchangeTime.microseconds, pg2AttackTime.microseconds, pub, constant_private]], axis=0)
            counter = counter + 1
    for priv in private:
        for i in tqdm(range(NUMBER_OF_POINTS)):
            pg2 = PermutationGroup(s16)
            pg2ExchangeTime, pg2AttackTime = timing(PermutationGroup, pg2, constant_public, priv)
            arr = np.append(arr, [[pg2ExchangeTime.microseconds, pg2AttackTime.microseconds, constant_public, priv]], axis=0)

    print(arr)
    arr.tofile('AttackExchangeData.csv', sep = ',')

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
    arr.tofile('CubeAttackExchangeData.csv', sep = ',')

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
    arr.tofile('BraidAttackExchangeData.csv', sep = ',')

def main():
    # hg = HeisenbergGroup(n=Integer(5), R=Integer(10000))

    generate_permutation()
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