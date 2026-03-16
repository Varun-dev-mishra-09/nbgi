from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', 'backend/.env', '.env.example', 'backend/.env.example'),
        extra='ignore',
    )

    app_name: str = 'NGBI API'
    api_v1_prefix: str = '/api/v1'
    secret_key: str = 'dev-only-change-me'
    access_token_expire_minutes: int = 60
    database_url: str = 'sqlite:///./ngbi.db'
    redis_url: str = 'redis://localhost:6379/0'

    google_client_id: str | None = None
    google_client_secret: str | None = None
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None
    paytm_mid: str | None = None
    paytm_merchant_key: str | None = None
    paytm_website: str = 'DEFAULT'


settings = Settings()
