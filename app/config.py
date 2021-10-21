from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
LOGGING_LEVEL = env.log_level("LOGGING_LEVEL")
WORK_PATH = Path(__file__).parent.parent

admins = list(map(int, env.list("ADMINS")))

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT")

POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT")
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")

POSTGRES_URI = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
