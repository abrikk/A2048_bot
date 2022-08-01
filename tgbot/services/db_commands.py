from sqlalchemy import select

from tgbot.models.user import User


class DBCommands:
    def __init__(self, session):
        self.session = session

    async def get_user(self, user_id: int):
        sql = select(User).where(User.user_id == user_id)
        request = await self.session.execute(sql)
        user = request.scalar()
        return user

    async def add_user(self,
                       user_id: int,
                       first_name: str,
                       last_name: str = None,
                       username: str = None,
                       role: str = 'user'
                       ) -> 'User':
        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    role=role)
        self.session.add(user)
        return user
