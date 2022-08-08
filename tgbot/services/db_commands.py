import datetime

from sqlalchemy import select, extract, and_, func
from sqlalchemy.orm import aliased

from tgbot.models.game_history import GameHistory


class DBCommands:
    def __init__(self, session):
        self.session = session

    current_season = datetime.datetime.now().year, datetime.datetime.now().month

    async def get_game_history(self, limit: int = 5, season: tuple[int, int] = current_season):
        gh1 = aliased(GameHistory, name="gh1")
        gh2 = aliased(GameHistory, name="gh2")

        sql = select(func.dense_rank().over(order_by=[gh1.score.desc(), gh1.moves_made]).label("rank"), gh1).select_from(gh1).join(
            gh2, gh1.user_id == gh2.user_id
        ).where(
            and_(
                extract("YEAR", gh1.created_at) == season[0],
                extract("MONTH", gh1.created_at) == season[1],
            )
        ).group_by(gh1).having(func.max(gh2.score) == gh1.score)

        sql = sql.order_by(gh1.score.desc(), gh1.moves_made).limit(limit)
        result = await self.session.execute(sql)
        scalars = result.all()
        return scalars

    async def get_user_history(self, user_id: int, limit: int = 4, offset: int = 0):
        sql = select(GameHistory).where(
            GameHistory.user_id == user_id
        ).order_by(GameHistory.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(sql)
        scalars = result.scalars().all()
        return scalars

    async def get_best_user_game(self, user_id: int):
        sql = select(GameHistory).where(
            GameHistory.user_id == user_id
        ).order_by(GameHistory.score.desc(), GameHistory.moves_made).limit(1)
        result = await self.session.execute(sql)
        scalars = result.scalars().first()
        return scalars
