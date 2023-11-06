from typing import Protocol

from src.core.interfaces.dao.base import Committer
from src.core.models import dto


class UserUpserter(Committer, Protocol):
    async def upsert_user(self, user: dto.User) -> dto.User:
        raise NotImplementedError


class UserNotActiveMarker(Committer, Protocol):
    async def mark_user_not_active(self, user_id: int) -> None:
        raise NotImplementedError


class AllActiveUserIdsGetter(Protocol):
    async def get_all_active_user_ids(self) -> list[int]:
        raise NotImplementedError
