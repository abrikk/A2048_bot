from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from tgbot.models.user import User


class UserDB(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        session = data["session"]
        user = await session.get(User, obj.from_user.id)

        if user:
            if user.first_name != obj.from_user.first_name:
                user.first_name = obj.from_user.first_name
            if user.last_name != obj.from_user.last_name:
                user.last_name = obj.from_user.last_name
            if user.username != obj.from_user.username:
                user.username = obj.from_user.username
            await session.commit()

        data["user"] = user if user else None

    async def post_process(self, obj, data, *args):
        del data["user"]
