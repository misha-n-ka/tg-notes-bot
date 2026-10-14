# NotesBot

Telegram-бот для сохранения, просмотра, поиска и удаления текстовых заметок.

Сейчас реализованы каркас пакета и загрузка настроек. Хранилище SQLite, команды
Telegram и запуск бота появятся на следующих этапах. Требования и порядок работы:
[MVP](docs/mvp.md), [архитектура](docs/architecture.md),
[план реализации](docs/implementation-plan.md).

## Подготовка окружения

Нужны Python 3.12+ и uv. Если uv уже установлен, использовать его. Для локальной
установки инструментов внутри проекта на macOS/Linux выполнить из корня:

```sh
python3 -m pip install --target .tools/uv --only-binary=:all: 'uv==0.13.1'
export PATH="$PWD/.tools/uv/bin:$PATH"
export UV_CACHE_DIR="$PWD/.uv-cache"
export UV_PYTHON_INSTALL_DIR="$PWD/.python"
uv python install 3.12 --no-bin
uv sync --locked --python 3.12 --no-install-project
```

`export` действует только в текущем shell. После открытия нового терминала
повторить три команды `export` из корня проекта. Python установлен в `.python/`,
инструменты в `.tools/`, зависимости в `.venv/`; эти каталоги исключены из Git.
`--no-install-project` устанавливает зависимости без установки самого NotesBot.
Версии зависимостей зафиксированы в `uv.lock`.

## Настройки

| Переменная | Назначение | Значение по умолчанию |
|---|---|---|
| `BOT_TOKEN` | Токен Telegram-бота; обязателен и не может быть пустым | Нет |
| `DATABASE_PATH` | Непустой путь к файлу SQLite | `data/notes.sqlite3` |

Пример передачи настроек в текущий shell:

```sh
export BOT_TOKEN='replace-with-your-telegram-bot-token'
export DATABASE_PATH='data/notes.sqlite3'
```

`.env.example` — шаблон названий переменных. Приложение не читает `.env`
автоматически. Реальный токен не помещать в отслеживаемые файлы, команды для
публикации, логи или отчёты. `load_settings()` проверяет наличие токена; проверка
его подлинности через Telegram в этот этап не входит.

## Проверки

Из корня проекта с подготовленным окружением:

```sh
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/python -m compileall -q notes_bot tests
.venv/bin/python -m pytest -q
uv build --no-build-isolation
```

Сборка создаёт sdist и wheel в `dist/`, используя build backend `uv_build`,
установленный вместе с dev-зависимостями. Тесты настроек используют вымышленные
значения и не обращаются к Telegram.

Правила разработки: [AGENTS.md](AGENTS.md). Рабочая ветка — `develop`.
