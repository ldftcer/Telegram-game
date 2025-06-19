"""
Основной файл Telegram бота "Мафиозное Казино"
Содержит все обработчики команд и callback'ов
"""

import logging
import asyncio
import signal
import sys
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, InlineQueryHandler
from telegram.constants import ParseMode

# Импортируем наши модули

import config
from mongo_database import MongoDB
from games import casino_games
from crime_system import crime_system
from keyboards import keyboards
from translations import get_text
from config import SHOP_ITEMS, ADMIN_IDS

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('mafia_casino_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

db = MongoDB(config.MONGO_URL)

class MafiaCasinoBot:
    def __init__(self):
        """Инициализация бота"""
        # Настройка логирования
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler('mafia_casino_bot.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Создание приложения
        self.application = Application.builder().token(config.BOT_TOKEN).build()
        
        # Настройка обработчиков
        self.setup_handlers()
        
        # Настройка обработчика сигналов для сохранения игр при завершении
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для сохранения игр при завершении"""
        print(f"\nПолучен сигнал {signum}. Сохраняем игры и завершаем работу...")
        save_games()
        sys.exit(0)
    
    def setup_handlers(self):
        """Настраивает обработчики команд и callback'ов"""
        # Добавляем обработчики команд
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        self.application.add_handler(CommandHandler("balance", self.balance_command))
        self.application.add_handler(CommandHandler("casino", self.casino_command))
        self.application.add_handler(CommandHandler("crime", self.crime_command))
        self.application.add_handler(CommandHandler("gang", self.gang_command))
        self.application.add_handler(CommandHandler("top", self.top_command))
        self.application.add_handler(CommandHandler("daily_bonus", self.daily_bonus_command))
        self.application.add_handler(CommandHandler("rank", self.rank_command))
        self.application.add_handler(CommandHandler("stats", self.stats_command))
        self.application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        self.application.add_handler(CommandHandler("ban", self.ban_command))
        self.application.add_handler(CommandHandler("unban", self.unban_command))
        self.application.add_handler(CommandHandler("addmoney", self.addmoney_command))
        self.application.add_handler(CommandHandler("removemoney", self.removemoney_command))
        self.application.add_handler(CommandHandler("setrank", self.setrank_command))
        self.application.add_handler(CommandHandler("userstats", self.userstats_command))
        
        # Обработчик callback-запросов
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        # Проверяем, есть ли пользователь в базе
        user_data = await db.get_user(user.id)
        
        if not user_data:
            # Создаем нового пользователя
            user_data = await db.create_user(user.id, user.username or "Unknown", user.first_name)
            
            welcome_text = get_text("welcome_new", name=user.first_name, money=user_data['money'], rank=user_data['rank'])
        else:
            welcome_text = get_text("welcome_return", name=user.first_name, money=user_data['money'], rank=user_data['rank'])
        
        await update.message.reply_text(
            welcome_text,
            reply_markup=keyboards.main_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /profile"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        await self.show_profile(update, context, user_data)
    
    async def casino_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /casino"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        await update.message.reply_text(
            get_text("casino_title"),
            reply_markup=keyboards.casino_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def crime_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /crime"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        await update.message.reply_text(
            get_text("crime_title"),
            reply_markup=keyboards.crime_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def gang_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /gang"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        await update.message.reply_text(
            "👥 **Խմբեր** 👥\n\nԽմբի կառավարում՝",
            reply_markup=keyboards.gang_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def top_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /top"""
        await update.message.reply_text(
            get_text("top_title"),
            reply_markup=keyboards.top_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = f"""
{get_text("help_title")}

{get_text("help_commands")}
{get_text("help_start")}
{get_text("help_profile")}
{get_text("help_casino")}
{get_text("help_crime")}
{get_text("help_gang")}
{get_text("help_top")}
{get_text("help_help")}

{get_text("help_games")}
{get_text("help_slots")}
{get_text("help_roulette")}
{get_text("help_blackjack")}
{get_text("help_dice")}
{get_text("help_poker")}

{get_text("help_crimes")}
{get_text("help_pickpocket")}
{get_text("help_robbery")}
{get_text("help_smuggling")}
{get_text("help_bank")}

{get_text("help_territories")}
{get_text("help_territories_desc")}
{get_text("help_income")}
{get_text("help_protect")}

{get_text("help_gangs")}
{get_text("help_gangs_desc")}
{get_text("help_common")}
{get_text("help_wars")}

{get_text("help_shop")}
{get_text("help_weapons")}
{get_text("help_armor")}
{get_text("help_connections")}

{get_text("help_economy")}
{get_text("help_earn")}
{get_text("help_spend")}
{get_text("help_ranks")}

{get_text("help_ranks_list")}

{get_text("help_daily")}

{get_text("help_good_luck")}
        """
        
        await update.message.reply_text(
            help_text,
            reply_markup=keyboards.back_button("main_menu"),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик всех callback'ов"""
        query = update.callback_query
        await query.answer()
        
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await query.edit_message_text("❌ Вы не зарегистрированы! Используйте /start")
            return
        
        callback_data = query.data
        
        try:
            # Главное меню
            if callback_data == "main_menu":
                await self.show_main_menu(query)
            elif callback_data == "profile":
                await self.show_profile(update, context, user_data, query)
            elif callback_data == "profile_stats":
                await self.show_profile_stats(query, user_data)
            elif callback_data == "profile_achievements":
                await self.show_profile_achievements(query, user_data)
            elif callback_data == "shop_menu":
                await self.show_shop_menu(query)
            elif callback_data == "crime_menu":
                await self.show_crime_menu(query)
            elif callback_data == "casino_menu":
                await self.show_casino_menu(query)
            elif callback_data == "poker_menu":
                await self.show_poker_menu(query, user_data)
            elif callback_data == "casino_stats":
                await self.show_casino_stats(query, user_data)
            elif callback_data == "territories":
                await self.show_territories_menu(query)
            elif callback_data == "gang":
                await self.show_gang_menu(query, user_data)
            elif callback_data == "group":
                await self.show_group_menu(query, user_data)
            
            # Казино
            elif callback_data.startswith("slots_"):
                await self.handle_slots(query, user_data, callback_data)
            elif callback_data.startswith("roulette_"):
                await self.handle_roulette(query, user_data, callback_data, context)
            elif callback_data.startswith("blackjack_"):
                await self.handle_blackjack(query, user_data, callback_data, context)
            elif callback_data.startswith("dice_"):
                await self.handle_dice(query, user_data, callback_data, context)
            
            # Преступления
            elif callback_data.startswith("crime_"):
                await self.handle_crime(query, user_data, callback_data)
            
            # Территории
            elif callback_data == "territories_menu":
                await self.show_territories_menu(query)
            elif callback_data.startswith("buy_territory"):
                await self.handle_buy_territory(query, user_data, callback_data)
            elif callback_data == "collect_income":
                await self.handle_collect_income(query, user_data)
            elif callback_data == "my_territories":
                await self.show_my_territories(query, user_data)
            
            # Магазин
            elif callback_data.startswith("buy_"):
                await self.handle_shop(query, user_data, callback_data)
            
            # Банда
            elif callback_data.startswith("gang_"):
                await self.handle_gang(query, user_data, callback_data)
            
            # Группа
            elif callback_data.startswith("group_"):
                await self.handle_group(query, user_data, callback_data)
            
            elif callback_data == "daily_bonus":
                await self.handle_daily_bonus(query, user_data)
            elif callback_data == "help":
                await self.show_help(query)
            elif callback_data == "gang_menu":
                await self.show_gang_menu(query)
            elif callback_data == "escape":
                await self.handle_escape(query, user_data)
            elif callback_data == "top_menu":
                await self.show_top_menu(query)
            elif callback_data.startswith("top_"):
                await self.handle_top(query, callback_data)
            
            else:
                await query.edit_message_text("❌ Անհայտ հրաման")
        
        except Exception as e:
            logger.error(f"Ошибка в callback {callback_data}: {e}")
            await query.edit_message_text(f"❌ Произошла ошибка.\n{e}")
    
    async def show_main_menu(self, query):
        """Показывает главное меню"""
        await query.edit_message_text(
            get_text("main_menu"),
            reply_markup=keyboards.main_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def show_profile(self, update, context, user_data, query=None):
        """Показывает профиль пользователя"""
        # Проверяем, в тюрьме ли пользователь
        jail_status = ""
        if user_data.get("jail_time"):
            jail_end = datetime.fromisoformat(user_data["jail_time"])
            if jail_end > datetime.now():
                remaining = jail_end - datetime.now()
                minutes = int(remaining.total_seconds() / 60)
                jail_status = f"\n🚔 **В тюрьме:** {minutes} минут"
        
        # Проверяем, в банде ли пользователь
        gang_status = ""
        if user_data.get("gang"):
            gang_status = f"\n👥 **Банда:** {user_data['gang']['name']} ({user_data['gang']['role']})"
        
        profile_text = f"""
{get_text("profile_title")}

{get_text("profile_name", name=user_data.get('name') or user_data.get('first_name') or user_data.get('username') or 'Без имени')}
{get_text("profile_balance", money=user_data['money'])}
{get_text("profile_rank", rank=user_data['rank'])}

{get_text("profile_reputation")}
{get_text("profile_cops", cops=user_data['reputation']['копы'])}
{get_text("profile_mafia", mafia=user_data['reputation']['мафия'])}
{get_text("profile_citizens", citizens=user_data['reputation']['граждане'])}

{get_text("profile_territories", count=len(user_data['territories']))}
{get_text("profile_inventory", count=len(user_data['inventory']))}{gang_status}{jail_status}
        """
        
        if query:
            await query.edit_message_text(
                profile_text,
                reply_markup=keyboards.profile_actions(),
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                profile_text,
                reply_markup=keyboards.profile_actions(),
                parse_mode=ParseMode.HTML
            )
    
    async def handle_daily_bonus(self, query, user_data):
        from datetime import datetime, timedelta
        BONUS_AMOUNT = 1000
        BONUS_COOLDOWN = 24 * 60 * 60  # 24 часа в секундах
        now = datetime.now()
        last_time_str = user_data.get("daily_bonus_time")
        if last_time_str:
            last_time = datetime.fromisoformat(last_time_str)
            elapsed = (now - last_time).total_seconds()
            if elapsed < BONUS_COOLDOWN:
                remaining = BONUS_COOLDOWN - elapsed
                hours = int(remaining // 3600)
                minutes = int((remaining % 3600) // 60)
                await query.edit_message_text(
                    f"⏰ Օրական բոնուսը հասանելի կլինի {hours} ժ {minutes} ր հետո!",
                    reply_markup=keyboards.back_button("main_menu")
                )
                return
        # Выдаём бонус
        new_money = user_data["money"] + BONUS_AMOUNT
        await db.update_user(query.from_user.id, {"money": new_money, "daily_bonus_time": now.isoformat()})
        await query.edit_message_text(
            f"🎁 Դուք ստացել եք {BONUS_AMOUNT} մետաղադրամ օրական բոնուս!\n💳 Նոր հաշվեկշիռ: {new_money} մետաղադրամ",
            reply_markup=keyboards.back_button("main_menu")
        )
    
    async def show_casino_menu(self, query):
        """Показывает меню казино"""
        await query.edit_message_text(
            get_text("casino_title"),
            reply_markup=keyboards.casino_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def show_poker_menu(self, query, user_data):
        """Заглушка для покера"""
        await query.edit_message_text(
            "♠️ **Պոկեր**\n\nԱյս խաղը շուտով հասանելի կլինի!",
            reply_markup=keyboards.back_button("casino_menu"),
            parse_mode=ParseMode.HTML
        )

    async def show_casino_stats(self, query, user_data):
        """Показывает простую статистику по казино-играм"""
        stats = user_data.get("statistics", {})
        text = f"""
📊 **Կազինոյի վիճակագրություն**

🎰 Սլոտեր: {stats.get('slots_played', 0)} խաղ
🎲 Ռուլետկա: {stats.get('roulette_played', 0)} խաղ
🃏 Բլեքջեք: {stats.get('blackjack_played', 0)} խաղ
🎲 Զառեր: {stats.get('dice_played', 0)} խաղ
♠️ Պոկեր: {stats.get('poker_played', 0)} խաղ
"""
        await query.edit_message_text(
            text,
            reply_markup=keyboards.back_button("casino_menu"),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_slots(self, query, user_data, callback_data):
        """Обработчик слотов"""
        if callback_data == "slots_menu":
            await query.edit_message_text(
                get_text("slots_title"),
                reply_markup=keyboards.slots_menu(),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Извлекаем ставку
        bet = int(callback_data.split("_")[1])
        
        if user_data["money"] < bet:
            await query.edit_message_text(
                get_text("not_enough_money", amount=bet),
                reply_markup=keyboards.back_button("slots_menu"),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Играем в слоты
        result = casino_games.play_slots(bet)
        
        if result["success"]:
            # Обновляем деньги
            new_money = user_data["money"] - bet + result["win_amount"]
            stats = user_data.get("statistics", {})
            stats["slots_played"] = stats.get("slots_played", 0) + 1
            await db.update_user(query.from_user.id, {"money": new_money, "statistics": stats})
            
            # Показываем результат
            result_text = get_text("slots_result", 
                                 result=' '.join(result['result']), 
                                 message=result['message'],
                                 bet=bet, 
                                 balance=new_money)
            
            await query.edit_message_text(
                result_text,
                reply_markup=keyboards.back_button("slots_menu"),
                parse_mode=ParseMode.HTML
            )
    
    async def handle_roulette(self, query, user_data, callback_data, context):
        """Обработчик рулетки"""
        if callback_data == "roulette_menu":
            await query.edit_message_text(
                get_text("roulette_title"),
                reply_markup=keyboards.roulette_menu(),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Обрабатываем разные типы ставок
        if callback_data in ["roulette_red", "roulette_black", "roulette_even", "roulette_odd"]:
            bet_type = callback_data.split("_")[1]
            bet_value = {"red": "կարմիր", "black": "սև", "even": "զույգ", "odd": "կենտ"}[bet_type]
            
            # Сохраняем выбор в контексте
            context.user_data["roulette_bet"] = {"type": "color" if bet_type in ["red", "black"] else "even_odd", "value": bet_value}
            
            await query.edit_message_text(
                f"🎲 **Ռուլետկա** 🎲\n\nԳրավադրում: {bet_value}\nԸնտրեք գումարը՝",
                reply_markup=keyboards.roulette_bet_amounts(),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Новый блок: выбор числа
        if callback_data == "roulette_number":
            await query.edit_message_text(
                "🎯 Ընտրեք թիվը (0-36):",
                reply_markup=keyboards.number_keyboard(36, "roulette_pick_number"),
                parse_mode=ParseMode.HTML
            )
            return
        
        if callback_data.startswith("roulette_pick_number_"):
            number = int(callback_data.split("_")[-1])
            context.user_data["roulette_bet"] = {"type": "number", "value": str(number)}
            await query.edit_message_text(
                f"🎲 **Ռուլետկա** 🎲\n\nԳրավադրում: թիվ {number}\nԸնտրեք գումարը՝",
                reply_markup=keyboards.roulette_bet_amounts(),
                parse_mode=ParseMode.HTML
            )
            return
        
        if callback_data.startswith("roulette_bet_"):
            bet_amount = int(callback_data.split("_")[2])
            
            if user_data["money"] < bet_amount:
                await query.edit_message_text(
                    get_text("not_enough_money", amount=bet_amount),
                    reply_markup=keyboards.back_button("roulette_menu"),
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Получаем сохраненную ставку
            roulette_bet = context.user_data.get("roulette_bet", {})
            if not roulette_bet:
                await query.edit_message_text(
                    "❌ Սխալ! Ընտրեք գրավադրման տեսակը կրկին",
                    reply_markup=keyboards.roulette_menu(),
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Играем в рулетку
            result = casino_games.play_roulette(
                roulette_bet["type"], 
                roulette_bet["value"], 
                bet_amount
            )
            
            if result["success"]:
                # Обновляем деньги
                new_money = user_data["money"] - bet_amount + result["win_amount"]
                stats = user_data.get("statistics", {})
                stats["roulette_played"] = stats.get("roulette_played", 0) + 1
                await db.update_user(query.from_user.id, {"money": new_money, "statistics": stats})
                
                # Показываем результат
                result_text = get_text("roulette_result",
                                     number=result['number'],
                                     color=result['color'],
                                     message=result['message'],
                                     bet=bet_amount,
                                     balance=new_money)
                
                await query.edit_message_text(
                    result_text,
                    reply_markup=keyboards.back_button("roulette_menu"),
                    parse_mode=ParseMode.HTML
                )
    
    async def handle_blackjack(self, query, user_data, callback_data, context):
        """Обработчик блэкджека"""
        if callback_data == "blackjack_menu":
            await query.edit_message_text(
                get_text("blackjack_title"),
                reply_markup=keyboards.blackjack_menu(),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Первый ход: выбор ставки
        if callback_data.startswith("blackjack_") and callback_data.split("_")[1].isdigit():
            bet = int(callback_data.split("_")[1])
            if user_data["money"] < bet:
                await query.edit_message_text(
                    get_text("not_enough_money", amount=bet),
                    reply_markup=keyboards.back_button("blackjack_menu"),
                    parse_mode=ParseMode.HTML
                )
                return
            # Сохраняем ставку в context
            context.user_data["blackjack_bet"] = bet
            # Играем в блэкджек
            result = casino_games.play_blackjack(bet)
            if result["success"]:
                new_money = user_data["money"] - bet + result.get("win_amount", 0)
                stats = user_data.get("statistics", {})
                stats["blackjack_played"] = stats.get("blackjack_played", 0) + 1
                await db.update_user(query.from_user.id, {"money": new_money, "statistics": stats})
                player_score = casino_games.calculate_blackjack_score(result["player_cards"])
                result_text = f"""
🃏 **Բլեքջեք** 🃏

🎯 Ձեր քարտերը: {' '.join(result['player_cards'])}
📊 Ձեր միավորները: {player_score}

🎰 Դիլերի քարտերը: {' '.join(result['dealer_visible'])}

Ընտրեք գործողությունը՝
                """
                # Сохраняем карты в context
                context.user_data["blackjack_player_cards"] = result["player_cards"]
                context.user_data["blackjack_dealer_cards"] = result["dealer_cards"]
                await query.edit_message_text(
                    result_text,
                    reply_markup=keyboards.blackjack_game(),
                    parse_mode=ParseMode.HTML
                )
            return
        
        # Ход: взять карту
        if callback_data == "blackjack_hit":
            bet = context.user_data.get("blackjack_bet", 0)
            player_cards = context.user_data.get("blackjack_player_cards", [])
            dealer_cards = context.user_data.get("blackjack_dealer_cards", [])
            result = casino_games.blackjack_hit(player_cards, dealer_cards, bet)
            player_score = casino_games.calculate_blackjack_score(result["player_cards"])
            if result["game_state"] == "bust":
                # Проигрыш
                result_text = f"💥 **Փոխանցում** 💥\n\n🎯 Ձեր քարտերը: {' '.join(result['player_cards'])}\n📊 Ձեր միավորները: {player_score}\n\nԴուք պարտվեցիք!"
                await query.edit_message_text(
                    result_text,
                    reply_markup=keyboards.back_button("blackjack_menu"),
                    parse_mode=ParseMode.HTML
                )
                return
            # Иначе продолжаем игру
            context.user_data["blackjack_player_cards"] = result["player_cards"]
            context.user_data["blackjack_dealer_cards"] = result["dealer_cards"]
            result_text = f"🃏 **Բլեքջեք** 🃏\n\n🎯 Ձեր քարտերը: {' '.join(result['player_cards'])}\n📊 Ձեր միավորները: {player_score}\n\n🎰 Դիլերի քարտերը: {' '.join(['🂠' if i > 0 else c for i, c in enumerate(result['dealer_cards'])])}\n\nԸնտրեք գործողությունը՝"
            await query.edit_message_text(
                result_text,
                reply_markup=keyboards.blackjack_game(),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Ход: хватит
        if callback_data == "blackjack_stand":
            bet = context.user_data.get("blackjack_bet", 0)
            player_cards = context.user_data.get("blackjack_player_cards", [])
            dealer_cards = context.user_data.get("blackjack_dealer_cards", [])
            result = casino_games.blackjack_stand(player_cards, dealer_cards, bet)
            player_score = casino_games.calculate_blackjack_score(result["player_cards"])
            dealer_score = casino_games.calculate_blackjack_score(result["dealer_cards"])
            result_text = f"🃏 **Բլեքջեք** 🃏\n\n🎯 Ձեր քարտերը: {' '.join(result['player_cards'])}\n📊 Ձեր միավորները: {player_score}\n\n🎰 Դիլերի քարտերը: {' '.join(result['dealer_cards'])}\n📊 Դիլերի միավորները: {dealer_score}\n\n{result['message']}"
            # Обновляем деньги
            new_money = user_data["money"] + result.get("win_amount", 0)
            stats = user_data.get("statistics", {})
            stats["blackjack_played"] = stats.get("blackjack_played", 0) + 1
            await db.update_user(query.from_user.id, {"money": new_money, "statistics": stats})
            await query.edit_message_text(
                result_text,
                reply_markup=keyboards.back_button("blackjack_menu"),
                parse_mode=ParseMode.HTML
            )
            return
    
    async def handle_dice(self, query, user_data, callback_data, context):
        """Обработчик костей"""
        if callback_data == "dice_menu":
            await query.edit_message_text(
                get_text("dice_title"),
                reply_markup=keyboards.dice_menu(),
                parse_mode=ParseMode.HTML
            )
            return
        
        if callback_data.startswith("dice_") and not callback_data.startswith("dice_pred_"):
            bet = int(callback_data.split("_")[1])
            
            if user_data["money"] < bet:
                await query.edit_message_text(
                    get_text("not_enough_money", amount=bet),
                    reply_markup=keyboards.back_button("dice_menu"),
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Сохраняем ставку
            context.user_data["dice_bet"] = bet
            
            await query.edit_message_text(
                f"🎲 **Զառեր** 🎲\n\nԳրավադրում: {bet} մետաղադրամ\nԳուշակեք երկու զառերի գումարը՝",
                reply_markup=keyboards.dice_predictions(),
                parse_mode=ParseMode.HTML
            )
            return
        
        if callback_data.startswith("dice_pred_"):
            prediction = int(callback_data.split("_")[2])
            bet = context.user_data.get("dice_bet", 0)
            
            if bet == 0:
                await query.edit_message_text(
                    "❌ Սխալ! Ընտրեք գրավադրումը կրկին",
                    reply_markup=keyboards.dice_menu(),
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Играем в кости
            result = casino_games.play_dice(bet, prediction)
            
            if result["success"]:
                # Обновляем деньги
                new_money = user_data["money"] - bet + result["win_amount"]
                stats = user_data.get("statistics", {})
                stats["dice_played"] = stats.get("dice_played", 0) + 1
                await db.update_user(query.from_user.id, {"money": new_money, "statistics": stats})
                
                # Показываем результат
                result_text = get_text("dice_result",
                                     prediction=prediction,
                                     dice1=result['dice'][0],
                                     dice2=result['dice'][1],
                                     total=result['total'],
                                     message=result['message'],
                                     bet=bet,
                                     balance=new_money)
                
                await query.edit_message_text(
                    result_text,
                    reply_markup=keyboards.back_button("dice_menu"),
                    parse_mode=ParseMode.HTML
                )
    
    async def show_crime_menu(self, query):
        """Показывает меню преступлений"""
        await query.edit_message_text(
            get_text("crime_title"),
            reply_markup=keyboards.crime_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_crime(self, query, user_data, callback_data):
        """Обработчик преступлений"""
        crime_type = callback_data.split("_")[1]
        crime_names = {
            "pickpocket": get_text("crime_pickpocket"),
            "robbery": get_text("crime_robbery"),
            "smuggling": get_text("crime_smuggling"),
            "bank": get_text("crime_bank")
        }
        
        crime_name = crime_names.get(crime_type)
        if not crime_name:
            await query.edit_message_text("❌ Անհայտ հանցագործություն")
            return
        
        # Совершаем преступление
        result = crime_system.commit_crime(query.from_user.id, crime_name, user_data)
        
        if result["success"]:
            # Обновляем данные пользователя
            updates = {
                "money": result.get("new_money", user_data["money"]),
                "reputation": result.get("new_reputation", user_data["reputation"]),
                "statistics": result.get("new_stats", user_data["statistics"]),
                "last_crime_time": datetime.now().isoformat()
            }
            
            if result.get("jail_time"):
                updates["jail_time"] = result["jail_time"]
                updates["jail_start"] = datetime.now().isoformat()
            
            await db.update_user(query.from_user.id, updates)
            
            # Показываем результат
            await query.edit_message_text(
                f"🔫 **{crime_name.title()}** 🔫\n\n{result['message']}",
                reply_markup=keyboards.back_button("crime_menu"),
                parse_mode=ParseMode.HTML
            )
        else:
            await query.edit_message_text(
                f"❌ {result['message']}",
                reply_markup=keyboards.back_button("crime_menu"),
                parse_mode=ParseMode.HTML
            )
    
    async def show_territories_menu(self, query):
        """Показывает меню территорий"""
        await query.edit_message_text(
            get_text("territories_title"),
            reply_markup=keyboards.territories_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_buy_territory(self, query, user_data, callback_data):
        """Обработчик покупки территории"""
        if callback_data == "buy_territory":
            # Показываем доступные территории
            available = crime_system.get_available_territories(user_data)
            
            if not available:
                await query.edit_message_text(
                    "❌ Գնման համար հասանելի տարածքներ չկան",
                    reply_markup=keyboards.back_button("territories_menu"),
                    parse_mode=ParseMode.HTML
                )
                return
            
            await query.edit_message_text(
                "🏘️ **Հասանելի տարածքներ** 🏘️\n\nԸնտրեք գնման համար՝",
                reply_markup=keyboards.available_territories(available),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Покупаем конкретную территорию
        territory_name = callback_data.split("_", 2)[2]
        result = crime_system.buy_territory(query.from_user.id, territory_name, user_data)
        
        if result["success"]:
            # Обновляем данные пользователя
            await db.update_user(query.from_user.id, {
                "money": result["new_money"],
                "territories": result["new_territories"]
            })
            
            await query.edit_message_text(
                get_text("territory_bought", message=result['message']),
                reply_markup=keyboards.back_button("territories_menu"),
                parse_mode=ParseMode.HTML
            )
        else:
            await query.edit_message_text(
                f"❌ {result['message']}",
                reply_markup=keyboards.back_button("territories_menu"),
                parse_mode=ParseMode.HTML
            )
    
    async def handle_collect_income(self, query, user_data):
        """Обработчик сбора дохода с территорий"""
        result = crime_system.collect_territory_income(query.from_user.id, user_data)
        
        if result["success"]:
            # Обновляем данные пользователя
            updates = {
                "money": result["new_money"],
                "last_territory_income": datetime.now().isoformat()
            }
            
            await db.update_user(query.from_user.id, updates)
            
            await query.edit_message_text(
                get_text("income_collected", message=result['message']),
                reply_markup=keyboards.back_button("territories_menu"),
                parse_mode=ParseMode.HTML
            )
        else:
            await query.edit_message_text(
                f"❌ {result['message']}",
                reply_markup=keyboards.back_button("territories_menu"),
                parse_mode=ParseMode.HTML
            )
    
    async def show_gang_menu(self, query):
        """Показывает меню банды"""
        await query.edit_message_text(
            "👥 **Խմբեր** 👥\n\nԽմբի կառավարում՝",
            reply_markup=keyboards.gang_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_gang(self, query, user_data, callback_data):
        """Обработчик действий с бандой"""
        # Заглушка для обработки действий с бандой
        await query.edit_message_text(
            "👥 **Խմբեր** 👥\n\nФункция в разработке!",
            reply_markup=keyboards.back_button("gang_menu"),
            parse_mode=ParseMode.HTML
        )
    
    async def show_shop_menu(self, query):
        """Показывает меню магазина"""
        await query.edit_message_text(
            get_text("shop_title"),
            reply_markup=keyboards.shop_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_shop(self, query, user_data, callback_data):
        """Обработчик покупок в магазине"""
        item_name = callback_data.split("_", 1)[1]
        item_info = SHOP_ITEMS.get(item_name)
        
        if not item_info:
            await query.edit_message_text(
                "❌ Անհայտ առարկա",
                reply_markup=keyboards.back_button("shop_menu"),
                parse_mode=ParseMode.HTML
            )
            return
        
        if user_data["money"] < item_info["cost"]:
            await query.edit_message_text(
                get_text("not_enough_money", amount=item_info['cost']),
                reply_markup=keyboards.back_button("shop_menu"),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Покупаем предмет
        new_money = user_data["money"] - item_info["cost"]
        new_inventory = user_data["inventory"] + [item_name]
        
        await db.update_user(query.from_user.id, {
            "money": new_money,
            "inventory": new_inventory
        })
        
        await query.edit_message_text(
            get_text("item_bought", item=item_name, cost=item_info['cost'], balance=new_money),
            reply_markup=keyboards.back_button("shop_menu"),
            parse_mode=ParseMode.HTML
        )
    
    async def show_top_menu(self, query):
        """Показывает меню рейтингов"""
        await query.edit_message_text(
            get_text("top_title"),
            reply_markup=keyboards.top_menu(),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_top(self, query, callback_data):
        """Обработчик рейтингов"""
        top_type = callback_data.split("_")[1]
        top_users = await db.get_top_users(top_type, 10)
        
        if not top_users:
            await query.edit_message_text(
                "❌ Դասակարգման տվյալներ չկան",
                reply_markup=keyboards.back_button("top_menu"),
                parse_mode=ParseMode.HTML
            )
            return
        
        # Формируем текст рейтинга
        if top_type == "money":
            top_text = get_text("top_money")
        elif top_type == "rank":
            top_text = get_text("top_rank")
        elif top_type == "reputation":
            top_text = get_text("top_reputation")
        else:
            top_text = get_text("top_territories")
        
        for i, user in enumerate(top_users, 1):
            if top_type == "money":
                value = f"{user['money']} մետաղադրամ"
            elif top_type == "rank":
                value = user['rank']
            elif top_type == "reputation":
                value = f"{sum(user['reputation'].values())} միավոր"
            else:
                value = f"{len(user['territories'])} տարածք"
            # Исправлено: используем user['name'] или user['username'] вместо user['first_name']
            display_name = user.get('name') or user.get('username') or 'Без имени'
            top_text += f"{i}. {display_name}: {value}\n"
        
        await query.edit_message_text(
            top_text,
            reply_markup=keyboards.back_button("top_menu"),
            parse_mode=ParseMode.HTML
        )
    
    async def show_help(self, query):
        """Показывает справку"""
        help_text = f"""
{get_text("help_title")}

{get_text("help_commands")}
{get_text("help_start")}
{get_text("help_profile")}
{get_text("help_casino")}
{get_text("help_crime")}
{get_text("help_gang")}
{get_text("help_top")}
{get_text("help_help")}

{get_text("help_games")}
{get_text("help_slots")}
{get_text("help_roulette")}
{get_text("help_blackjack")}
{get_text("help_dice")}
{get_text("help_poker")}

{get_text("help_crimes")}
{get_text("help_pickpocket")}
{get_text("help_robbery")}
{get_text("help_smuggling")}
{get_text("help_bank")}

{get_text("help_territories")}
{get_text("help_territories_desc")}
{get_text("help_income")}
{get_text("help_protect")}

{get_text("help_gangs")}
{get_text("help_gangs_desc")}
{get_text("help_common")}
{get_text("help_wars")}

{get_text("help_shop")}
{get_text("help_weapons")}
{get_text("help_armor")}
{get_text("help_connections")}

{get_text("help_economy")}
{get_text("help_earn")}
{get_text("help_spend")}
{get_text("help_ranks")}

{get_text("help_ranks_list")}

{get_text("help_daily")}

{get_text("help_good_luck")}
        """
        
        await query.edit_message_text(
            help_text,
            reply_markup=keyboards.back_button("main_menu"),
            parse_mode=ParseMode.HTML
        )
    
    async def handle_escape(self, query, user_data):
        """Обработчик побега из тюрьмы"""
        result = crime_system.organize_escape(query.from_user.id, user_data)
        
        if result["success"]:
            # Обновляем данные пользователя
            updates = {}
            if "new_money" in result:
                updates["money"] = result["new_money"]
            if result.get("new_jail_time"):
                updates["jail_time"] = result["new_jail_time"]
            if result.get("escape_success"):
                updates["jail_time"] = 0
                updates["jail_start"] = None
            await db.update_user(query.from_user.id, updates)
            
            await query.edit_message_text(
                f"🏃‍♂️ **Փախուստ** 🏃‍♂️\n\n{result['message']}",
                reply_markup=keyboards.back_button("main_menu"),
                parse_mode=ParseMode.HTML
            )
        else:
            await query.edit_message_text(
                f"❌ {result['message']}",
                reply_markup=keyboards.back_button("main_menu"),
                parse_mode=ParseMode.HTML
            )
    
    # Групповые команды
    async def daily_bonus_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда ежедневного бонуса для групп"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        current_time = datetime.now()
        
        if user_data.get("daily_bonus_time"):
            last_bonus = datetime.fromisoformat(user_data["daily_bonus_time"])
            time_diff = current_time - last_bonus
            
            if time_diff < timedelta(seconds=DAILY_BONUS_COOLDOWN):
                remaining = DAILY_BONUS_COOLDOWN - time_diff.seconds
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                
                await update.message.reply_text(
                    get_text("group_daily_wait", username=user.username or user.first_name, hours=hours, minutes=minutes),
                    parse_mode=ParseMode.HTML
                )
                return
        
        # Выдаем бонус
        new_money = user_data["money"] + DAILY_BONUS_AMOUNT
        await db.update_user(user.id, {
            "money": new_money,
            "daily_bonus_time": current_time.isoformat()
        })
        
        await update.message.reply_text(
            get_text("group_daily_received", username=user.username or user.first_name, amount=DAILY_BONUS_AMOUNT, balance=new_money),
            parse_mode=ParseMode.HTML
        )
    
    async def balance_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда баланса для групп"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        rank = await db.get_user_rank(user.id)
        
        await update.message.reply_text(
            get_text("group_balance", username=user.username or user.first_name, money=user_data['money'], rank=rank),
            parse_mode=ParseMode.HTML
        )
    
    async def rank_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда ранга для групп"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        rank = await db.get_user_rank(user.id)
        total_reputation = sum(user_data["reputation"].values())
        
        await update.message.reply_text(
            get_text("group_rank", username=user.username or user.first_name, rank=rank, reputation=total_reputation, territories=len(user_data['territories'])),
            parse_mode=ParseMode.HTML
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда статистики для групп"""
        user = update.effective_user
        user_data = await db.get_user(user.id)
        
        if not user_data:
            await update.message.reply_text(get_text("not_registered"))
            return
        
        stats = user_data["statistics"]
        
        await update.message.reply_text(
            get_text("group_stats", username=user.username or user.first_name, games_played=stats['games_played'], games_won=stats['games_won'], crimes_committed=stats['crimes_committed'], crimes_successful=stats['crimes_successful'], money_earned=stats['money_earned'], money_lost=stats['money_lost']),
            parse_mode=ParseMode.HTML
        )
    
    async def show_my_territories(self, query, user_data):
        """Показывает список территорий пользователя"""
        if not user_data["territories"]:
            await query.edit_message_text(
                "❌ Դուք չունեք տարածքներ",
                reply_markup=keyboards.back_button("territories_menu"),
                parse_mode=ParseMode.HTML
            )
            return
        text = "🏘️ **Ձեր տարածքները** 🏘️\n\n"
        for t in user_data["territories"]:
            text += f"• {t}\n"
        await query.edit_message_text(
            text,
            reply_markup=keyboards.back_button("territories_menu"),
            parse_mode=ParseMode.HTML
        )
    
    async def show_profile_stats(self, query, user_data):
        """Показывает статистику игрока"""
        stats = user_data.get("statistics", {})
        text = f"""
📊 **Վիճակագրություն**

🎰 Խաղեր: {stats.get('games_played', 0)}
🎉 Հաղթանակներ: {stats.get('games_won', 0)}
🔫 Հանցագործություններ: {stats.get('crimes_committed', 0)}
💰 Կողոպուտներ: {stats.get('robberies', 0)}
        """
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Հետ", callback_data="profile")]
            ]),
            parse_mode=ParseMode.HTML
        )
    
    async def show_profile_achievements(self, query, user_data):
        """Показывает достижения игрока"""
        achievements = user_data.get("achievements", [])
        if not achievements:
            text = "🏆 Դեռևս ձեռքբերումներ չկան"
        else:
            text = "🏆 **Ձեռքբերումներ**\n\n" + "\n".join(f"• {a}" for a in achievements)
        await query.edit_message_text(
            text,
            reply_markup=keyboards.back_button("profile"),
            parse_mode=ParseMode.HTML
        )
    
    # Проверка на админа
    async def is_admin(self, user_id):
        return user_id in ADMIN_IDS

    # Команда рассылки
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        text = ' '.join(context.args)
        count = 0
        for user in await db.get_all_users():
            try:
                await context.bot.send_message(user['user_id'], text)
                count += 1
            except Exception:
                pass
        await update.message.reply_text(f"Рассылка отправлена {count} пользователям.")

    # Бан/разбан
    async def ban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        user_id = int(context.args[0])
        await db.update_user(user_id, {"banned": True})
        await update.message.reply_text(f"Пользователь {user_id} забанен.")

    async def unban_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        user_id = int(context.args[0])
        await db.update_user(user_id, {"banned": False})
        await update.message.reply_text(f"Пользователь {user_id} разбанен.")

    # Выдать/отнять деньги
    async def addmoney_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        user_id = int(context.args[0])
        amount = int(context.args[1])
        user = await db.get_user(user_id)
        if not user:
            await update.message.reply_text("Пользователь не найден.")
            return
        new_money = user["money"] + amount
        await db.update_user(user_id, {"money": new_money})
        await update.message.reply_text(f"Готово! Новый баланс: {new_money}")

    async def removemoney_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        user_id = int(context.args[0])
        amount = int(context.args[1])
        user = await db.get_user(user_id)
        if not user:
            await update.message.reply_text("Пользователь не найден.")
            return
        new_money = max(0, user["money"] - amount)
        await db.update_user(user_id, {"money": new_money})
        await update.message.reply_text(f"Готово! Новый баланс: {new_money}")

    # Изменить ранг
    async def setrank_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        user_id = int(context.args[0])
        rank = context.args[1]
        await db.update_user(user_id, {"rank": rank})
        await update.message.reply_text(f"Ранг пользователя {user_id} изменён на {rank}.")

    # Профиль пользователя
    async def userstats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        user_id = int(context.args[0])
        user = await db.get_user(user_id)
        if not user:
            await update.message.reply_text("Пользователь не найден.")
            return
        await update.message.reply_text(str(user))

    # Общая статистика
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await self.is_admin(update.effective_user.id):
            return
        total = len(await db.get_all_users())
        banned = sum(1 for u in await db.get_all_users() if u.get("banned"))
        total_money = sum(u["money"] for u in await db.get_all_users())
        await update.message.reply_text(f"Всего пользователей: {total}\nЗабанено: {banned}\nОбщий баланс: {total_money}")

    def run(self):
        """Запускает бота"""
        logger.info("Запуск бота Мафиозное Казино...")
        self.application.run_polling()
    
if __name__ == "__main__":
    bot = MafiaCasinoBot()
    bot.run() 
