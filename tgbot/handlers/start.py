from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter
from aiogram_dialog import DialogManager, StartMode

from tgbot.config import Config
from tgbot.constants import ADMIN, USER
from tgbot.misc.states import Main
from tgbot.models.user import User


async def start_bot(message: types.Message, config: Config, session, dialog_manager: DialogManager):
    user_id = message.from_user.id
    user: User = await session.get(User, user_id)

    if not user:
        if user_id in config.tg_bot.admin_ids:
            role: str = ADMIN
        else:
            role: str = USER

        user = User(
            active=True,
            user_id=user_id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            last_name=message.from_user.last_name,
            role=role
        )

        session.add(user)
        await session.commit()

        await dialog_manager.start(state=Main.main, data={
            "first_name": user.first_name
        })

    else:
        await dialog_manager.start(state=Main.main, mode=StartMode.RESET_STACK)


def register_start(dp: Dispatcher):
    dp.register_message_handler(start_bot, CommandStart(), ChatTypeFilter(types.ChatType.PRIVATE))
