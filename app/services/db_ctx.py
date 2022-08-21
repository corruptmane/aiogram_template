from contextlib import asynccontextmanager
from typing import TypeVar, cast, Any, Sequence, Callable, AsyncGenerator, Generic

from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.elements import BinaryExpression, ClauseElement

from app.models.base import BaseModel

ASTERISK = '*'

SQLAlchemyModel = TypeVar('SQLAlchemyModel', bound=BaseModel)
ExpressionType = BinaryExpression | ClauseElement | bool


class BaseRepo(Generic[SQLAlchemyModel]):
    model: SQLAlchemyModel

    def __init__(self, session_or_pool: sessionmaker | AsyncSession) -> None:
        if isinstance(session_or_pool, sessionmaker):
            self._session: AsyncSession = cast(AsyncSession, session_or_pool())
        else:
            self._session = session_or_pool

    async def add(self, **values: Any) -> None:
        stmt = insert(self.model).values(**values).on_conflict_do_nothing()
        async with self._transaction():
            await self._session.execute(stmt)

    async def add_many(self, *models: SQLAlchemyModel) -> None:
        async with self._transaction():
            bulk_save_func = make_proxy_bulk_save_func(instances=models)
            await self._session.run_sync(bulk_save_func)

    async def get_one(self, *clauses: ExpressionType) -> SQLAlchemyModel | None:
        stmt = select(self.model).where(*clauses).limit(1)
        async with self._transaction():
            result = (await self._session.execute(stmt)).scalars().first()
        return cast(SQLAlchemyModel | None, result)

    async def get_random(self, *clauses: ExpressionType, limit: int = 1) -> SQLAlchemyModel | None:
        stmt = select(self.model).where(*clauses).order_by(func.random()).limit(limit)
        async with self._transaction():
            result = (await self._session.execute(stmt)).scalars().first()
        return cast(SQLAlchemyModel | None, result)

    async def get_all(self, *clauses: ExpressionType, limit: int | None = None) -> list[SQLAlchemyModel] | None:
        stmt = select(self.model).where(*clauses).limit(limit)
        async with self._transaction():
            results = (await self._session.execute(stmt)).scalars().all()
        return cast(list[SQLAlchemyModel] | None, results)

    async def update(self, *clauses: ExpressionType, **values: Any) -> None:
        stmt = update(self.model).where(*clauses).values(**values).returning(None)
        async with self._transaction():
            await self._session.execute(stmt)
        return None

    async def delete(self, *clauses: ExpressionType, returning: Any = ASTERISK) -> list[SQLAlchemyModel] | None:
        stmt = delete(self.model).where(*clauses).returning(returning)
        async with self._transaction():
            result = (await self._session.execute(stmt)).scalars().all()
        return cast(list[SQLAlchemyModel] | None, result)

    async def count(self, *clauses: ExpressionType, limit: int | None = None) -> int:
        stmt = select(func.count(ASTERISK)).select_from(self.model).limit(limit)
        if clauses:
            stmt = stmt.where(*clauses)
        async with self._transaction():
            result = (await self._session.execute(stmt)).scalar()
        return cast(int, result)

    async def exists(self, *clauses: ExpressionType) -> bool:
        stmt = exists(select(self.model)).where(*clauses).select()
        async with self._transaction():
            result = (await self._session.execute(stmt)).scalar()
        return cast(bool, result)

    @asynccontextmanager
    async def _transaction(self) -> AsyncGenerator:
        if not self._session.in_transaction() and self._session.is_active:
            async with self._session.begin() as transaction:
                yield transaction
        else:
            yield


def make_proxy_bulk_save_func(
        instances: Sequence[Any],
        return_defaults: bool = False,
        update_changed_only: bool = True,
        preserve_order: bool = True
) -> Callable[[Session], None]:
    def _proxy(session: Session) -> None:
        return session.bulk_save_objects(
            instances,
            return_defaults=return_defaults,
            update_changed_only=update_changed_only,
            preserve_order=preserve_order)
    return _proxy
