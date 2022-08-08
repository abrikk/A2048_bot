from typing import Optional, Any, Dict

from aiogram.types import ContentType

from aiogram_dialog.manager.manager import DialogManager
from aiogram_dialog.manager.protocols import MediaAttachment, MediaId

from aiogram_dialog.widgets.media import Media
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.when import WhenCondition


class DynamicMediaFileId(Media):
    def __init__(
            self,
            *,
            file_id: Text,
            type: ContentType = ContentType.PHOTO,
            media_params: Dict = None,
            when: WhenCondition = None,
    ):
        super().__init__(when)
        self.file_id = file_id
        self.type = type
        self.media_params = media_params or {}

    async def _render_media(
            self,
            data: Any,
            manager: DialogManager
    ) -> Optional[MediaAttachment]:
        file_id = MediaId(file_id=await self.file_id.render_text(data, manager), file_unique_id=None)

        return MediaAttachment(
            type=self.type,
            file_id=file_id,
            **self.media_params,
        )
