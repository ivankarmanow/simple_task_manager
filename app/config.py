from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    db_uri: str

    model_config = SettingsConfigDict(env_file=".env")
