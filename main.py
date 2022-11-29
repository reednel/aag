from sage.all import *
from aag import AAGExchangeObject

from sage.groups.braid import BraidGroup, Braid

import itertools

def main():
    bg = BraidGroup(3)
    alice = AAGExchangeObject[bg]()
    bob = AAGExchangeObject[bg]()

    # choose random subset of bg to be publicKey
    alice.publicKey: set[Braid] = {bg.random_element() for _ in range(3)}
    bob.publicKey: set[Braid] = {bg.random_element() for _ in range(3)}

    # choose random permutation of each publicKey to be privateKey
    alice.privateKey: list[Braid] = random.shuffle(list(alice.publicKey))[:2]
    bob.privateKey: list[Braid] = random.shuffle(list(bob.publicKey))[:2]

    # derive shared key
    aliceSharedKey = alice.deriveSharedKey(bob)
    bobSharedKey = bob.deriveSharedKey(alice)

    print(aliceSharedKey)
    print(bobSharedKey)

if __name__ == "__main__":
    main()