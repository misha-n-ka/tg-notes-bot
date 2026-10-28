---
last_mapped_commit: 5f0af69c618c372578aadb50c8e595cb9edd01b1
last_mapped_at: 2026-10-27
---
# Technology Stack

**Analysis Date:** 2026-10-27

## Languages

**Primary:**
- Python 3.12+ — пакет `notes_bot/`, тесты `tests/` и хук `.codex/hooks/ruff_after_edit.py`; минимум задан в `pyproject.toml`.

**Secondary:**
- Markdown — требования и инструкции в `docs/`, `README.md`, `AGENTS.md`.
- TOML и JSON — конфигурация инструментов в `pyproject.toml`, `.codex/hooks.json`.

## Runtime

**Environment:**
- CPython 3.12+ требуется по `pyproject.toml`; фактический интерпретатор окружения при картировании не запускался.
- Исполняемый код приложения ограничен `notes_bot/config.py`; точки входа бота в отслеживаемых файлах нет.

**Package Manager:**
- uv — менеджер окружения и зависимостей; `README.md` описывает локальную установку версии 0.13.1.
- Lockfile: `uv.lock` присутствует; версии ниже взяты из lockfile, а не из установленного окружения.

## Frameworks

**Core:**
- aiogram 3 — единственная прямая runtime-зависимость: `>=3.31,<4` в `pyproject.toml`, 3.31.0 в `uv.lock`.
- Telegram-обработчики ещё не реализованы: aiogram объявлен для целевого MVP, но не импортируется в `notes_bot/config.py`.

**Testing:**
- pytest — диапазон `>=8,<10` в `pyproject.toml`, зафиксированная версия 9.1.1 в `uv.lock`.
- `unittest.mock` из стандартной библиотеки используется тестами хука в `tests/test_ruff_hook.py`.

**Build/Dev:**
- uv_build — backend сборки; диапазон `>=0.13.1,<0.14`, lockfile фиксирует 0.13.1 (`pyproject.toml`, `uv.lock`).
- Ruff — диапазон `>=0.14,<1`, lockfile фиксирует 0.17.0 (`pyproject.toml`, `uv.lock`).
- Ruff настроен на Python 3.12, длину строки 88 и правила `E`, `F`, `I` (`pyproject.toml`).

## Key Dependencies

**Critical:**
- Текущая логика настроек использует только `os`, `dataclasses`, `pathlib` из стандартной библиотеки (`notes_bot/config.py`).
- `Settings` хранит токен с `repr=False` и путь как `Path`; `load_settings()` проверяет непустые переменные (`notes_bot/config.py`).

**Infrastructure:**
- aiogram транзитивно использует aiohttp 3.14.5, pydantic 2.13.5 и magic-filter 1.0.12 (`uv.lock`).
- SQLite через стандартный `sqlite3` выбран в `docs/mvp.md`; модуль хранения ещё не реализован, отдельного DB-пакета в `pyproject.toml` нет.

## Configuration

**Environment:**
- `BOT_TOKEN` обязателен; `DATABASE_PATH` по умолчанию равен `data/notes.sqlite3` (`notes_bot/config.py`).
- Настройки читаются из `os.environ`; автоматической загрузки dotenv нет (`notes_bot/config.py`, `README.md`).
- Содержимое локальных секретов и окружения для карты не читалось; запрет определён в `AGENTS.md`.

**Build:**
- Backend собирает корневой модуль `notes_bot`, добавляет `tests/**` в исходный архив (`pyproject.toml`).
- Сборка sdist/wheel описана в `README.md`; артефакты `dist/` исключены через `.gitignore`.
- pytest использует `tests/`, корень в `pythonpath` и `--ignore=.env` (`pyproject.toml`).
- Хук после `apply_patch` запускает Ruff для изменённых Python-файлов (`.codex/hooks.json`, `.codex/hooks/ruff_after_edit.py`).

## Platform Requirements

**Development:**
- Python 3.12+, uv и подготовленные dev-зависимости; процедура для macOS/Linux приведена в `README.md`.
- Не устанавливать зависимости автоматически и не менять staging без отдельного поручения (`AGENTS.md`).

**Production:**
- Хостинг и production-процедура развёртывания не определены в `README.md` и `docs/roadmap.md`.
- Целевому боту нужны доступ к Telegram и записываемый файл SQLite; polling пока является планом (`docs/mvp.md`, `docs/architecture.md`).

---

*Stack analysis: 2026-10-27*
