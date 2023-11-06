from typing import TypedDict

import structlog
from nats.aio.client import Callback, ErrorCallback

log = structlog.get_logger('nats.callbacks')


async def error_cb(exc: Exception) -> None:
    await log.aexception('NATS error occurred', exc_info=exc)


async def disconnected_cb() -> None:
    await log.awarning('NATS disconnected')


async def closed_cb() -> None:
    await log.awarning('NATS connection closed')


async def discovered_server_cb() -> None:
    await log.adebug('NATS discovered server')


async def reconnected_cb() -> None:
    await log.ainfo('NATS reconnected')


class Callbacks(TypedDict):
    error_cb: ErrorCallback
    disconnected_cb: Callback
    closed_cb: Callback
    discovered_server_cb: Callback
    reconnected_cb: Callback


all_callbacks: Callbacks = {
    'error_cb': error_cb,
    'disconnected_cb': disconnected_cb,
    'closed_cb': closed_cb,
    'discovered_server_cb': discovered_server_cb,
    'reconnected_cb': reconnected_cb,
}
