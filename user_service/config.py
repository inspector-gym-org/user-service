from pydantic import BaseSettings


class Settings(BaseSettings):
    app_root_path: str

    mongo_host: str
    mongo_port: int

    mongo_user: str
    mongo_pass: str

    mongo_database_name: str


settings = Settings()  # type: ignore[call-arg]