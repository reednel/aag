from sage.all import *
from aag import AAGExchangeObject
import random

from sage.groups.matrix_gps.heisenberg import HeisenbergGroup

import itertools

def main() -> int:
    hg = HeisenbergGroup(n=Integer(3), R=Integer(2))
    alice = AAGExchangeObject[HeisenbergGroup](hg)
    bob = AAGExchangeObject[HeisenbergGroup](hg)

    # choose random subset of bg to be publicKey
    alice.generatePublicKey(3)
    bob.generatePublicKey(3)

    # choose random subset-permutation of each publicKey to be privateKey
    alice.generatePrivateKey(2)
    bob.generatePrivateKey(2)

    # derive shared key
    aliceSharedKey = alice.deriveSharedKey(True, bob)
    bobSharedKey = bob.deriveSharedKey(False, alice)

    print("---------- ALICE ----------")
    print(aliceSharedKey)

    print("---------- BOB ----------")
    print(bobSharedKey)

    # If the key is a list, uncomment these lines to print Alice's and Bob's side by side

    #for a, b in zip(aliceSharedKey, bobSharedKey):
    #    ast = str(a).replace('\n','')
    #    bst = str(b).replace('\n','')
    #    print(f"Alice has {ast}, Bob has {bst}")

    return (aliceSharedKey == bobSharedKey)


if __name__ == "__main__":
    successes = [0 for i in range(10)]
    for i in range(10):
        print(f"---------- ITERATION {i} (random seed = {i}) ----------")
        random.seed(i)
        success = main()
        successes[i] = success
    
    for i, success in enumerate(successes):
        print(f"Seed {i}: {'pass' if success else 'fail'}")

    print(f"Success rate: {sum(successes) / len(successes) * 100}%")

