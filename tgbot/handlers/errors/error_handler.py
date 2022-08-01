import io
import traceback

from aiogram import Dispatcher, types
from aiogram.types import Update
from aiogram.utils.markdown import hcode

from tgbot.config import Config


def exc_file() -> bytes:
    output = io.StringIO()
    output.write(traceback.format_exc())
    return output.getvalue().encode("utf-8")


async def errors_handler(update: Update, exception: Exception, config: Config):
    caption = f"An exception of type {hcode(type(exception).__name__)} occurred.\n\n" \
              f"⚠️ Error: {hcode(exception)}"

    await update.bot.send_document(
        chat_id=config.chats.errors_channel_id,
        document=types.InputFile(io.BytesIO(exc_file()), filename="traceback.txt"),
        caption=caption
    )


def register_error_handler(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
