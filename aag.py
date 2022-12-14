from sage.all import *
from sage.groups.group import Group
from typing import TypeVar, Generic
from functools import reduce
import random

from sage.groups.matrix_gps.heisenberg import HeisenbergGroup
from sage.groups.perm_gps.permgroup import PermutationGroup
from sage.groups.perm_gps.cubegroup import CubeGroup
from sage.groups.braid import BraidGroup_class

T = TypeVar('T', bound=Group)

class AAGExchangeObject(Generic[T]):
    # Abstract class for AAG exchange objects
    # holds reference to parent group, and selected public key, which is a
    # subset of that group

    def __init__(self, group) -> None:
        self.G = group
        self._publicKey: list
        self._privateKey: T
        self._privateKeySource: list[tuple[int, bool]] # entries: (pk index, is_inverse) for all chosen elements in sk

    @property
    def publicKey(self):
        return self._publicKey

    @publicKey.setter
    def publicKey(self, value: T) -> None:
        self._publicKey = value

    @publicKey.getter
    def publicKey(self) -> list:
        return self._publicKey

    def random_element_H(self, n, R):
        n += 2 # matrix dim is 2 greater than n
        H = matrix(ZZ, n, n, lambda i,j: 1 if i == j else 0)
        for i in range(1, n-1):
            H[0,i] = random.randint(0, R)
            H[i,n-1] = random.randint(0, R)
        H[0,n-1] = random.randint(0, R)

        g = self.G.Element(self.G, H, check=False) # Need check=false to circumvent O(|G|) check
        return g

    def random_element_B(self, n):

        # See "Length Based Attack and Braid Groups: Cryptanalysis of
        # Anshel-Anshel-Goldfeld Key Exchange Protocol" for choice of L1, L2
        L1 = 5
        L2 = 8

        def getrand(n):
            while True:
                v = random.randint(0 - n, n)
                if v != 0:
                    return v

        B = [getrand(n) for _ in range(random.randint(L1, L2))]

        g = self.G.Element(self.G, B, check=False)
        return g

    def generatePublicKey(self, length: int) -> None:
        assert length > 0
        assert self.G.order() >= length

        pk: set = set()
        while len(pk) < length:
            if isinstance(self.G, HeisenbergGroup):
                g = self.random_element_H(self.G._n, len(self.G._ring))
            elif isinstance(self.G, BraidGroup_class):
                g = self.random_element_B(self.G.strands()-1)
            else:
                g = self.G.random_element() # very slow for large groups

            pk.add(g)

        self._publicKey = list(pk)

    def setPrivateKey(self, value: T) -> None:
        self._privateKey = value

    def generatePrivateKey(self, length: int) -> None:
        assert length > 0

        # choose random indices from publicKey
        indices = random.choices(range(len(self.publicKey)), k=length)
        is_inverses = random.choices([True, False], k=length)
        self._privateKeySource = list(zip(indices, is_inverses))

        # collect chosen elements and invert if randomly selected
        sk = [self.publicKey[i] for i in indices]
        for i in range(len(sk)):
            if is_inverses[i]:
                sk[i] = sk[i].inverse()

        # private key is ordered product of chosen elements
        self._privateKey = reduce(lambda x, y: x * y, sk)
        assert self._privateKey in self.G

    def __repr__(self) -> str:
        return f"Public Key: {self._publicKey} (Private Key: {self._privateKey})" # TODO: remove private key from repr

    def oracle(self, otherExchangeObject):
        # Returns the correct shared key. This is only used for testing purposes.

        # Compute A * B
        AB = self._privateKey * otherExchangeObject._privateKey

        # Compute Ai * Bi * A * B
        return self._privateKey.inverse() * otherExchangeObject._privateKey.inverse() * AB

    def transition(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        A = self._privateKey # Alice's private key
        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        Ai = A.inverse() # Inverse of Alice's private key

        # Wikipedia calls this the "transition"
        AiBA: list = [Ai * b * A for b in B] # should contain the value of Ai * B * A

        return AiBA

    def deriveSharedKey(self, first: bool, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        # All variables defined as in Heisenberg group paper: https://arxiv.org/pdf/1403.4165.pdf

        A = self._privateKey # Alice's private key
        Ai = A.inverse() # Inverse of Alice's private key

        # transition
        # a_prime = B^-1 * a_bar * B, that is, it contains conjugates of all
        # elements of Alice's public set a_bar
        a_prime: list = otherExchangeObject.transition(self) # B^-1 * a_bar * B

        # a_prime_s = B^-1 * A * B, that is, it only contains conjugates of elements in Alice's private key A
        a_prime_s: list = []

        # When Alice's private key was chosen, we saved which public-set elements the private key elements
        # corresponded to, and whether the public set element was inverted or not.
        for index, is_inverse in self._privateKeySource:
            if is_inverse:
                a_prime_s.append(a_prime[index].inverse())
            else:
                a_prime_s.append(a_prime[index])

        a_prime_s_prod = reduce(lambda x, y: x * y, a_prime_s)

        # THIS MULTIPLICATION IS BAD AND I CAN'T FATHOM WHY
        Ka = Ai * a_prime_s_prod

        # # DEBUG
        # if first:
        #     print("A:     ", A)
        #     print("Ai:    ", Ai)
        #     print("BiAB:  ", a_prime)
        #     print("a'_s:  ", a_prime_s)
        #     print("a'_s X:", a_prime_s_prod)
        #     print("AiBiAB:", Ka)
        #     print("")
        # else:
        #     print("B:     ", A)
        #     print("Bi:    ", Ai)
        #     print("AiBA:  ", a_prime)
        #     print("b'_s:  ", a_prime_s)
        #     print("b'_s X:", a_prime_s_prod)
        #     print("BiAiBA:", Ka)
        #     print("AiBiAB:", Ka.inverse())
        #     print("")

        if first: # Alice
            return Ka
        else: # Bob
            return Ka.inverse()
