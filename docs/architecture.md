# Архитектура NotesBot

Схема описывает целевую архитектуру MVP. Состояние реализации модулей —
в [progress.md](progress.md).

```mermaid
flowchart TD
    Telegram["Telegram Bot API"]

    subgraph App["Приложение notes_bot"]
        Main["__main__.py<br/>Подготовка БД и запуск polling"]
        Config["config.py<br/>Чтение и проверка настроек"]
        Handlers["handlers.py<br/>Команды и ответы пользователю"]
        Storage["storage.py<br/>Операции с заметками"]
    end

    Env["Переменные окружения<br/>Токен и путь к БД"]
    DB[("SQLite<br/>Таблица notes")]

    Env --> Config
    Config -->|"Настройки"| Main
    Main -->|"Инициализация"| Storage
    Main -->|"Подключение обработчиков"| Handlers
    Main -->|"Запуск polling"| Telegram

    Telegram -->|"Сообщения и команды"| Handlers
    Handlers -->|"Сохранить / список / поиск / удалить<br/>Всегда с user_id"| Storage
    Storage -->|"Запросы с параметрами"| DB
    DB -->|"Данные или результат удаления"| Storage
    Storage -->|"Результат операции"| Handlers
    Handlers -->|"Ответ пользователю"| Telegram
```

`handlers.py` отвечает за Telegram-интерфейс, `storage.py` — за данные и ограничение доступа по владельцу. `__main__.py` связывает модули и управляет запуском.

Хранилище тестируется с временной SQLite-БД, обработчики — без обращения к Telegram.
