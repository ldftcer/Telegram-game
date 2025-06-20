# Мафиозное Казино — Telegram Bot

![Logo](https://emojicdn.elk.sh/🎰)

**Мафиозное Казино** — это современный Telegram-бот-игра с казино, преступлениями, бандами, территориями и рейтингами. Полностью на армянском языке, с поддержкой групп и приватных чатов.

---

## 🚀 Возможности
- Казино: слоты, рулетка, блэкджек, кости, покер
- Преступления, банды, территория, ограбления
- Профили, достижения, топы, магазин
- Ежедневный бонус, система рангов, репутация
- Красивые PNG-карты (inline-режим)
- Гибкая локализация и поддержка групп

---

## 🖼️ Пример интерфейса

```
@ваш_бот /start

🎰 Բարի գալուստ Մաֆիոզական Կազինո!

💰 Ձեր հաշիվը: 10000 մետաղադրամ
👑 Ձեր կոչումը: Շեստյորկա
```

![Пример карты](https://your-ngrok-url.ngrok-free.app/cards/Q♡.png)

---

## ⚡ Быстрый старт
1. Клонируйте репозиторий и установите зависимости:
   ```bash
   git clone <ваш-репозиторий>
   cd "Telegram game"
   pip install -r requirements.txt
   ```
2. Настройте `config.py` (токен, параметры)
3. Запустите бота:
   ```bash
   python bot.py
   ```
4. (Опционально) Настройте ngrok для публичного доступа к картинкам

---

## ❓ FAQ
- **Где взять токен?** — Получите у @BotFather
- **Как добавить PNG-карты?** — Положите 36 файлов в папку `cards/`
- **Как сделать картинки публичными?** — Используйте ngrok и http.server (см. INSTALL.md)
- **Как запустить на сервере?** — Используйте screen/tmux или Task Scheduler
- **Как сменить язык?** — Все тексты в `translations.py`

---

## 💡 Советы
- Не забывайте делать бэкапы базы данных
- Для кастомизации — редактируйте клавиатуры и переводы
- Для поддержки — создайте issue или напишите автору

---

## 👤 Контакты
- Автор: [https://t.me/ishqantas]
- Telegram: [https://t.me/ldftcer]
- Issues: [ссылка на репозиторий]

---

Удачной игры! 🎲 