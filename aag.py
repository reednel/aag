from sage.all import *
from sage.groups.group import Group
from typing import TypeVar, Generic
import random

T = TypeVar('T', bound=Group)

class AAGExchangeObject(Generic[T]):
    # Abstract class for AAG exchange objects
    # holds reference to parent group, and selected public key, which is a
    # subset of that group

    def __init__(self, group) -> None:
        self.parent_group = group

    _publicKey: list

    @property
    def publicKey(self):
        return self._publicKey

    @publicKey.setter
    def publicKey(self, value) -> None:
        self._publicKey = value

    @publicKey.getter
    def publicKey(self):
        return self._publicKey

    def generatePublicKey(self, length: int) -> None:
        assert length > 0
        assert self.parent_group.order() >= length

        pk: set = set()
        while len(pk) < length:
            pk.add(self.parent_group.random_element())

        self._publicKey = list(pk)

    _privateKey: list

    def setPrivateKey(self, value) -> None:
        self._privateKey = value
    
    privateKey = property(None, setPrivateKey) # make private key unreadable

    def generatePrivateKey(self, length: int) -> None:
        assert length > 0
        assert len(self.publicKey) >= length

        self._privateKey = random.choices(list(self.publicKey))

    def __repr__(self) -> str:
        return f"Public Key: {self._publicKey} (Private Key: {self._privateKey})" # TODO: remove private key from repr

    def deriveSharedKey(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        A = otherExchangeObject.publicKey
        B = self._privateKey

        sharedKey = [A[i].inverse() * B[i] * A[i] for i in range(len(B))]

        return sharedKey