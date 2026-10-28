---
last_mapped_commit: 5f0af69c618c372578aadb50c8e595cb9edd01b1
last_mapped_at: 2026-10-27
---
# Testing Patterns

**Analysis Date:** 2026-10-27

## Test Framework

**Runner:**
- pytest с ограничением `>=8,<10` в группе `dev`: `pyproject.toml`.
- Конфигурация задаёт `testpaths = ["tests"]`, `pythonpath = ["."]`, `addopts = "--ignore=.env"`: `pyproject.toml`.
- Исключение `.env` сохраняйте: обход запрещённого файла мешает запуску pytest; причина описана в `docs/progress.md`.

**Assertion Library:** Обычный `assert`, `pytest.raises`, проверки mock-вызовов (`tests/test_config.py`, `tests/test_ruff_hook.py`).

**Run Commands:**
```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m pytest tests/test_config.py -q
.venv/bin/python -m pytest tests/test_ruff_hook.py -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/python -m compileall -q notes_bot tests
uv build --no-build-isolation
```
- Это документированные команды из `AGENTS.md`; при составлении карты они не выполнялись.
- После изменения Python, тестов, зависимостей или параметров сборки весь набор проверок обязателен по `AGENTS.md`.
- Для документационных изменений достаточно статических проверок по `AGENTS.md`; не устанавливайте недостающие инструменты автоматически.

## Test File Organization

**Location:** Отдельный каталог `tests/`, настройки находятся в `pyproject.toml`.

**Naming:** `test_<module>.py`; функции `test_<behavior>()` в `tests/test_config.py` и `tests/test_ruff_hook.py`.

**Structure:**
```text
tests/
├── test_config.py       # настройки приложения
└── test_ruff_hook.py    # инструмент Ruff после patch
```

## Test Structure

**Suite Organization:**
```python
@pytest.mark.parametrize("database_path", ["", "   ", "\t\n"])
def test_blank_database_path(
    monkeypatch: pytest.MonkeyPatch, database_path: str
) -> None:
    monkeypatch.setenv("BOT_TOKEN", "test-token")
    monkeypatch.setenv("DATABASE_PATH", database_path)

    with pytest.raises(ValueError, match="DATABASE_PATH"):
        load_settings()
```
- Образец взят из `tests/test_config.py`; применяйте parametrization для набора пустых значений.
- Классы тестов и ручной lifecycle setup/teardown не используются в `tests/test_config.py` и `tests/test_ruff_hook.py`.
- Изолируйте окружение через `monkeypatch`, файловую систему через `tmp_path` (`tests/test_config.py`, `tests/test_ruff_hook.py`).

## Mocking

**Framework:** `unittest.mock.patch` в `tests/test_ruff_hook.py` и fixture `monkeypatch` pytest в `tests/test_config.py`.

**Patterns:**
```python
with patch("subprocess.run") as run:
    run.return_value.returncode = 0
    assert hook(event, tmp_path) == 0
```
- В `tests/test_ruff_hook.py` дополнительно сравниваются точные аргументы вызовов Ruff и отсутствие вызовов при patch документации.

**What to Mock:** Подменяйте процессы Ruff и окружение; тесты не должны требовать реальный токен или запуск внешнего инструмента (`tests/test_config.py`, `tests/test_ruff_hook.py`).

**What NOT to Mock:** Файловые границы хука проверяются на реальных временных каталогах; `Path` сравнивается напрямую (`tests/test_ruff_hook.py`, `tests/test_config.py`).

## Fixtures and Factories

**Test Data:** Вымышленные токены, временные пути, события `tool_input.command` с маркерами patch (`tests/test_config.py`, `tests/test_ruff_hook.py`).

**Location:** Fixture `hook` находится в `tests/test_ruff_hook.py` и загружает `run_hook` через `runpy.run_path()` из `.codex/hooks/ruff_after_edit.py`.

- Общий `conftest.py` среди текущих отслеживаемых тестов отсутствует (`tests/`).
- Fixture `capsys` проверяет передачу ошибки Ruff в stderr в `tests/test_ruff_hook.py`.

## Coverage

**Requirements:** Числовой порог покрытия и конфигурация coverage не заданы в `pyproject.toml`.

**View Coverage:** Команда покрытия в `pyproject.toml` не настроена; дополнительных зависимостей ради карты не требуется.

- `tests/test_config.py` содержит 10 случаев с учётом parametrization: пустой токен, путь по умолчанию, произвольный путь, скрытие токена в repr, пустой путь.
- `tests/test_ruff_hook.py` содержит 4 теста: выбор Python-файлов и порядок команд, пропуск документации, отсутствие Ruff, ошибка линтера.
- `docs/progress.md` фиксирует успешный запуск 14 тестов от 19 октября 2026 года; это исторический результат, не проверка текущего сеанса.

## Test Types

**Unit Tests:** Настройки окружения и логика инструмента проверяются в `tests/test_config.py`, `tests/test_ruff_hook.py`.

**Integration Tests:** Хранилище и обработчики ещё не реализованы; соответствующих тестов нет, что соответствует границе этапа (`docs/progress.md`).

**E2E Tests:** Настоящий Telegram API в тестах не используется; сетевой запуск требует отдельного разрешения (`AGENTS.md`).

## Common Patterns

**Async Testing:** Текущие тесты синхронные (`tests/test_config.py`, `tests/test_ruff_hook.py`); async-плагин не объявлен в `pyproject.toml`.

**Error Testing:** Используйте `pytest.raises(ValueError, match=...)`; для ошибки токена проверяется полное имя ключа регулярным выражением `r"\bBOT_TOKEN\b"` (`tests/test_config.py`).

- Для будущего хранилища предусмотрены временные файловые SQLite-БД и проверки владельца, исходного текста, последних 10 записей и повторной инициализации (`docs/plan.md`). Эти тесты пока не существуют.
- Будущие обработчики проверяйте без настоящего Telegram API; требования к кириллице, `%`/`_`, emoji и ошибочным командам перечислены в `AGENTS.md`, `docs/mvp.md`.

---

*Testing analysis: 2026-10-27*
