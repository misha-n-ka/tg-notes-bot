"""Application settings."""

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Settings:
    bot_token: str = field(repr=False)
    database_path: Path


def load_settings() -> Settings:
    bot_token = os.environ.get("BOT_TOKEN", "")
    if not bot_token.strip():
        raise ValueError("BOT_TOKEN не задан или пуст.")

    database_path = os.environ.get("DATABASE_PATH", "data/notes.sqlite3")
    if not database_path.strip():
        raise ValueError("DATABASE_PATH не должен быть пустым.")

    return Settings(bot_token=bot_token, database_path=Path(database_path))
