---
last_mapped_commit: 5f0af69c618c372578aadb50c8e595cb9edd01b1
last_mapped_at: 2026-10-27
---
# Coding Conventions

**Analysis Date:** 2026-10-27

## Naming Patterns

**Files:**
- Используйте английские имена Python-модулей в `snake_case`: `notes_bot/config.py`, `tests/test_config.py`.
- Держите тесты отдельно в `tests/test_<module>.py`; пример для инструмента — `tests/test_ruff_hook.py`.

**Functions:**
- Используйте `snake_case`: `load_settings()` в `notes_bot/config.py`, `run_hook()` в `.codex/hooks/ruff_after_edit.py`.
- Имена тестов описывают проверяемое поведение: `test_token_not_in_settings_repr()` в `tests/test_config.py`.

**Variables:**
- Локальные переменные — `snake_case`; ключи окружения — `BOT_TOKEN`, `DATABASE_PATH` в `notes_bot/config.py`.

**Types:**
- Имена классов — `PascalCase`; `Settings` реализован через `dataclass` в `notes_bot/config.py`.
- Используйте стандартные аннотации, включая `str | None`, `Path`, `-> None`; образец — `tests/test_config.py`.

## Code Style

**Formatting:**
- Применяйте Ruff с длиной строки 88 и целевой версией `py312`: `pyproject.toml`.
- В текущем коде используются двойные кавычки и четыре пробела: `notes_bot/config.py`.
- Создавайте и редактируйте Python через `apply_patch`; порядок запуска хука и ручной fallback определяет `AGENTS.md`.

**Linting:**
- Набор правил Ruff — `E`, `F`, `I` в `pyproject.toml`.
- Хук `.codex/hooks/ruff_after_edit.py` запускает сначала `ruff format`, затем `ruff check` только для существующих Python-файлов из patch внутри корня.
- Перед завершением изменений Python обязательны общие Ruff-проверки из `AGENTS.md`; чужие файлы не форматируйте ради локальной задачи.

## Import Organization

**Order:**
1. Стандартная библиотека: `os`, `dataclasses`, `pathlib` в `notes_bot/config.py`.
2. Сторонние пакеты: `pytest` в `tests/test_config.py`.
3. Импорты проекта: `from notes_bot.config import load_settings` в `tests/test_config.py`.

**Path Aliases:**
- Алиасы не настроены; `pythonpath = ["."]` задан для pytest в `pyproject.toml`.

## Error Handling

**Patterns:**
- Проверяйте настройки на границе: `load_settings()` отклоняет отсутствующий/пустой токен и пустой путь через `ValueError` в `notes_bot/config.py`.
- Проверка `.strip()` определяет пустоту; исходное значение токена возвращается без изменения в `notes_bot/config.py`.
- Ошибки настроек называют ключ, не его значение; `Settings.bot_token` скрыт из `repr` через `field(repr=False)` в `notes_bot/config.py`.
- Утилита `.codex/hooks/ruff_after_edit.py` возвращает код 2 и пишет диагностические сообщения в stderr при сбое Ruff или входных данных.

## Logging

**Framework:** Прикладной логгер не настроен в `notes_bot/config.py`; хук использует `print(..., file=sys.stderr)` в `.codex/hooks/ruff_after_edit.py`.

**Patterns:**
- Не выводите токены и тексты заметок; правило закреплено в `AGENTS.md` и `docs/mvp.md`.
- Не читайте `.env`, реальные заметки и базы ради анализа; используйте вымышленные данные по `AGENTS.md`.

## Comments

**When to Comment:**
- Краткие модульные docstring описывают назначение: `notes_bot/__init__.py`, `notes_bot/config.py`, `.codex/hooks/ruff_after_edit.py`.
- Отдельного требования к docstring каждой функции в `pyproject.toml` нет; сохраняйте стиль ближайшего кода согласно `AGENTS.md`.

**JSDoc/TSDoc:** Не применимо; проект Python (`pyproject.toml`).

## Function Design

**Size:** Используйте прямые функции без дополнительного слоя ради локальной задачи; ограничение установлено `AGENTS.md`, пример — `load_settings()` в `notes_bot/config.py`.

**Parameters:** `load_settings()` читает окружение напрямую; `run_hook(event, root)` получает событие и корень явно в `.codex/hooks/ruff_after_edit.py`.

**Return Values:** Настройки возвращаются объектом `Settings`; хук возвращает целочисленный статус (`notes_bot/config.py`, `.codex/hooks/ruff_after_edit.py`).

## Module Design

**Exports:** Потребитель импортирует функцию из конкретного модуля в `tests/test_config.py`; `notes_bot/__init__.py` содержит только docstring.

**Barrel Files:** Публичные реэкспорты и `__all__` не заданы в `notes_bot/__init__.py`.

- Сохраняйте независимость будущего хранилища от Telegram; это архитектурное требование, а не уже реализованный слой (`docs/architecture.md`, `docs/plan.md`).
- Изменение контракта требует проверки непосредственных потребителей и тестов по `AGENTS.md`.

---

*Convention analysis: 2026-10-27*
