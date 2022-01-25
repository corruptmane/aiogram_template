import contextlib
import enum
import sys
from typing import TypeVar, Union, Optional, Generic, Type, cast, Any, Sequence, Callable, Iterable

from sqlalchemy import delete, exists, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction, AsyncResult
from sqlalchemy.orm import sessionmaker, Session, joinedload
from sqlalchemy.sql.elements import BinaryExpression, ClauseElement

from tgbot.models.base import BaseModel

ASTERISK = '*'

SQLAlchemyModel = TypeVar('SQLAlchemyModel', bound=BaseModel)
ExpressionType = Union[BinaryExpression, ClauseElement, bool]


class TransactionStrategy(enum.Enum):
    ONE_PER_REQUEST = 1
    KEEP_ALIVE = 2


DEFAULT_STRATEGY = TransactionStrategy.ONE_PER_REQUEST


class Transaction:
    def __init__(self, session: AsyncSession, strategy: TransactionStrategy):
        self._session = session
        self._strategy = strategy
        self._current_txn: Optional[AsyncSessionTransaction] = None

    async def __aenter__(self) -> AsyncSessionTransaction:
        if self._current_txn is not None and self._strategy == TransactionStrategy.KEEP_ALIVE:
            return self._current_txn
        self._current_txn = self._session.begin()
        await self._current_txn.start()
        return self._current_txn

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None or exc_val is not None or exc_tb is not None:
            return await self._current_txn.__aexit__(exc_type, exc_val, exc_tb)
        if self._strategy == TransactionStrategy.KEEP_ALIVE:
            return
        await self._current_txn.__aexit__(exc_type, exc_val, exc_tb)

    async def close(self) -> None:
        await self._current_txn.__aexit__(None, None, None)

    def change_strategy(self, new_strategy: TransactionStrategy) -> None:
        self._strategy = new_strategy


class DatabaseContext(Generic[SQLAlchemyModel]):
    def __init__(
            self,
            session_or_pool: Union[sessionmaker, AsyncSession],
            *,
            query_model: Type[SQLAlchemyModel]
    ) -> None:
        if isinstance(session_or_pool, sessionmaker):
            self._session: AsyncSession = cast(AsyncSession, session_or_pool())
        else:
            self._session = session_or_pool
        self.model = query_model
        self._transaction = Transaction(self._session, DEFAULT_STRATEGY)

    async def add(self, **values: Any) -> Optional[SQLAlchemyModel]:
        async with self._transaction:
            stmt = insert(self.model).values(
                **values
            ).returning(ASTERISK)
            result = await self._session.execute(stmt)
        return result.scalars().first()

    async def add_many(self, *models: SQLAlchemyModel) -> None:
        async with self._transaction:
            bulk_save_func = make_proxy_bulk_save_func(instances=models)
            await self._session.run_sync(bulk_save_func)

    async def get_all(self, *clauses: ExpressionType, load: Optional[Any] = None) -> list[SQLAlchemyModel]:
        stmt = select(self.model).where(*clauses)
        if load:
            if isinstance(load, Iterable):
                for query in load:
                    stmt = stmt.options(joinedload(query))
            else:
                stmt = stmt.options(joinedload(load))
        async with self._transaction:
            result: AsyncResult = await self._session.execute(stmt)
            scalars = result.scalars().unique().all()
        return cast(list[SQLAlchemyModel], scalars)

    async def get_one(self, *clauses: ExpressionType, load: Optional[Any] = None) -> Optional[SQLAlchemyModel]:
        stmt = select(self.model).where(*clauses)
        if load:
            if isinstance(load, Iterable):
                for query in load:
                    stmt = stmt.options(joinedload(query))
            else:
                stmt = stmt.options(joinedload(load))
        async with self._transaction:
            result: AsyncResult = await self._session.execute(stmt)
            first_scalar_result = result.scalars().first()
        return first_scalar_result

    async def update(self, *clauses: ExpressionType, **values: Any) -> list[SQLAlchemyModel]:
        async with self._transaction:
            stmt = update(self.model).where(*clauses).values(**values).returning(ASTERISK)
            result = (await self._session.execute(stmt)).scalars().all()
        return cast(list[SQLAlchemyModel], result)

    async def exists(self, *clauses: ExpressionType) -> bool:
        async with self._transaction:
            stmt = exists(self.model).where(*clauses).select()
            result = (await self._session.execute(stmt)).scalar()
        return cast(bool, result)

    async def delete(self, *clauses: ExpressionType) -> list[SQLAlchemyModel]:
        async with self._transaction:
            stmt = delete(self.model).where(*clauses).returning(ASTERISK)
            result = (await self._session.execute(stmt)).scalars().all()
        return cast(list[SQLAlchemyModel], result)

    async def count(self, *clauses: ExpressionType) -> int:
        async with self._transaction:
            stmt = select(func.count(ASTERISK)).select_from(self.model).where(*clauses)
            result: AsyncResult = await self._session.execute(stmt)
        return cast(int, result.scalar())

    @contextlib.asynccontextmanager
    async def transaction(self) -> AsyncSessionTransaction:
        self._transaction.change_strategy(TransactionStrategy.KEEP_ALIVE)
        try:
            yield await self._transaction.__aenter__()
        except Exception as ex:
            await self._transaction.__aexit__(*sys.exc_info())
            raise ex
        finally:
            await self._transaction.close()
            self._transaction.change_strategy(DEFAULT_STRATEGY)


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
