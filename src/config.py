from os import environ

APP_META = dict(
    title="Book-Track API",
    description="Track your favourite literature list!",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://opensource.org/license/mit",
    },
)

DATABASE_URL = (
    "postgresql+asyncpg://"
    "{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    "postgresql:5432/{POSTGRES_DB}"
).format(**environ)

JWT_TOKEN_URL = "auth/login"
JWT_TOKEN_SECRET = environ.get("JWT_TOKEN_SECRET")
JWT_TOKEN_LIFETIME = 7 * 24 * 3600

URL_ALIAS_LENGTH = 6
IS_E2E = environ.get("E2E_ACTIVE")
