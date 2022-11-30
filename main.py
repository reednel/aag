from sage.all import *
from aag import AAGExchangeObject

from sage.groups.matrix_gps.heisenberg import HeisenbergGroup

import itertools

def main():
    hg = HeisenbergGroup(n=Integer(1), R=Integer(13))
    alice = AAGExchangeObject[HeisenbergGroup](hg)
    bob = AAGExchangeObject[HeisenbergGroup](hg)

    # choose random subset of bg to be publicKey
    alice.generatePublicKey(5)
    bob.generatePublicKey(5)

    # choose random subset-permutation of each publicKey to be privateKey
    alice.generatePrivateKey(3)
    bob.generatePrivateKey(3)

    # derive shared key
    aliceSharedKey = alice.deriveSharedKey(bob)
    bobSharedKey = bob.deriveSharedKey(alice)

    print(aliceSharedKey)
    print(bobSharedKey)

if __name__ == "__main__":
    main()