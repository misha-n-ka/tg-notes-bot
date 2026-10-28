---
last_mapped_commit: 5f0af69c618c372578aadb50c8e595cb9edd01b1
last_mapped_at: 2026-10-27
---
# Codebase Structure

**Analysis Date:** 2026-10-27

## Directory Layout

```text
tg-notes-bot/
├── notes_bot/              # Пакет приложения: __init__.py, config.py
├── tests/                  # test_config.py, test_ruff_hook.py
├── docs/                   # Требования, архитектура, план и прогресс
│   └── image/              # Изображения для документации
├── .agents/skills/         # Локальные навыки NotesBot
├── .codex/                 # Профиль, правила команд и хук Ruff
│   ├── hooks/              # ruff_after_edit.py
│   └── rules/              # notes-bot.rules
├── .planning/codebase/     # Карта существующего кода
├── AGENTS.md               # Правила работы в репозитории
├── README.md               # Подготовка окружения и команды проверок
├── pyproject.toml          # Метаданные, зависимости и настройки инструментов
├── uv.lock                 # Зафиксированные версии зависимостей
└── .gitignore              # Исключения секретов, локальных данных и артефактов
```

## Directory Purposes

**`notes_bot/`:**
- Код приложения расположен непосредственно в корне пакета, без `src/`.
- `notes_bot/config.py` содержит `Settings` и `load_settings()`.
- `notes_bot/__init__.py` содержит только docstring пакета.

**`tests/`:**
- Отдельные тестовые модули для настроек и инструментального хука.
- `tests/test_config.py` импортирует настройки обычным Python-импортом.
- `tests/test_ruff_hook.py` загружает `.codex/hooks/ruff_after_edit.py` через `runpy`.

**`docs/`:**
- Требования: `docs/mvp.md`; целевая схема: `docs/architecture.md`.
- Порядок этапов: `docs/roadmap.md`; шаги выбранного этапа: `docs/plan.md`.
- Фактическое состояние и результаты: `docs/progress.md`.
- Работа агента: `docs/agent-workflow.md`; общий обзор: `docs/about.md`.
- `docs/test-report.md` хранит отчёт ранее выполненных проверок.

**`.agents/skills/`:**
- `notes-task/SKILL.md`: один порученный этап реализации.
- `notes-review/SKILL.md`: ревью изменений.
- `notes-rules-check/SKILL.md`: проверка правил команд, не бизнес-логики.
- Загружать только навык текущего поручения (`AGENTS.md`).

## Key File Locations

**Entry Points:**
- У приложения нет исполняемой точки входа (`notes_bot/`, `pyproject.toml`).
- `.codex/hooks/ruff_after_edit.py`: исполняемый инструментальный хук.

**Configuration:**
- `pyproject.toml`: Python >=3.12, зависимости, uv_build, pytest и Ruff.
- `.codex/config.toml`: профиль ограничений агента.
- `.codex/hooks.json`: привязка Ruff к событию `apply_patch`.
- `.codex/rules/notes-bot.rules`: разрешения и ограничения команд.

**Core Logic:**
- `notes_bot/config.py`: существующий код приложения.

**Testing:**
- `tests/test_config.py`: переменные окружения, путь, безопасный repr.
- `tests/test_ruff_hook.py`: выбор файлов и ошибки хука.

## Naming Conventions

**Files:** Python-модули названы в `snake_case`; тесты имеют префикс `test_`
(`notes_bot/config.py`, `tests/test_config.py`).

**Directories:** пакет — `notes_bot`; функциональные Python-подпакеты не введены.
Документы GSD в `.planning/codebase/` используют имена в `UPPERCASE.md`.

## Where to Add New Code

**New Feature:** следовать только порученному пункту `docs/roadmap.md` и
`docs/plan.md`; новый функционал размещать в `notes_bot/`, тесты — в `tests/`.

**New Component/Module:** план этапа 2 задаёт `notes_bot/storage.py` и
`tests/test_storage.py`; этих файлов нет. Целевая схема дополнительно задаёт
`notes_bot/handlers.py` и `notes_bot/__main__.py` (`docs/architecture.md`),
также отсутствующие. Не создавать их в рамках картирования.

**Utilities:** общего модуля утилит нет; не вводить его без необходимости.
Сохранять локальные функции в соответствующем модуле (`AGENTS.md`).

## Special Directories

**`.planning/codebase/`:**
- Назначение: Markdown-карта существующего кода для планирования GSD.
- Содержимое создаётся картированием; Git-операции требуют отдельного поручения.

**Локальное окружение и артефакты:**
- `.venv/`, `.tools/`, `.python/`, `.uv-cache/`, `dist/`, `build/` исключены
  через `.gitignore`; наличие и содержимое каждого каталога не проверялись.
- `/data/` и файлы SQLite исключены через `.gitignore`; реальные данные не читать.
- Файлы `.env` и `.env.*` исключены из Git; их содержимое не является входом
  для карты и запрещено к чтению (`AGENTS.md`).

---

*Structure analysis: 2026-10-27*
