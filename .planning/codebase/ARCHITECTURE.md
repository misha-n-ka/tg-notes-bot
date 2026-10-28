---
last_mapped_commit: 5f0af69c618c372578aadb50c8e595cb9edd01b1
last_mapped_at: 2026-10-27
---
<!-- refreshed: 2026-10-27 -->
# Architecture

**Analysis Date:** 2026-10-27

## System Overview

```text
Вызывающий код / тесты
       │
       ▼
notes_bot/config.py: load_settings()
       │ читает os.environ и проверяет строки
       ▼
notes_bot/config.py: Settings(bot_token, database_path)
```

Реализованный пакет содержит настройки и маркер пакета `notes_bot/__init__.py`.
`docs/architecture.md` описывает целевой MVP, а не работающий Telegram-процесс.
Хранилище, обработчики, polling и исполняемая точка входа отсутствуют; это
соответствует статусу этапов в `docs/progress.md`.

## Component Responsibilities

| Component | Responsibility | File |
|-----------|----------------|------|
| `load_settings()` | Чтение и проверка переменных окружения | `notes_bot/config.py` |
| `Settings` | Передача токена и пути к файлу БД | `notes_bot/config.py` |
| Пакет | Обозначение Python-пакета без побочных действий | `notes_bot/__init__.py` |
| `run_hook()` | Форматирование и lint изменённых Python-файлов | `.codex/hooks/ruff_after_edit.py` |

## Pattern Overview

**Overall:** небольшой Python-пакет с отдельным модулем настроек.

**Key Characteristics:**
- `notes_bot/config.py` использует только стандартную библиотеку.
- Загрузка окружения явная: импорт модуля сам по себе настройки не читает.
- Настройки возвращаются dataclass-объектом, путь представлен `pathlib.Path`.
- Инструментальный хук `.codex/hooks/ruff_after_edit.py` отделён от приложения.

## Layers

**Application configuration:**
- Location: `notes_bot/config.py`.
- Contains: `Settings`, `load_settings()`.
- Depends on: `os`, `dataclasses`, `pathlib`.
- Used by: `tests/test_config.py`; потребителя запуска в приложении нет.

**Development tooling:**
- Location: `.codex/hooks/ruff_after_edit.py`, `.codex/hooks.json`.
- При событии `apply_patch` извлекает существующие `.py` внутри корня и запускает
  Ruff format, затем check через `subprocess.run`.
- Проверяется отдельно в `tests/test_ruff_hook.py`.

## Data Flow

### Settings Loading

1. `load_settings()` получает `BOT_TOKEN` из `os.environ` (`notes_bot/config.py`).
2. Отсутствующая или пробельная строка вызывает `ValueError`.
3. `DATABASE_PATH` берётся из окружения или получает значение по умолчанию;
   пустой путь также вызывает `ValueError`.
4. Возвращается `Settings` с исходным токеном и преобразованным в `Path` путём.

**State Management:** глобальных экземпляров настроек и БД в `notes_bot/` нет.
`Settings` — обычный изменяемый dataclass; `bot_token` исключён из `repr`.

## Key Abstractions

**Settings:** `notes_bot/config.py` содержит два обязательных поля конструктора:
`bot_token: str`, `database_path: Path`. Значение пути по умолчанию задаёт
`load_settings()`, а не dataclass.

## Entry Points

**Application:** исполняемая точка входа отсутствует. В `pyproject.toml` нет
`project.scripts`, а `notes_bot/__main__.py` отсутствует.

**Tooling:** `.codex/hooks/ruff_after_edit.py` читает JSON из stdin при прямом
запуске; его основной callable — `run_hook(event, root)`.

## Architectural Constraints

- **Threading:** работающего event loop и SQLite-кода нет. Для реализации MVP
  `docs/mvp.md` требует `asyncio.to_thread` и соединение внутри каждой операции.
- **Module boundaries:** целевой `storage.py` не должен зависеть от Telegram;
  `handlers.py` отвечает за интерфейс, `__main__.py` — связывание модулей
  (`docs/architecture.md`). Эти модули пока не реализованы.
- **Scope:** следующий отдельный этап ограничен созданием и чтением заметок
  (`docs/plan.md`); карта кода не разрешает его реализацию.
- **Dependencies:** не вводить новый слой или библиотеку ради локальной задачи
  (`AGENTS.md`).

## Anti-Patterns

Подтверждённых архитектурных антипаттернов в `notes_bot/config.py` не обнаружено
при статическом чтении. Не трактовать целевую схему `docs/architecture.md`
как существующую реализацию и не смешивать Telegram с хранением при расширении.

## Error Handling

**Strategy:** `notes_bot/config.py` явно выбрасывает `ValueError` с именем
неверной переменной без включения её значения. Перехвата в приложении пока нет.
Хук `.codex/hooks/ruff_after_edit.py` возвращает ненулевой код и пишет ошибки
в stderr при отсутствии Ruff, ошибке subprocess или некорректном событии.

## Cross-Cutting Concerns

**Logging:** подсистема логирования приложения не реализована (`notes_bot/`).
**Validation:** проверяется непустота настроек; подлинность токена не проверяется.
**Authentication:** Telegram-авторизация отсутствует; требование владельца через
`from_user.id` и ограничения всех операций по `user_id` задано в `docs/mvp.md`.
**Secrets:** `.env` не загружается приложением; читать его агенту запрещено
(`AGENTS.md`). Не добавлять токен и тексты заметок в логи.

---

*Architecture analysis: 2026-10-27*
