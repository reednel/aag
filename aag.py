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

        skProd = self.G.one()
        for x in sk:
            skProd *= x

        self._privateKey = skProd

    def __repr__(self) -> str:
        return f"Public Key: {self._publicKey} (Private Key: {self._privateKey})" # TODO: remove private key from repr

    def transition(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        # inv = lambda l : list(map(lambda x: x.inverse(), l)) # inverse of each element in list

        A = self._privateKey # Alice's private key
        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        Ai = A.inverse() # Inverse of Alice's private key

        # Wikipedia calls this the "transition"
        AiBA: list = [A * b * Ai for b in B] # should contain the value of Ai * B * A

        return AiBA

    def bob_transition(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        # inv = lambda l : list(map(lambda x: x.inverse(), l)) # inverse of each element in list

        A = self._privateKey # Alice's private key
        B: list = list(otherExchangeObject.publicKey) # Bob's public key
        Ai = A.inverse() # Inverse of Alice's private key

        # Wikipedia calls this the "transition"
        AiBA: list = [A * b.inverse() * Ai for b in B] # should contain the value of Ai * B * A

        return AiBA
        
    def deriveSharedKey(self, first: bool, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        # All variables defined as in Heisenberg group paper: https://arxiv.org/pdf/1403.4165.pdf

        # a_bar: list = self.publicKey # Alice's public set
        
        

        

        if first: # Alice
            # Distribute Ai to all elements of a_prime and take the product
            # Not certain that's the right thing to do
            A = self._privateKey # Alice's private key
            Ai = A.inverse() # Inverse of Alice's private key

            # transition
            a_prime: list = otherExchangeObject.transition(self) # B^-1 * a_bar * B
            Ka = reduce(lambda x, y: x * Ai * y, a_prime, self.G.one()) 
            return Ka
        else: # Bob
            B = self._privateKey
            Bi = B.inverse() # Inverse of Alice's private key

            # transition
            b_prime: list = otherExchangeObject.transition(self)
            Kb = reduce(lambda x, y: x * y * B, b_prime, self.G.one())
            return Kb
