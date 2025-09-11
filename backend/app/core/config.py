from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: AnyUrl
    REDIS_URL: str | None = None
    OPENSEARCH_URL: str | None = None

    # OIDC (dev via Keycloak) / Cognito (prod)
    OIDC_AUDIENCE: str | None = None
    OIDC_JWKS_URL: str | None = None
    COGNITO_AUDIENCE: str | None = None
    COGNITO_JWKS_URL: str | None = None

    AWS_REGION: str = "eu-central-1"
    S3_BUCKET: str | None = None
    S3_UPLOAD_PREFIX: str = "uploads/"

    API_PREFIX: str = "/api"


class Config:
    env_file = ".env"


settings = Settings()

