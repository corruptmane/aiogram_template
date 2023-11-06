from dataclasses import dataclass
from typing import Self

from aiogram import types as tg
from aiogram.utils.markdown import hlink

from src.core.utils.unset import Empty


@dataclass(slots=True, kw_only=True)
class User:
    user_id: int | Empty = Empty.UNSET
    full_name: str | Empty | None = None
    username: str | Empty | None = None

    is_active: bool | Empty = True

    @property
    def url(self) -> str:
        if isinstance(self.username, str):
            return f'https://t.me/{self.username}'
        if self.user_id is Empty.UNSET:
            raise ValueError('user_id is not set')
        return f'tg://user?id={self.user_id}'

    def get_mention(self, name: str | None = None) -> str:
        if name is None:
            name = self.full_name
        return hlink(name, self.url)

    @classmethod
    def from_aiogram(cls, user: tg.User, is_active: bool = True) -> Self:
        return cls(
            user_id=user.id,
            full_name=user.full_name,
            username=user.username,
            is_active=is_active,
        )
