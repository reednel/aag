from sage.all import *
from sage.all import Integer
from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup
from sage.groups.braid import BraidGroup

from src.aag import AAGExchangeObject

import itertools
import random
import time
from datetime import timedelta

import cowsay
from cowsay import generate_bubble

import os

def backward_foxsay(speech: str) -> None:
    backwards_fox = r"""
                    /
                   /
       Alice      /
  `~~,_____,,|\_/|
 }}~`(     ~~(.".)
 }}~ //~---\ /\o/
  }~ \\_    \\_
"""
    print('\n'.join(generate_bubble(speech)), end='')
    print(backwards_fox)

def pause():
    tmp = input()
    if tmp == 'q':
        exit()
    elif tmp == 'f':
        os.system('clear')
        print("""
        Here we have demonstrated a generic implementation of the AAG protocol that can work
        with any group. We have shown implementations for...

        • The Heisenberg group, of upper-triangular matrices of a certain form

        • Arbitrary permutation groups

        • The braid group, with an arbitrary number of strands

        • The Rubik's cube group

        Our paper will focus on comparing the performance of the AAG protocol between these groups.""")
        pause()
        exit()


def animate(group_type, group_object, pk_length, sk_length):
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

    endTime = time.time()
    elapsed = str(timedelta(seconds=((endTime - startTime))))

    os.system('clear')
    pause()
    os.system('clear')

    backward_foxsay("Psst! Bob! Let's go get dumplings on TUESDAY at 8 PM!")
    pause()
    cowsay.cow("Ok Alice, see you there! That sounds delicious!")

    pause()
    os.system('clear')

    cowsay.trex("HAHAHA! See you there! That sounds delicious!")

    pause()
    os.system('clear')

    cowsay.cow("Uh oh...We need cryptography to keep our message safe! But how can we obtain a shared key?")
    backward_foxsay("Let's use the Anshel-Anshel-Goldfeld key exchange protocol. I'll be Alice, you are Bob.")

    pause()
    os.system('clear')

    backward_foxsay(f"ALICE's PUBLIC SET\nI chose {len(alice.publicKey)} elements from {group_object} as my public set.")

    pause()

    backward_foxsay(f"ALICE's PRIVATE KEY\nI then chose some of those and multiplied them together to get my private key, \n {alice._privateKey}")

    pause()
    os.system('clear')

    backward_foxsay(f"ALICE's PRIVATE KEY\nI then chose some of those and multiplied them together to get my private key, \n {alice._privateKey}")
    cowsay.cow("TRANSITION \n( B^-1 * a * B ) ∀ a ∈ ā \n(I conjugated my private key with each element of your public key)")

    pause()

    backward_foxsay(f"SHARED KEY (Ka)\nOkay, I multiplied \nA^-1 * (B^-1 * a * B) ∀ a ∈ A\n\n Shared key Ka = A^-1*B^-1*A*B = \n{aliceSharedKey}")
    pause()

    os.system('clear')
    print(f"Ka = \n{aliceSharedKey}")
    print("----------------------------------------------------------------------------------------------------")

    cowsay.cow("""
    Okay, I do the same thing:
     • My pk = subset of G
     • My sk = product of ordered subset of pk
    """)

    pause()

    backward_foxsay("""I compute my transition for you, because you
    cannot see my secret key\n(A^-1*b*A) ∀ b ∈ b_bar""")

    pause()
    os.system('clear')
    print(f"Ka = \n{aliceSharedKey}")
    print("----------------------------------------------------------------------------------------------------")

    cowsay.cow(f"""
    I then calculate the shared key, just like you...
    B^-1 * (A^-1 * b * A) ∀ b ∈ B
    {bobSharedKey.inverse()}
    """)

    pause()
    os.system('clear')
    print(f"Ka = \n{aliceSharedKey}")
    print(f"B^-1 * (A^-1 * b * A) ∀ b ∈ B = \n{bobSharedKey.inverse()}")
    print("----------------------------------------------------------------------------------------------------")

    cowsay.cow(f"""
    Oops! That's not the shared key!
    B^-1 * (A^-1 * b * A) ∀ b ∈ B is the INVERSE of
    A^-1 * (B^-1 * a * B) ∀ a ∈ A, so I will invert
    it to get the actual shared key.
    {bobSharedKey}
    """)

    pause()
    os.system('clear')

    os.system('clear')
    print(f"Ka = \n{aliceSharedKey}")
    print(f"Kb = \n{bobSharedKey}")
    print("----------------------------------------------------------------------------------------------------")

    pause()
    os.system('clear')
    cowsay.trex("I still know neither private key, so to obtain the shared key I would have to guess both private keys!")
    pause()

    print("\nTime:", elapsed)

    return (aliceSharedKey == bobSharedKey and aliceSharedKey == alice.oracle(bob))

def demo_without_animation(group_type, group_object, pk_length, sk_length):
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

    endTime = time.time()

    os.system('clear')
    print(f"G = {group_object}")
    sleep(0.1)
    print(f"\nAlice's public key is a subset of G of size {pk_length}")
    print(f"\nAlice's private key: {alice._privateKey}")
    sleep(0.1)
    print(f"\nBob's public key is a subset of G of size {pk_length}")
    print(f"\nBob's private key: {bob._privateKey}")
    sleep(0.1)
    #print(f"Bob computes a transition for Alice: {bob.transition(alice)}")
    #print(f"Alice computes a transition for Bob: {alice.transition(bob)}")
    print(f"\nAlice's shared key: {aliceSharedKey}")
    print(f"\nBob's shared key: {bobSharedKey}")
    sleep(0.1)

    elapsed = str(timedelta(seconds=((endTime - startTime))))
    print("\nTime:", elapsed)

    pause()
    os.system('clear')

    return (aliceSharedKey == bobSharedKey == alice.oracle(bob))

def main():
    successes = []

    random.seed(1)

    # HEISENBERG GROUP
    # Note: let n be odd
    hg = HeisenbergGroup(n=Integer(5), R=Integer(10000))
    os.system('clear')

    hg_result = animate(HeisenbergGroup, hg, 27, 17)
    successes.append(hg_result)

    # PERMUTATION GROUP
    pg = PermutationGroup([[(1,2,3),(4,5)],[(3,4)]]) # ,[(5,6,7),(8,9)]
    successes.append(demo_without_animation(PermutationGroup, pg, 23, 13))

    # BRAID GROUP
    bg = BraidGroup(5)
    successes.append(demo_without_animation(BraidGroup, bg, 11, 7))

    # RUBIK'S CUBE GROUP
    rg = CubeGroup()
    successes.append(demo_without_animation(CubeGroup, rg, 11, 7))

    print("""
    Here we have demonstrated a generic implementation of the AAG protocol that can work
    with any group. We have shown implementations for...

     • The Heisenberg group, of upper-triangular matrices of a certain form

     • Arbitrary permutation groups

     • The braid group, with an arbitrary number of strands

     • The Rubik's cube group

    Our paper will focus on comparing the performance of the AAG protocol between these groups.""")

    pause()

    print("""
    Thank you for listening! Now you know that you can securely exchange keys with anyone by means of friendship 
    bracelets or Rubik's cubes, and your enemies will struggle to compromise those keys even using their quantum
    computers!
    """)

    cowsay.cow("Bye!")
    backward_foxsay("Bye!")

    sleep(10)

    cowsay.trex("Bye!")

if __name__ == "__main__":
    main()
