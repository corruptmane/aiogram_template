from typing import List, NoReturn

from sqlalchemy.sql.elements import False_, True_, and_

from app.models import User


async def add_user(user_id: int, full_name: str, mention: str) -> NoReturn:
    return await User(user_id=user_id, full_name=full_name, mention=mention).create()


async def get_user_by_user_id(user_id: int) -> User:
    return await User.get(user_id)


async def get_all_users() -> List[User]:
    return await User.query.gino.all()


async def get_admins() -> List[User]:
    return await User.query.where(
        and_(User.is_admin == True_(), User.is_banned == False_())
    ).gino.all()


async def update_user_mailing_status(user_id: int) -> NoReturn:
    user = await get_user_by_user_id(user_id)
    mailing = not user.mailing
    await user.update(mailing=mailing).apply()


async def update_user_role(user_id: int, role: str) -> NoReturn:
    user = await get_user_by_user_id(user_id)
    if role == "admin":
        kwargs = dict(is_admin=True, is_banned=False)
    elif role == "banned":
        kwargs = dict(is_admin=False, is_banned=True)
    else:
        kwargs = dict(is_admin=False, is_banned=False)
    await user.update(**kwargs).apply()


async def update_user_naming(user_id: int, full_name: str, mention: str) -> NoReturn:
    user = await get_user_by_user_id(user_id)
    await user.update(full_name=full_name, mention=mention).apply()
