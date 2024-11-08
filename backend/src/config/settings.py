import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    TEAMS_DIR: Path = DATA_DIR / "teams"
    GAMES_DIR: Path = DATA_DIR / "games"

    class Config:
        env_file: str = ".env"


settings = Settings()
