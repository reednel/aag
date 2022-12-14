from sage.all import *
from sage.all import Integer
from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup
from sage.groups.braid import BraidGroup

from aag import AAGExchangeObject
from attack import bruteforce

import itertools
import random
import time
from datetime import timedelta

def test(group_type, group_object, pk_length, sk_length):

    alice = AAGExchangeObject[group_type](group_object)
    bob = AAGExchangeObject[group_type](group_object)

    startTime = time.time()

    # choose random subset of bg to be publicKey
    alice.generatePublicKey(pk_length)
    bob.generatePublicKey(pk_length)

    # choose random subset-permutation of each publicKey to be privateKey
    alice.generatePrivateKey(sk_length)
    bob.generatePrivateKey(sk_length)

    # # Keep for future debugging
    # alice.publicKey = [PermutationGroupElement([(2,4,5)]), PermutationGroupElement([(3,5)]), PermutationGroupElement([(1,2,5),(3,4)])]
    # bob.publicKey = [PermutationGroupElement([(1,4,3,5)]), PermutationGroupElement([(1,5,4,2)]), PermutationGroupElement([(1,3,2,4,5)])]
    # alice.setPrivateKey(PermutationGroupElement([(1,2,5),(3,4)]))
    # bob.setPrivateKey(PermutationGroupElement([(1,2,4,5)]))

    # derive shared key
    aliceSharedKey = alice.deriveSharedKey(True, bob)
    bobSharedKey = bob.deriveSharedKey(False, alice)

    # print("ALICE:")
    # print(aliceSharedKey)
    # print("BOB:")
    # print(bobSharedKey)

    endTime = time.time()
    elapsed = str(timedelta(seconds=((endTime - startTime))))
    print("Exchange Time:", elapsed)

    # Attack
    atb = alice.transition(bob)
    bta = bob.transition(alice)
    bfSharedKey = bruteforce(alice.publicKey, bob.publicKey, sk_length, atb, bta)

    return (aliceSharedKey == bobSharedKey == bfSharedKey == alice.oracle(bob))

def main() -> int:
    # # HEISENBERG GROUP
    # # Note: let n be odd
    # hg = HeisenbergGroup(n=Integer(3), R=Integer(sys.maxsize))
    # return test(HeisenbergGroup, hg, 3, 3)

    # PERMUTATION GROUP
    # Note: a Permutation group with generators of the form (1 2),(1 3),...,(1 n) is the Symmetric group S_n
    PERMSIZE = 16
    Sn = [[(0, i)] for i in range(PERMSIZE)]
    pg = PermutationGroup(Sn)
    return test(PermutationGroup, pg, 10, 5)

    # # RUBIK'S CUBE GROUP
    # rg = CubeGroup()
    # return test(CubeGroup, rg, 11, 7)

    # # BRAID GROUP
    # strands = ["s" + str(i) for i in range(80)]
    # bg = BraidGroup(names=strands)
    # return test(BraidGroup, bg, 4, 2)


if __name__ == "__main__":
    tests = 5
    successes = [0 for i in range(tests)]
    for i in range(tests):
        print(f"\n---------- ITERATION {i} (random seed = {i}) ----------")
        random.seed(i)
        success = main()
        successes[i] = success

    print("\n---------- RESULTS ----------")
    for i, success in enumerate(successes):
        print(f"Seed {i}: {'pass' if success else 'fail'}")

    print(f"Success rate: {sum(successes) / len(successes) * 100}%")
