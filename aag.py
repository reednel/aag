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

    _publicKey: list

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

    _privateKey: list
    _privateKeySource: list[tuple[int, bool]] # entries: (pk index, is_inverse) for all chosen elements in sk

    def setPrivateKey(self, value: T) -> None:
        self._privateKey = value
    
    privateKey = property(None, setPrivateKey) # make private key unreadable


    def generatePrivateKey(self, length: int) -> None:
        assert length > 0
        assert len(self.publicKey) >= length

        # choose random indices from publicKey
        indices = random.choices(range(len(self.publicKey)), k=length)
        is_inverses = random.choices([True, False], k=length)

        sk = [self.publicKey[i] for i in indices]
        for i in range(len(sk)):
            if is_inverses[i]:
                sk[i] = sk[i].inverse()

        self._privateKey = sk
        self._privateKeySource = list(zip(indices, is_inverses))


    def __repr__(self) -> str:
        return f"Public Key: {self._publicKey} (Private Key: {self._privateKey})" # TODO: remove private key from repr

    def transition(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        inv = lambda l : list(map(lambda x: x.inverse(), l)) # inverse of each element in list

        A: list = self._privateKey # Alice's private key
        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        Ai: list = inv(A) # Inverse of Alice's private key

        # Wikipedia calls this the "transition"
        AiBA: list = [] # should contain the value of Ai * B * A

        # TODO problem area
        for b in B:
            temp = []
            for a, ai in zip(A, Ai): # iterates A, A^-1 in parallel
                temp.append(a * b * ai)
            AiBA.append(reduce(lambda x, y: x*y, temp)) # probably wrong, please delete and start over

        assert len(AiBA) == len(B) # My current understanding is that B and AiBA should be the same length, 1-to-1

        return AiBA
        
    def deriveSharedKey(self, first: bool, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        # All variables defined as in Heisenberg group paper: https://arxiv.org/pdf/1403.4165.pdf

        inv = lambda l : list(map(lambda x: x.inverse(), l)) # inverse of each element in list

        a_bar: list = self.publicKey # Alice's public set
        A: list = self._privateKey # Alice's private key
        Ai: list = inv(A) # Inverse of Alice's private key

        # transition
        a_prime: list = otherExchangeObject.transition(self) # B^-1 * a_bar * B
        
        # a_prime_s is a subset of a_prime
        # a_prime = B^-1 * a_bar * B, that is, it contains conjugates of all elements of Alice's public set a_bar
        # a_prime_s = B^-1 * A * B, that is, it only contains conjugates of elements in Alice's private key A
        a_prime_s: list = []

        # When Alice's private key was chosen, we saved which public-set elements the private key elements
        # corresponded to, and whether the public set element was inverted or not.
        for index, is_inverse in self._privateKeySource:
            if is_inverse:
                a_prime_s.append(a_prime[index].inverse())
            else:
                a_prime_s.append(a_prime[index])

        # We first multiply together all the elements in A^-1
        # Then we multiply together all the elements in a_prime_s
        # Then we multiply the two results together
        Ka = reduce(lambda x, y: x*y, Ai) * reduce(lambda x, y: x*y, a_prime_s) # TODO may be wrong

        # This currently produces a single matrix for Ka. I am unsure whether Ka should be a matrix or a list of matrices.

        if first: # Alice
            return Ka
        else: # Bob
            return Ka.inverse() # Kb = Ka^-1

