from typing import Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    def __init__(self, environments: dict[str, Any]) -> None:
        self.environments = environments
        super().__init__()

    def update_environments(self, **new_environments: dict[str, Any]) -> None:
        self.environments.update(**new_environments)

    async def pre_process(self, obj: TelegramObject, data: dict[str, Any], *args: Any) -> None:
        data.update(**self.environments, update_environments=self.update_environments)
