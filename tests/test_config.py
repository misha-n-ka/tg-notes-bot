from pathlib import Path

import pytest

from notes_bot.config import load_settings


@pytest.mark.parametrize("token", [None, "", "   ", "\t\n"])
def test_missing_token(monkeypatch: pytest.MonkeyPatch, token: str | None) -> None:
    if token is None:
        monkeypatch.delenv("BOT_TOKEN", raising=False)
    else:
        monkeypatch.setenv("BOT_TOKEN", token)

    with pytest.raises(ValueError, match=r"\bBOT_TOKEN\b"):
        load_settings()


def test_default_database_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    settings = load_settings()

    assert settings.bot_token == "test-token"
    assert settings.database_path == Path("data/notes.sqlite3")


def test_custom_database_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    database_path = tmp_path / "custom.sqlite3"
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("DATABASE_PATH", str(database_path))

    settings = load_settings()

    assert settings.database_path == database_path


def test_token_not_in_settings_repr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-secret-token")
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    settings = load_settings()

    assert "test-secret-token" not in repr(settings)


@pytest.mark.parametrize("database_path", ["", "   ", "\t\n"])
def test_blank_database_path(
    monkeypatch: pytest.MonkeyPatch, database_path: str
) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("DATABASE_PATH", database_path)

    with pytest.raises(ValueError, match="DATABASE_PATH"):
        load_settings()
