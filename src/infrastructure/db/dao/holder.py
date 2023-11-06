from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.rdb.user import UserDAO


class HolderDAO:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.user = UserDAO(session)

    async def commit(self) -> None:
        await self._session.commit()
