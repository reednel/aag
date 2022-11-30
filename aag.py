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
        """Returns A^-1 * b_i * A, the conjugate of this person's private key with the other person's public."""
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

        conj = lambda inside, outside: outside.inverse() * inside * outside

        transition = [conj(b,a) for a in A for b in B]

        return transition
        
    def deriveSharedKey(self, first: bool, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        A: list = self._privateKey
        BiAB: list = otherExchangeObject.transition(self) # BiAB = B^-1 * a_i * B for all a_i in A
                                                          #     or A^-1 * b_i * A for all b_i in B
        B: list = list(otherExchangeObject.publicKey)

        gamma1 = lambda u, v: u.inverse() * v
        gamma2 = lambda u, v: v.inverse() * u
        beta = lambda u, v: v.transition(u)

        # key is Ai * BiAB
        if first:
            sharedKey = [gamma1(a, b) for a in A for b in BiAB]
        else:
            sharedKey = [gamma2(a, b) for a in A for b in BiAB]

        return sharedKey