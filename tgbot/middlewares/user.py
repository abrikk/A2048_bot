from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.user import User


class UserDB(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        session = data["session"]
        user = await session.get(User, obj.from_user.id)
        data["user"] = user if user else None

    async def post_process(self, obj, data, *args):
        del data["user"]
