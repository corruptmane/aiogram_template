from typing import Any

from app.models import User
from app.services.db_ctx import BaseRepo


class UserRepo(BaseRepo[User]):
    model = User

    async def get_user(self, user_id: int) -> User | None:
        model = self.model
        return await self.get_one(model.user_id == user_id)

    async def update_user(self, user_id: int, **kwargs: Any) -> None:
        return await self.update(self.model.user_id == user_id, **kwargs)

    async def not_active_user(self, user_id: int) -> None:
        return await self.update_user(user_id, active=False)
