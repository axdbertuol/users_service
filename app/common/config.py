from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_version: str = Field(...)
    app_name: str = Field(...)
    app_port: int = Field(...)
    environment: str = Field(...)

    database_driver: str = Field(...)
    database_host: str = Field(...)
    database_port: int = Field(...)
    database_user: str = Field(...)
    database_password: str = Field(...)
    database_dbname: str = Field(...)

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", populate_by_name=True
    )

    def get_api_prefix(self):
        return f"/api/{self.api_version}"

    def get_sql_alch_dbconnstr(self):
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:5432/{self.database_dbname}"


# Initialize the settings
settings = Settings()
