from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    NAME_DB: str
    USER_DB: str
    PASSWORD_DB: str
    HOST: str
    PORT: str

    @property
    def database_url_asyncpg(self):
        return f"postgresql+asyncpg://{self.USER_DB}:{self.PASSWORD_DB}@{self.HOST}:{self.PORT}/{self.NAME_DB}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
