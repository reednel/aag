from sage.all import *
from sage.groups.group import Group
from sage.sets.set import Set
from typing import TypeVar, Generic
from functools import reduce
import random

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

    def generatePublicKey(self, length: int) -> None:
        assert length > 0
        assert self.G.order() >= length

        pk: set = set()
        while len(pk) < length:
            pk.add(self.G.random_element())

        self._publicKey = list(pk)

    def setPrivateKey(self, value: T) -> None:
        self._privateKey = value

    def generatePrivateKey(self, length: int) -> None:
        assert length > 0
        assert len(self.publicKey) >= length

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
        assert self._privateKey != self.G.one() # might be a problem once in a while, TODO delete when bug fixed

    def __repr__(self) -> str:
        return f"Public Key: {self._publicKey} (Private Key: {self._privateKey})" # TODO: remove private key from repr

    def transition(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        A = self._privateKey # Alice's private key
        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        Ai = A.inverse() # Inverse of Alice's private key

        # Wikipedia calls this the "transition"
        AiBA: list = [A * b * Ai for b in B] # should contain the value of Ai * B * A

        return AiBA

    def deriveSharedKey(self, first: bool, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        # All variables defined as in Heisenberg group paper: https://arxiv.org/pdf/1403.4165.pdf

        # Distribute Ai to all elements of a_prime and take the product
        # Not certain that's the right thing to do
        A = self._privateKey # Alice's private key
        Ai = A.inverse() # Inverse of Alice's private key

        # transition
        # a_prime = B^-1 * a_bar * B, that is, it contains conjugates of all elements of Alice's public set a_bar
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

        # # DEBUG
        # print("Ai")
        # print(Ai)
        # print("a_prime_s_prod")
        # print(a_prime_s_prod)

        # NOTICE: neither Ai nor a_prime_s_prod are identity or near-identity...
        # I have verified the product is actually Ka

        Ka = Ai * a_prime_s_prod

        if first: # Alice
            return Ka
        else: # Bob
            return Ka.inverse()
