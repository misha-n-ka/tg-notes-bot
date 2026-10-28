---
last_mapped_commit: 5f0af69c618c372578aadb50c8e595cb9edd01b1
last_mapped_at: 2026-10-27
---
# External Integrations

**Analysis Date:** 2026-10-27

## APIs & External Services

**Telegram:**
- Telegram Bot API — целевая внешняя интеграция для личных текстовых заметок (`docs/mvp.md`).
- SDK/Client: aiogram `>=3.31,<4`, зафиксирован 3.31.0 (`pyproject.toml`, `uv.lock`).
- Auth: имя переменной `BOT_TOKEN`; `load_settings()` проверяет наличие, но не подлинность токена (`notes_bot/config.py`, `README.md`).
- Обработчики и polling не реализованы; текущий код приложения не выполняет запросы к Telegram (`notes_bot/`, `docs/progress.md`).
- LLM и загрузка содержимого ссылок исключены из MVP (`docs/mvp.md`).

## Data Storage

**Databases:**
- SQLite — выбранная файловая БД, пока без реализованного хранилища (`docs/mvp.md`, `docs/plan.md`).
- Connection: `DATABASE_PATH`, по умолчанию `data/notes.sqlite3`; сейчас путь только возвращается настройками (`notes_bot/config.py`).
- Client: стандартный `sqlite3`; план требует открывать и закрывать соединение внутри каждой операции рабочего потока (`docs/mvp.md`).
- Контракт будущего хранилища описан в `docs/plan.md`; это не существующая интеграция.

**File Storage:**
- Внешнее файловое хранилище не объявлено в `pyproject.toml` и `docs/mvp.md`.
- Локальные БД, SQLite sidecar-файлы и `data/` исключены из Git (`.gitignore`); реальные файлы данных для карты не читались.

**Caching:**
- Прикладного кэша в `notes_bot/config.py` нет; Redis и другие cache-сервисы в `pyproject.toml` не объявлены.
- `.uv-cache/` — только локальный кэш инструментов, исключённый в `.gitignore`.

## Authentication & Identity

**Auth Provider:**
- Отдельная система аккаунтов не предусмотрена (`docs/mvp.md`).
- Будущий владелец заметки определяется по Telegram `from_user.id`, не по аргументу команды (`docs/mvp.md`, `AGENTS.md`).
- Ограничение чтения, поиска и удаления по владельцу пока является требованием; обработчиков и хранилища нет (`docs/progress.md`).
- `Settings.bot_token` исключён из `repr`, но само значение доступно вызывающему коду как поле (`notes_bot/config.py`).

## Monitoring & Observability

**Error Tracking:**
- Внешний трекер ошибок не объявлен в `pyproject.toml`; SDK мониторинга в `notes_bot/config.py` не используется.

**Logs:**
- Логирование приложения пока не реализовано в `notes_bot/config.py`.
- Запрещено логировать токены и тексты заметок; хранение не должно подтверждаться при ошибке (`AGENTS.md`, `docs/mvp.md`).

## CI/CD & Deployment

**Hosting:**
- Платформа размещения и production-конфигурация не определены (`README.md`, `docs/roadmap.md`).

**CI Pipeline:**
- В отслеживаемой структуре нет конфигурации CI; локальные команды проверок приведены в `README.md` и `AGENTS.md`.
- `.codex/hooks.json` подключает локальный Ruff-хук, а не серверный CI.

## Environment Configuration

**Required env vars:**
- `BOT_TOKEN` — обязательное непустое значение (`notes_bot/config.py`).
- `DATABASE_PATH` — необязательная переменная с непустым значением, если задана (`notes_bot/config.py`).

**Secrets location:**
- Приложение получает секрет из переменных окружения; `.env` не загружается автоматически (`README.md`, `notes_bot/config.py`).
- `.env` и `.env.*` исключены через `.gitignore`; доступ агентов к содержимому запрещён в `AGENTS.md`.
- Не помещать токены, реальные заметки или БД в карту и отслеживаемые файлы (`AGENTS.md`).

## Webhooks & Callbacks

**Incoming:**
- HTTP endpoints и webhook-обработчики отсутствуют; целевой способ получения событий — polling (`docs/architecture.md`).

**Outgoing:**
- Исходящие Telegram-вызовы ещё не реализованы; настройки не обращаются к сети (`notes_bot/config.py`, `docs/progress.md`).
- Проверять будущих обработчиков без настоящего Telegram API; реальный сетевой запуск требует отдельного разрешения (`AGENTS.md`).

---

*Integration audit: 2026-10-27*
