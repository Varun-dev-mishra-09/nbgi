from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    app_name: str = 'NGBI API'
    api_v1_prefix: str = '/api/v1'
    secret_key: str
    access_token_expire_minutes: int = 60
    database_url: str
    redis_url: str

    google_client_id: str | None = None
    google_client_secret: str | None = None
    razorpay_key_id: str | None = None
    razorpay_key_secret: str | None = None
    paytm_mid: str | None = None
    paytm_merchant_key: str | None = None
    paytm_website: str = 'DEFAULT'


settings = Settings()
