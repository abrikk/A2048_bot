from dataclasses import dataclass

from environs import Env


@dataclass
class DbConfig:
    user: str
    password: str
    host: str
    port: int
    database: str


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Chats:
    errors_channel_id: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis_config: RedisConfig
    chats: Chats


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            port=env.int('DB_PORT'),
            database=env.str('DB_NAME')
        ),
        redis_config=RedisConfig(
            host=env.str('REDIS_HOST'),
            port=env.int('REDIS_PORT'),
            db=env.int('REDIS_DB'),
        ),
        chats=Chats(
            errors_channel_id=env.int('ERRORS_CHANNEL_ID')
        )
    )
