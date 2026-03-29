import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


DOTENV = os.path.join(os.path.dirname(__file__), '../.env')


class Settings(BaseSettings):
    DRIVER: str
    LOGIN: str
    PASSWORD: str
    IPADDRESS: str
    DATABASE: str


    model_config = SettingsConfigDict(env_file=DOTENV)

    def get_db_url(self):
        return f"{self.DRIVER}://{self.LOGIN}:{self.PASSWORD}@{self.IPADDRESS}/{self.DATABASE}"

settings = Settings()


@lru_cache()
def get_settings():
    return Settings()