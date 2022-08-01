from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject

from tgbot.config import Config


class ConfigMiddleware(LifetimeControllerMiddleware):
    def __init__(self, config: Config):
        super().__init__()
        self.config = config

    async def pre_process(self, obj: TelegramObject, data: Dict[str, Any], *args: Any) -> None:
        data["config"] = self.config
