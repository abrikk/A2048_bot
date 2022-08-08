from sqlalchemy import Column, BigInteger, TIMESTAMP, func, ForeignKey, Integer

from tgbot.services.db_base import Base


class GameHistory(Base):
    __tablename__ = "game_history"
    game_history_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey('users.user_id', ondelete="CASCADE", onupdate="CASCADE"))
    board_size = Column(Integer, nullable=False)
    score = Column(BigInteger, nullable=False)
    moves_made = Column(Integer, nullable=False)
    max_num = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=func.now(),
                        onupdate=func.now(),
                        server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f'Game History (User ID: {self.user_id} - Score: {self.score} - Max number {self.max_num})'
