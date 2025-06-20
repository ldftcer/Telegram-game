# Установка и запуск бота "Мафиозное Казино"

## Требования
- Python 3.10+
- pip (Python package manager)
- Telegram-бот (токен через @BotFather)
- (Опционально) [ngrok](https://ngrok.com/) для публичного доступа к картинкам карт

## Шаг 1. Клонирование и подготовка
1. Скачайте или клонируйте репозиторий:
   ```bash
   git clone <ваш-репозиторий>
   cd "Telegram game"
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## Шаг 2. Настройка
1. Откройте файл `config.py` и укажите:
   - `TOKEN` — токен вашего Telegram-бота
   - Другие параметры по необходимости
2. Убедитесь, что в папке `cards/` есть все PNG-файлы карт (36 штук, например: `6♧.png`, `Q♡.png` и т.д.)

## Шаг 3. Запуск
```bash
python bot.py
```

## Шаг 4. (Опционально) Публичный доступ к картинкам
Если хотите, чтобы Telegram показывал изображения карт в inline-режиме:
1. Запустите локальный HTTP-сервер:
   ```bash
   python -m http.server 8080
   ```
2. Запустите ngrok для проброса порта:
   ```bash
   ngrok http 8080
   ```
3. Используйте выданный ngrok-URL (например, `https://xxxx.ngrok-free.app/cards/6♧.png`) в коде бота.

## Советы
- Для автозапуска используйте screen/tmux (Linux) или Task Scheduler (Windows)
- Для обновления зависимостей: `pip install --upgrade -r requirements.txt`
- Для вопросов — пишите автору или создайте issue

---
Удачной игры в "Мафиозное Казино"! 🎰 