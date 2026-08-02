from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001


class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 1
    max_overflow: int = 10


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    token_expire_minutes: int = 60


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env-template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_",
    )
    run: RunConfig = RunConfig()
    api_v1_prefix: str = "/api/v1"
    auth_jwt: AuthJWT = AuthJWT()
    db: DbSettings


settings = Settings()
