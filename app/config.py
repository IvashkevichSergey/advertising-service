from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class for using environment variables from dotenv file"""
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_JWT_KEY: str

    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://" \
               f"{self.DB_USER}:" \
               f"{self.DB_PASS}@" \
               f"{self.DB_HOST}:" \
               f"{self.DB_PORT}/" \
               f"{self.DB_NAME}"

    class Config:
        env_file = ".env"
        extra = 'allow'


settings = Settings()
