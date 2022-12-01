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

        inv = lambda l : list(map(lambda x: x.inverse(), l))
        conj = lambda outside, inside : list(map(lambda x, y: y.inverse() * x * y, inside, outside))
        triple_multiply = lambda X, Y, Z: [x*y*z for x in X for y in Y for z in Z]


        A: list = self._privateKey
        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        Ai: list = inv(A)

        AiBA: list = triple_multiply(Ai, B, A)

        return AiBA
        
    def deriveSharedKey(self, first: bool, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        inv = lambda l : list(map(lambda x: x.inverse(), l))
        conj = lambda outside, inside : list(map(lambda x, y: y.inverse() * x * y, inside, outside))
        triple_multiply = lambda X, Y, Z: [x*y*z for x in X for y in Y for z in Z]

        a_bar: list = self.publicKey # Alice's public set
        A: list = self._privateKey # Alice's private key
        Ai: list = inv(A)

        # transition
        a_prime: list = otherExchangeObject.transition(self) # B^-1 * a_bar * B
        
        # A is a subset of a_bar, so we can use A to filter a_prime index-wise
        # at this point also handle the epsilon exponent (invert things that are inverted in sk)
        a_prime_s: list = []

        for index, is_inverse in self._privateKeySource:
            if is_inverse:
                a_prime_s.append(a_prime[index].inverse())
            else:
                a_prime_s.append(a_prime[index])

        Ka = reduce(lambda x, y: x*y, Ai) * reduce(lambda x, y: x*y, a_prime_s)

        if first:
            return Ka
        else:
            return Ka.inverse()

