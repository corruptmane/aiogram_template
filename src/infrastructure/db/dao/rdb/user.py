from sqlalchemy import select, true, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import dcf_dump
from src.core.models import dto
from src.infrastructure.db.dao.rdb.base import BaseDAO
from src.infrastructure.db.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def upsert_user(self, user: dto.User) -> dto.User:
        kwargs = dcf_dump(user)
        saved_user = await self._session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(User.user_id,),
                set_=kwargs,
                where=User.user_id == user.user_id,
            )
            .returning(User)
        )
        return saved_user.scalar_one().to_dto()

    async def mark_user_not_active(self, user_id: int) -> None:
        stmt = update(User).where(User.user_id == user_id).values(is_active=False)
        await self._session.execute(stmt)

    async def get_all_active_user_ids(self) -> list[int]:
        stmt = select(User.user_id).where(User.is_active == true())
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
