from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BDS API"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/bds"
    razorpay_key_id: str = "rzp_test_placeholder"
    razorpay_key_secret: str = "test_secret_placeholder"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
