from datetime import timedelta
from typing import Optional, TypeAlias

from nats.aio.client import Client
from nats.js.errors import BadRequestError
from nats.js.kv import KeyValue

from .key import KvNameBuilder, DefaultKvNameBuilder

ExpiryT: TypeAlias = float | timedelta


class NATSFSMAdapter:
    def __init__(
            self,
            client: Client,
            kv_name_builder: Optional[KvNameBuilder] = None,
            state_ttl: Optional[ExpiryT] = None,
            data_ttl: Optional[ExpiryT] = None,
            manual_close: bool = False,
    ):
        if kv_name_builder is None:
            kv_name_builder = DefaultKvNameBuilder()
        self.client = client
        self.kv_name_builder = kv_name_builder
        self._state_kv: Optional[KeyValue] = None
        self._data_kv: Optional[KeyValue] = None
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl
        self.manual_close = manual_close

    @property
    def state_kv(self) -> KeyValue:
        if self._state_kv is None:
            raise RuntimeError("'state_kv' is not created")
        return self._state_kv

    @property
    def data_kv(self) -> KeyValue:
        if self._data_kv is None:
            raise RuntimeError("'data_kv' is not created")
        return self._data_kv

    async def close(self) -> None:
        if not self.manual_close:
            await self.client.close()

    async def create_kv(self) -> None:
        js = self.client.jetstream()
        state_kv = self.kv_name_builder.build("state")
        data_kv = self.kv_name_builder.build("data")

        try:
            self._state_kv = await js.create_key_value(bucket=state_kv, ttl=self.state_ttl)
        except BadRequestError:
            self._state_kv = await js.key_value(bucket=state_kv)

        try:
            self._data_kv = await js.create_key_value(bucket=data_kv, ttl=self.data_ttl)
        except BadRequestError:
            self._data_kv = await js.key_value(bucket=data_kv)
