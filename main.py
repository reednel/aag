from sage.all import *
from sage.all import Integer
from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup
from sage.groups.braid import BraidGroup

from src.aag import AAGExchangeObject
from src.attack import bruteforce

import random
import time

def test(group_type, group_object, pk_length, sk_length):

    # EXCHANGE #

    # Set up exchange objects (fixing the platform)
    alice = AAGExchangeObject[group_type](group_object)
    bob = AAGExchangeObject[group_type](group_object)

    startExchangeTime = time.time_ns()

    # Choose public keys
    alice.generatePublicKey(pk_length)
    bob.generatePublicKey(pk_length)
    # Choose private keys
    alice.generatePrivateKey(sk_length)
    bob.generatePrivateKey(sk_length)
    # Derive shared keys
    aliceSharedKey = alice.deriveSharedKey(True, bob)
    bobSharedKey = bob.deriveSharedKey(False, alice)

    endExchangeTime = time.time_ns()
    exchangeTime = (endExchangeTime - startExchangeTime) / 1000000 # to ms
    print("Exchange Time:", exchangeTime)

    # ATTACK #

    atb = alice.transition(bob)
    bta = bob.transition(alice)

    startAttackTime = time.time_ns()

    bfSharedKey, guesses = bruteforce(alice.publicKey, bob.publicKey, sk_length, atb, bta)

    endAttackTime = time.time_ns()
    attackTime = (endAttackTime - startAttackTime) / 1000000 # to ms
    print("Attack Time:", attackTime)

    return (aliceSharedKey == bobSharedKey == bfSharedKey == alice.oracle(bob))

def main() -> int:
    # # HEISENBERG GROUP
    # # Note: let n be odd
    # hg = HeisenbergGroup(n=Integer(3), R=Integer(sys.maxsize))
    # return test(HeisenbergGroup, hg, 3, 3)

    # PERMUTATION GROUP
    PERMSIZE = 16
    Sn = [[(0, i)] for i in range(PERMSIZE)]
    pg = PermutationGroup(Sn)
    return test(PermutationGroup, pg, 10, 4)

    # # RUBIK'S CUBE GROUP
    # rg = CubeGroup()
    # test(CubeGroup, rg, 3, 4)

    # # BRAID GROUP
    # BRAIDSIZE = 5
    # strands = ["s" + str(i) for i in range(BRAIDSIZE)]
    # bg = BraidGroup(names=strands)
    # return test(BraidGroup, bg, 3, 3)


if __name__ == "__main__":
    tests = 5
    successes = [0 for _ in range(tests)]
    for i in range(tests):
        print(f"\n---------- ITERATION {i} ----------")
        random.seed(i)
        success = main()
        successes[i] = success

    print("\n---------- RESULTS ----------")
    for i, success in enumerate(successes):
        print(f"Seed {i}: {'pass' if success else 'fail'}")
