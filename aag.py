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

    _publicKey: set

    @property
    def publicKey(self):
        return self._publicKey

    @publicKey.setter
    def publicKey(self, value: T) -> None:
        self._publicKey = value

    @publicKey.getter
    def publicKey(self) -> set:
        return self._publicKey

    def generatePublicKey(self, length: int) -> None:
        assert length > 0
        assert self.G.order() >= length

        pk: set = set()
        while len(pk) < length:
            pk.add(self.G.random_element())

        self._publicKey = pk

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

        A: list = self._privateKey # Alice's private key
        #print(type(A), A)
        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        #print(type(B), B)

        # A^-1 * b_i * A for all b_i in B
        Ai: list = list([x.inverse() for x in A])
        #print(type(Ai), Ai)

        conj = lambda x,y: y.inverse() * x * y

        transition = [conj(b,a) for a in A for b in B]

        return transition
        
    def deriveSharedKey(self, first: bool, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        inv = lambda l : list(map(lambda x: x.inverse(), l))
        conj = lambda outside, inside : list(map(lambda x, y: y.inverse() * x * y, inside, outside))

        A: list = self._privateKey
        Ai: list = inv(A)

        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        Bi: list = inv(B)

        BiAB: list = [x * y * z for x,y,z in zip(Bi, A, B)]
        #AiBA: list = [x * y * z for x,y,z in zip(Ai, B, A)]
        #print(type(BiAB), BiAB)

        if first: # want AiBiAB
            Ka = [x * y for x,y in zip(Ai, BiAB)]
            return Ka
        else: # want BiAiBA which is here inv(AiBiAB)
            Kb = inv([x * y for x,y in zip(BiAB, Ai)])
            return Kb

