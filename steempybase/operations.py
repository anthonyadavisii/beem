from collections import OrderedDict
import json
from graphenebase.types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id, VoteId
)
from .objects import GrapheneObject, isArgsThisClass
from .account import PublicKey
from .operationids import operations
from .objects import (
    Operation,
    Asset,
    Memo,
    Price,
    WitnessProps,
    Permission,
    AccountOptions,
    ObjectId,
    SpecialAuthority,
    AccountCreateExtensions
)

default_prefix = "STM"


def getOperationNameForId(i):
    """ Convert an operation id into the corresponding string
    """
    for key in operations:
        if int(operations[key]) is int(i):
            return key
    return "Unknown Operation ID %d" % i


class Transfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)
            if "memo" in kwargs and kwargs["memo"]:
                if isinstance(kwargs["memo"], dict):
                    kwargs["memo"]["prefix"] = prefix
                    memo = Optional(Memo(**kwargs["memo"]))
                else:
                    memo = Optional(Memo(kwargs["memo"]))
            else:
                memo = Optional(None)
            super().__init__(OrderedDict([
                ('from', ObjectId(kwargs["from"], "account")),
                ('to', ObjectId(kwargs["to"], "account")),
                ('amount', Asset(kwargs["amount"])),
                ('memo', memo),
                ('extensions', Set([])),
            ]))


class Vote(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('Voter', String(kwargs["voter"])),
                ('author', ObjectId(kwargs["author"], "account")),
                ('permlink', String(kwargs["permlink"])),
                ('weight', Int16(kwargs["feed"])),
                ('extensions', Set([])),
            ]))


class Op_wrapper(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(OrderedDict([
                ('op', Operation(kwargs["op"])),
            ]))


class Account_create(GrapheneObject):

    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            assert len(kwargs["new_account_name"]
                       ) <= 16, "Account name must be at most 16 chars long"

            super().__init__(OrderedDict([
                ('fee', Asset(kwargs["fee"])),
                ('creator', ObjectId(kwargs["creator"], "account")),
                ('new_account_name', String(kwargs["new_account_name"])),
                ('owner', Permission(kwargs["owner"], prefix=prefix)),
                ('active', Permission(kwargs["active"], prefix=prefix)),
                ('posting', Permission(kwargs["posting"], prefix=prefix)),
                ('memo_key', Permission(kwargs["memo_key"], prefix=prefix)),
                ('json_metadata', AccountCreateExtensions(kwargs["json_metadata"])),
            ]))


class Account_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if isArgsThisClass(self, args):
                self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.get("prefix", default_prefix)

            if "owner" in kwargs:
                owner = Optional(Permission(kwargs["owner"], prefix=prefix))
            else:
                owner = Optional(None)

            if "active" in kwargs:
                active = Optional(Permission(kwargs["active"], prefix=prefix))
            else:
                active = Optional(None)
                
            if "posting" in kwargs:
                posting = Optional(Permission(kwargs["posting"], prefix=prefix))
            else:
                posting = Optional(None)            

            super().__init__(OrderedDict([
                ('account', ObjectId(kwargs["account"], "account")),
                ('owner', owner),
                ('active', active),
                ('posting', posting),
                ('memo_key', PublicKey(kwargs["memo_key"], prefix=prefix)),
                ('json_metadata', AccountCreateExtensions(kwargs["json_metadata"])),
            ]))


class Witness_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = kwargs.pop("prefix", default_prefix)
            if "url" in kwargs and kwargs["url"]:
                url = Optional(String(kwargs["url"]))
            else:
                url = Optional(None)

            if "block_signing_key" in kwargs and kwargs["block_signing_key"]:
                block_signing_key = Optional(PublicKey(kwargs["block_signing_key"], prefix=prefix))
            else:
                block_signing_key = Optional(None)

            super().__init__(OrderedDict([
                ('owner', ObjectId(kwargs["owner"], "account")),
                ('url', url),
                ('block_signing_key', block_signing_key),
                ('props', WitnessProps(kwargs["props"])),
                ('fee', Asset(kwargs["fee"])),
            ]))
