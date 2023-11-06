from typing import TypeVar, Type, Any

import ormsgpack
from nats.aio.msg import Msg

from src.common import dcf_load, dcf_dump

_T = TypeVar('_T')


def unpack_message(msg: Msg, tp: Type[_T]) -> _T:
    return dcf_load(ormsgpack.unpackb(msg.data), tp)


def pack_message(data: Any) -> bytes:
    return ormsgpack.packb(dcf_dump(data))
