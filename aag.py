from sage.all import *
from sage.groups.group import Group
from sage.sets.set import Set
from typing import TypeVar, Generic
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

    def setPrivateKey(self, value: T) -> None:
        self._privateKey = value
    
    privateKey = property(None, setPrivateKey) # make private key unreadable

    def generatePrivateKey(self, length: int) -> None:
        assert length > 0
        assert len(self.publicKey) >= length

        pk: list = random.choices(list(self.publicKey), k=length)
        self._privateKey = pk

    def __repr__(self) -> str:
        return f"Public Key: {self._publicKey} (Private Key: {self._privateKey})" # TODO: remove private key from repr

    def transition(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        inv = lambda l : list(map(lambda x: x.inverse(), l))
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
        A_indices_in_a_bar: list = [a_bar.index(a) for a in A]

        a_prime: list = otherExchangeObject.transition(self) # B^-1 * a_bar * B
        
        # A is a subset of a_bar, so we can use A to filter b_prime index-wise
        a_prime_s: list = [a_prime[i] for i in A_indices_in_a_bar]

        if first:
            Ka = [x * y for x in Ai for y in a_prime_s]
            return Ka
        else:
            Kb = inv([x * y for x in Ai for y in a_prime_s])
            return Kb

