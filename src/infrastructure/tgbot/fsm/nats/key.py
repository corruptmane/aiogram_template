from abc import abstractmethod, ABC
from typing import Literal

from aiogram.fsm.storage.base import StorageKey, DEFAULT_DESTINY
from pathvalidate import is_valid_filename


class KvNameBuilder:
    @abstractmethod
    def build(self, part: Literal["state", "data"]) -> str:
        pass


class DefaultKvNameBuilder(KvNameBuilder):
    def __init__(self, prefix: str = "fsm", separator: str = "_"):
        self.prefix = prefix
        self.separator = separator

        if not is_valid_filename(self.build("state")):  # build key for validate
            raise ValueError(
                "Invalid kv builder "
                f"prefix or separator ({self.prefix!r}, "
                f"{self.separator!r})"
            )

    def build(self, part: Literal["state", "data"]) -> str:
        return f"{self.prefix}{self.separator}{part}"


class KeyBuilder(ABC):
    @abstractmethod
    def build(self, key: StorageKey, part: Literal["data", "state", "lock"]) -> str:
        pass


class DefaultKeyBuilder(KeyBuilder):
    def __init__(
            self,
            *,
            prefix: str = "fsm",
            separator: str = ":",
            with_bot_id: bool = False,
            with_destiny: bool = False,
    ) -> None:
        self.prefix = prefix
        self.separator = separator
        self.with_bot_id = with_bot_id
        self.with_destiny = with_destiny

    def build(self, key: StorageKey, part: Literal["data", "state", "lock"]) -> str:
        parts = [self.prefix]
        if self.with_bot_id:
            parts.append(str(key.bot_id))
        parts.extend([str(key.chat_id), str(key.user_id)])
        if self.with_destiny:
            parts.append(key.destiny)
        elif key.destiny != DEFAULT_DESTINY:
            raise ValueError(
                "Nats key builder is not configured to use key destiny other the default.\n"
                "\n"
                "Probably, you should set `with_destiny=True` in for DefaultKeyBuilder.\n"
                "E.g: `NatsStorage(adapter, key_builder=DefaultKeyBuilder(with_destiny=True))`"
            )
        parts.append(part)
        return self.separator.join(parts)
