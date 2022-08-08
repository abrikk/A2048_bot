from aiogram import Dispatcher, types

from tgbot.models.user import User


async def user_check_active(member: types.ChatMemberUpdated, session):
    user_id = member.from_user.id
    is_active = member.new_chat_member.is_chat_member()
    user: User = await session.get(User, user_id)

    user.active = is_active
    await session.commit()


def register_is_active_user(dp: Dispatcher):
    dp.register_my_chat_member_handler(user_check_active)
