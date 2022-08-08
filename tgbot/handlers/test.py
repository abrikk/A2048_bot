from aiogram import types, Dispatcher
from aiogram.utils.markdown import hcode


async def test(message: types.Message):
    print(message.photo[-1].file_id)

def register_test(dp: Dispatcher):
    dp.register_message_handler(test, content_types="photo")
