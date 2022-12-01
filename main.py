from sage.all import *
from aag import AAGExchangeObject

from sage.groups.matrix_gps.heisenberg import HeisenbergGroup

import itertools

def main():
    hg = HeisenbergGroup(n=Integer(1), R=Integer(2))
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


    #for a, b in zip(aliceSharedKey, bobSharedKey):
    #    ast = str(a).replace('\n','')
    #    bst = str(b).replace('\n','')
    #    print(f"Alice has {ast}, Bob has {bst}")

    assert(aliceSharedKey == bobSharedKey)


if __name__ == "__main__":
    main()