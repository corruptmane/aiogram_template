from typing import Generic, TypeVar, Type, Sequence, Any

from sqlalchemy import ScalarResult, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.infrastructure.db.models import BaseModel

Model = TypeVar('Model', bound=BaseModel, covariant=True, contravariant=False)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self.model = model
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def flush(self, *objects: Model) -> None:
        await self._session.flush(objects)

    async def _get_all(self, options: Sequence[ORMOption] = tuple(), as_unique: bool = False) -> Sequence[Model]:
        result: ScalarResult[Model] = await self._session.scalars(select(self.model).options(*options))
        if as_unique:
            result = result.unique()
        return result.all()

    async def _get_by_id(
            self,
            entity_id: Any,
            options: Sequence[ORMOption] = None,
            populate_existing: bool = False,
    ) -> Model:
        result = await self._session.get(self.model, entity_id, options=options, populate_existing=populate_existing)
        if result is None:
            raise NoResultFound()
        return result

    def _save_model(self, obj: Model) -> None:
        self._session.add(obj)
