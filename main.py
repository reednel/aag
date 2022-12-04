from sage.all import *
from sage.all import Integer
from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
# from sage.groups.braid import BraidGroup
# from sage.groups.matrix_gps.linear import GL

from aag import AAGExchangeObject

import itertools
import random
import time
from datetime import timedelta

def test(group_type, group_object, pk_length, sk_length):

    startTime = time.time()

    alice = AAGExchangeObject[group_type](group_object)
    bob = AAGExchangeObject[group_type](group_object)

    # choose random subset of bg to be publicKey
    alice.generatePublicKey(pk_length)
    bob.generatePublicKey(pk_length)

    # choose random subset-permutation of each publicKey to be privateKey
    alice.generatePrivateKey(sk_length)
    bob.generatePrivateKey(sk_length)

    # derive shared key
    aliceSharedKey = alice.deriveSharedKey(True, bob)
    bobSharedKey = bob.deriveSharedKey(False, alice)

    print("---------- ALICE ----------")
    print(alice._privateKey)
    print("-")
    print(aliceSharedKey)

    print("---------- BOB ----------")
    print(bob._privateKey)
    print("-")
    print(bobSharedKey)

    # If the key is a list, uncomment these lines to print Alice's and Bob's side by side
    #for a, b in zip(aliceSharedKey, bobSharedKey):
    #    ast = str(a).replace('\n','')
    #    bst = str(b).replace('\n','')
    #    print(f"Alice has {ast}, Bob has {bst}")

    endTime = time.time()
    elapsed = str(timedelta(seconds=((endTime - startTime))))
    print("\nTime:", elapsed)

    return (aliceSharedKey == bobSharedKey)

def main() -> int:
    # # HEISENBERG GROUP
    # # Note: let n be odd, R be prime
    # hg = HeisenbergGroup(n=Integer(3), R=Integer(7))
    # return test(HeisenbergGroup, hg, 23, 13)

    # Permutation Group
    pg = PermutationGroup([[(1,2,3),(4,5)],[(3,4)]]) # ,[(5,6,7),(8,9)]
    return test(PermutationGroup, pg, 11, 7)

    # # BRAID GROUP # BROKEN
    # bg = BraidGroup(names=("a","b","c"))
    # bg.random_element() # DEBUG
    # return test(BraidGroup, bg, 11, 7)

    # # LINEAR MATRIX GROUP # BROKEN
    # mg = GL(Integer(3), ZZ)
    # return test(GL, mg, 11, 7)


if __name__ == "__main__":
    tests = 1
    successes = [0 for i in range(tests)]
    for i in range(tests):
        print(f"---------- ITERATION {i} (random seed = {i}) ----------")
        random.seed(i)
        success = main()
        successes[i] = success

    print("\n---------- RESULTS ----------")
    for i, success in enumerate(successes):
        print(f"Seed {i}: {'pass' if success else 'fail'}")

    print(f"Success rate: {sum(successes) / len(successes) * 100}%")
