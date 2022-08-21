from typing import Any, Literal

from aiogram.dispatcher.middlewares import BaseMiddleware


class EnvironmentMiddleware(BaseMiddleware):
    def __init__(self, environments: dict[str, Any]) -> None:
        super(EnvironmentMiddleware, self).__init__()
        self.environments = environments

    def update_environments(self, **new_environments: dict[str, Any]) -> None:
        self.environments.update(**new_environments)

    async def trigger(self, action: str, *args: Any) -> Literal[True] | None:
        if action.startswith('pre_process_'):
            data: dict = args[-1][-1]
            dp = self.manager.dispatcher
            data.update(**self.environments, update_environments=self.update_environments, bot=dp.bot, dp=dp)
            return True
        return
