from starlette.config import Config

from starlette.datastructures import Secret


try:
    Config = Config(".env")

except FileNotFoundError:
    Config = Config()


DATABASE_URI = Config("DATABASE_URI", cast=Secret)

TEST_DATABASE_URI = Config("TEST_DATABASE_URI", cast=Secret)
