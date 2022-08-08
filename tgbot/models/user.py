from sqlalchemy import Column, BigInteger, String, TIMESTAMP, func, SmallInteger, Boolean

from tgbot.constants import CLASSIC_THEME, USER, CLASSIC_CONTROLLERS, CLASSIC_NUMBERS
from tgbot.services.db_base import Base


class User(Base):
    __tablename__ = "users"
    active = Column(Boolean, nullable=False)
    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(length=128), nullable=False)
    last_name = Column(String(length=128), nullable=True)
    username = Column(String(length=128), nullable=True, unique=True)
    role = Column(String(length=128), default=USER)
    theme = Column(String(length=128), default=CLASSIC_THEME)
    controllers = Column(String(length=128), default=CLASSIC_CONTROLLERS)
    numbers_style = Column(String(length=128), default=CLASSIC_NUMBERS)
    rating = Column(SmallInteger, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=func.now(),
                        onupdate=func.now(),
                        server_default=func.now())

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f'User (ID: {self.user_id} - {self.first_name})'
