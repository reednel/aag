from sage.all import *
from abc import ABC, abstractmethod
from sage.groups.group import Group
from typing import TypeVar, Generic

T = TypeVar('T', bound=Group)

class AAGExchangeObject(Generic[T]):
    # Abstract class for AAG exchange objects
    # holds reference to parent group, and selected public key, which is a
    # subset of that group

    def __init__(self) -> None:
        pass

    _publicKey: list = None  # TODO subgroup type? What should be the type here?

    @property
    def publicKey(self):
        return self._publicKey

    @publicKey.setter
    def publicKey(self, value) -> None:
        self._publicKey = value

    @publicKey.getter
    def publicKey(self):
        return self._publicKey

    _privateKey: list = None

    def privateKey(self, value) -> None:
        self._privateKey = value

    privateKey = property(None, privateKey) # make private key unreadable

    def __repr__(self) -> str:
        return f"Public Key: {self._publicKey} (Private Key: {self._privateKey})" # TODO: remove private key from repr

    def deriveSharedKey(self, otherExchangeObject) -> list:
        assert self._publicKey != None
        assert otherExchangeObject.publicKey != None
        assert self._privateKey != None

        # AAG multiplication
        # TODO @reed nelson
        sharedKey = None

        return sharedKey