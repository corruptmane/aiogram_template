from src.core.interfaces.dao.user import UserUpserter, UserNotActiveMarker, AllActiveUserIdsGetter
from src.core.models import dto


async def upsert_user(user: dto.User, dao: UserUpserter) -> dto.User:
    saved_user = await dao.upsert_user(user)
    await dao.commit()
    return saved_user


async def mark_user_not_active(user_id: int, dao: UserNotActiveMarker) -> None:
    await dao.mark_user_not_active(user_id)
    await dao.commit()


async def get_all_active_user_ids(dao: AllActiveUserIdsGetter) -> list[int]:
    return await dao.get_all_active_user_ids()
