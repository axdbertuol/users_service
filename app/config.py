from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_version: str = Field("v1")
    app_name: str = Field("users_service")
    app_port: int = Field(3336)
    environment: str = Field("dev")

    database_driver: str = Field("postgresql")
    database_host: str = Field("localhost")
    database_port: int = Field(5432)
    database_user: str = Field("tester")
    database_password: str = Field("postgres")
    database_dbname: str = Field("test-db")

    kafka_url: str = Field("kafka:9092")
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", populate_by_name=True
    )

    def get_api_prefix(self):
        return f"/api/{self.api_version}"

    def get_sql_alch_dbconnstr(self):
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_dbname}"


# Initialize the settings
@lru_cache
def get_settings():
    return Settings()
