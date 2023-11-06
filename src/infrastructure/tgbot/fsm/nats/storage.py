from typing import cast, Any

import ormsgpack
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey
from nats.js.errors import KeyNotFoundError

from .adapter import NATSFSMAdapter
from .key import DefaultKeyBuilder, KeyBuilder


class NATSStorage(BaseStorage):
    def __init__(self, adapter: NATSFSMAdapter, key_builder: KeyBuilder | None = None):
        if key_builder is None:
            key_builder = DefaultKeyBuilder()
        self.adapter = adapter
        self.key_builder = key_builder

    async def close(self) -> None:
        await self.adapter.close()

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        nats_key = self.key_builder.build(key, "state")
        if state is None:
            await self.adapter.state_kv.purge(nats_key)
        else:
            if isinstance(state, State):
                state = state.state
            await self.adapter.state_kv.put(nats_key, ormsgpack.packb(state))

    async def get_state(self, key: StorageKey) -> str | None:
        nats_key = self.key_builder.build(key, "state")
        try:
            entry = await self.adapter.state_kv.get(nats_key)
        except KeyNotFoundError:
            value = None
        else:
            value = entry.value
        if value is not None:
            return cast(str, ormsgpack.unpackb(value))
        return value

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        nats_key = self.key_builder.build(key, "data")
        if not data:
            await self.adapter.data_kv.purge(nats_key)
        await self.adapter.data_kv.put(nats_key, ormsgpack.packb(data))

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        nats_key = self.key_builder.build(key, "data")
        try:
            entry = await self.adapter.data_kv.get(nats_key)
        except KeyNotFoundError:
            value = None
        else:
            value = entry.value
        if value is None:
            return {}
        return cast(dict[str, Any], ormsgpack.unpackb(value))
