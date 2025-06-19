# Пример конфигурационного файла для бота "Мафиозное Казино"
# Скопируйте этот файл в config.py и замените значения на свои

import os

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGO_URL = os.getenv('MONGO_URL')
ADMIN_ID = 5743254515  # Замените на ваш Telegram ID

# Список Telegram user_id админов, которые могут использовать админ-команды
ADMIN_IDS = [5743254515]  # Замените на свой user_id

# Игровые константы
STARTING_MONEY = 1000  # Стартовый капитал новых игроков
DAILY_BONUS_AMOUNT = 100  # Сумма ежедневного бонуса
DAILY_BONUS_COOLDOWN = 24 * 60 * 60  # 24 часа в секундах

# Ранги и их требования
RANKS = {
    "Շեստյորկա": {"min_money": 0, "min_reputation": 0},
    "Բոյեց": {"min_money": 5000, "min_reputation": 10},
    "Ավտորիտետ": {"min_money": 15000, "min_reputation": 25},
    "Սմոտրյաշչիյ": {"min_money": 30000, "min_reputation": 50},
    "Գող օրենքով": {"min_money": 60000, "min_reputation": 100},
    "Դոն": {"min_money": 100000, "min_reputation": 200}
}

# Фракции
FACTIONS = ["копы", "мафия", "граждане"]

# Слоты - символы и их выплаты
SLOT_SYMBOLS = {
    "🍒": 2,    # Вишня - x2
    "🍋": 3,    # Лимон - x3
    "🍊": 5,    # Апельсин - x5
    "⭐": 10,   # Звезда - x10
    "💎": 25    # Алмаз - x25
}

# Преступления и их характеристики
CRIMES = {
    "գրպանահատություն": {
        "min_money": 0,
        "success_rate": 0.8,
        "reward": (50, 200),
        "jail_time": 300,  # 5 минут
        "reputation_change": {"копы": -5, "мафия": 2, "граждане": -3}
    },
    "կողոպուտ": {
        "min_money": 1000,
        "success_rate": 0.6,
        "reward": (200, 800),
        "jail_time": 1800,  # 30 минут
        "reputation_change": {"копы": -10, "мафия": 5, "граждане": -8}
    },
    "մաքսանենգություն": {
        "min_money": 5000,
        "success_rate": 0.5,
        "reward": (500, 2000),
        "jail_time": 3600,  # 1 час
        "reputation_change": {"копы": -15, "мафия": 10, "граждане": -5}
    },
    "բանկի կողոպուտ": {
        "min_money": 10000,
        "success_rate": 0.3,
        "reward": (1000, 5000),
        "jail_time": 7200,  # 2 часа
        "reputation_change": {"копы": -25, "мафия": 20, "граждане": -15}
    }
}

# Территории и их доход
TERRITORIES = {
    "Թաղամասեր": {"cost": 5000, "income": 50, "risk": 0.1},
    "Շրջան": {"cost": 15000, "income": 150, "risk": 0.05},
    "Կենտրոն": {"cost": 50000, "income": 500, "risk": 0.02},
    "Էլիտար շրջան": {"cost": 100000, "income": 1000, "risk": 0.01}
}

# Магазин предметов
SHOP_ITEMS = {
    "դանակ": {"cost": 500, "type": "weapon", "bonus": 0.05},
    "ատրճանակ": {"cost": 2000, "type": "weapon", "bonus": 0.1},
    "հրացան": {"cost": 10000, "type": "weapon", "bonus": 0.2},
    "զրահապատ վերնաշապիկ": {"cost": 1000, "type": "armor", "bonus": 0.1},
    "կապեր ոստիկանության հետ": {"cost": 5000, "type": "connections", "bonus": 0.15}
}

# Кулдауны (в секундах)
COOLDOWNS = {
    "daily_bonus": 24 * 60 * 60,  # 24 часа
    "crime": 300,  # 5 минут
    "casino": 60,  # 1 минута
    "territory_income": 3600,  # 1 час
}

# Файлы данных
DATA_FILE = "users_data.json"
GANGS_FILE = "gangs_data.json"
EVENTS_FILE = "events_data.json"

# Логирование
LOG_LEVEL = "INFO"
LOG_FILE = "mafia_casino_bot.log" 