import sentry_sdk
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update


class SentryContextMiddleware(BaseMiddleware):
    @staticmethod
    def setup_user(user_id: int, update: Update) -> None:
        sentry_sdk.set_user({
            'id': user_id,
            'update': update.to_python()
        })

    async def on_pre_process_update(self, update: Update, _) -> None:
        if (not update.message) or (not update.callback_query):
            return
        upd = update.message or update.callback_query
        self.setup_user(upd.from_user.id, update)
