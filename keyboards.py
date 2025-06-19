"""
Модуль с клавиатурами и кнопками
Создает inline клавиатуры для всех меню бота
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Dict, Optional
from translations import get_text

class Keyboards:
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        """Главное меню"""
        keyboard = [
            [
                InlineKeyboardButton("💰 Կազինո", callback_data="casino_menu"),
                InlineKeyboardButton("🔫 Հանցագործություններ", callback_data="crime_menu")
            ],
            [
                InlineKeyboardButton("👤 Պրոֆիլ", callback_data="profile"),
                InlineKeyboardButton("👥 Խումբ", callback_data="gang_menu")
            ],
            [
                InlineKeyboardButton("🏪 Խանութ", callback_data="shop_menu"),
                InlineKeyboardButton("📊 Դասակարգում", callback_data="top_menu")
            ],
            [
                InlineKeyboardButton("🎁 Օրական բոնուս", callback_data="daily_bonus"),
                InlineKeyboardButton("❓ Օգնություն", callback_data="help")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def casino_menu() -> InlineKeyboardMarkup:
        """Меню казино"""
        keyboard = [
            [
                InlineKeyboardButton("🎰 Սլոտեր", callback_data="slots_menu"),
                InlineKeyboardButton("🎲 Ռուլետկա", callback_data="roulette_menu")
            ],
            [
                InlineKeyboardButton("🃏 Բլեքջեք", callback_data="blackjack_menu"),
                InlineKeyboardButton("🎲 Զառեր", callback_data="dice_menu")
            ],
            [
                InlineKeyboardButton("♠️ Պոկեր", callback_data="poker_menu"),
                InlineKeyboardButton("📊 Խաղերի վիճակագրություն", callback_data="casino_stats")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def slots_menu() -> InlineKeyboardMarkup:
        """Меню слотов"""
        keyboard = [
            [
                InlineKeyboardButton("🎰 10 մետաղադրամ", callback_data="slots_10"),
                InlineKeyboardButton("🎰 50 մետաղադրամ", callback_data="slots_50"),
                InlineKeyboardButton("🎰 100 մետաղադրամ", callback_data="slots_100")
            ],
            [
                InlineKeyboardButton("🎰 500 մետաղադրամ", callback_data="slots_500"),
                InlineKeyboardButton("🎰 1000 մետաղադրամ", callback_data="slots_1000")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="casino_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def roulette_menu() -> InlineKeyboardMarkup:
        """Меню рулетки"""
        keyboard = [
            [
                InlineKeyboardButton("🔴 Կարմիր", callback_data="roulette_red"),
                InlineKeyboardButton("⚫ Սև", callback_data="roulette_black")
            ],
            [
                InlineKeyboardButton("🔢 Զույգ", callback_data="roulette_even"),
                InlineKeyboardButton("🔢 Կենտ", callback_data="roulette_odd")
            ],
            [
                InlineKeyboardButton("🎯 Կոնկրետ թիվ", callback_data="roulette_number")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="casino_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def roulette_bet_amounts() -> InlineKeyboardMarkup:
        """Ставки для рулетки"""
        keyboard = [
            [
                InlineKeyboardButton("💰 10", callback_data="roulette_bet_10"),
                InlineKeyboardButton("💰 50", callback_data="roulette_bet_50"),
                InlineKeyboardButton("💰 100", callback_data="roulette_bet_100")
            ],
            [
                InlineKeyboardButton("💰 500", callback_data="roulette_bet_500"),
                InlineKeyboardButton("💰 1000", callback_data="roulette_bet_1000")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="roulette_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def blackjack_menu() -> InlineKeyboardMarkup:
        """Меню блэкджека"""
        keyboard = [
            [
                InlineKeyboardButton("🃏 10 մետաղադրամ", callback_data="blackjack_10"),
                InlineKeyboardButton("🃏 50 մետաղադրամ", callback_data="blackjack_50"),
                InlineKeyboardButton("🃏 100 մետաղադրամ", callback_data="blackjack_100")
            ],
            [
                InlineKeyboardButton("🃏 500 մետաղադրամ", callback_data="blackjack_500"),
                InlineKeyboardButton("🃏 1000 մետաղադրամ", callback_data="blackjack_1000")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="casino_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def blackjack_game() -> InlineKeyboardMarkup:
        """Кнопки во время игры в блэкджек"""
        keyboard = [
            [
                InlineKeyboardButton("➕ Վերցնել քարտ", callback_data="blackjack_hit"),
                InlineKeyboardButton("✋ Բավական է", callback_data="blackjack_stand")
            ],
            [
                InlineKeyboardButton("🔙 Նոր խաղ", callback_data="blackjack_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def dice_menu() -> InlineKeyboardMarkup:
        """Меню костей"""
        keyboard = [
            [
                InlineKeyboardButton("🎲 10 մետաղադրամ", callback_data="dice_10"),
                InlineKeyboardButton("🎲 50 մետաղադրամ", callback_data="dice_50"),
                InlineKeyboardButton("🎲 100 մետաղադրամ", callback_data="dice_100")
            ],
            [
                InlineKeyboardButton("🎲 500 մետաղադրամ", callback_data="dice_500"),
                InlineKeyboardButton("🎲 1000 մետաղադրամ", callback_data="dice_1000")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="casino_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def dice_predictions() -> InlineKeyboardMarkup:
        """Предполагаемые суммы для костей"""
        keyboard = [
            [
                InlineKeyboardButton("2", callback_data="dice_pred_2"),
                InlineKeyboardButton("3", callback_data="dice_pred_3"),
                InlineKeyboardButton("4", callback_data="dice_pred_4")
            ],
            [
                InlineKeyboardButton("5", callback_data="dice_pred_5"),
                InlineKeyboardButton("6", callback_data="dice_pred_6"),
                InlineKeyboardButton("7", callback_data="dice_pred_7")
            ],
            [
                InlineKeyboardButton("8", callback_data="dice_pred_8"),
                InlineKeyboardButton("9", callback_data="dice_pred_9"),
                InlineKeyboardButton("10", callback_data="dice_pred_10")
            ],
            [
                InlineKeyboardButton("11", callback_data="dice_pred_11"),
                InlineKeyboardButton("12", callback_data="dice_pred_12")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="dice_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def crime_menu() -> InlineKeyboardMarkup:
        """Меню преступлений"""
        keyboard = [
            [
                InlineKeyboardButton("🦹 Գրպանահատություն", callback_data="crime_pickpocket"),
                InlineKeyboardButton("🔫 Կողոպուտ", callback_data="crime_robbery")
            ],
            [
                InlineKeyboardButton("🚢 Մաքսանենգություն", callback_data="crime_smuggling"),
                InlineKeyboardButton("🏦 Բանկի կողոպուտ", callback_data="crime_bank")
            ],
            [
                InlineKeyboardButton("🏘️ Տարածքներ", callback_data="territories_menu"),
                InlineKeyboardButton("🏃‍♂️ Փախուստ", callback_data="escape")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def territories_menu() -> InlineKeyboardMarkup:
        """Меню территорий"""
        keyboard = [
            [
                InlineKeyboardButton("🏘️ Գնել տարածք", callback_data="buy_territory"),
                InlineKeyboardButton("💰 Հավաքել եկամուտ", callback_data="collect_income")
            ],
            [
                InlineKeyboardButton("📊 Իմ տարածքները", callback_data="my_territories")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="crime_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def available_territories(territories: List[Dict]) -> InlineKeyboardMarkup:
        """Доступные территории для покупки"""
        keyboard = []
        
        for territory in territories:
            keyboard.append([
                InlineKeyboardButton(
                    f"🏘️ {territory['name']} ({territory['cost']} մետաղադրամ)",
                    callback_data=f"buy_territory_{territory['name']}"
                )
            ])
        
        keyboard.append([InlineKeyboardButton("🔙 Հետ", callback_data="territories_menu")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def gang_menu() -> InlineKeyboardMarkup:
        """Меню банды"""
        keyboard = [
            [
                InlineKeyboardButton("👥 Իմ խումբը", callback_data="my_gang"),
                InlineKeyboardButton("🏗️ Ստեղծել խումբ", callback_data="create_gang")
            ],
            [
                InlineKeyboardButton("🔍 Գտնել խումբ", callback_data="find_gang"),
                InlineKeyboardButton("💰 Խմբի բանկ", callback_data="gang_bank")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def shop_menu() -> InlineKeyboardMarkup:
        """Меню магазина"""
        keyboard = [
            [
                InlineKeyboardButton("🔪 Դանակ (500 մետաղադրամ)", callback_data="buy_դանակ"),
                InlineKeyboardButton("🔫 Ատրճանակ (2000 մետաղադրամ)", callback_data="buy_ատրճանակ")
            ],
            [
                InlineKeyboardButton("🔫 Հրացան (10000 մետաղադրամ)", callback_data="buy_հրացան"),
                InlineKeyboardButton("🛡️ Զրահապատ վերնաշապիկ (1000 մետաղադրամ)", callback_data="buy_զրահապատ վերնաշապիկ")
            ],
            [
                InlineKeyboardButton("👮 Կապեր ոստիկանության հետ (5000 մետաղադրամ)", callback_data="buy_կապեր ոստիկանության հետ")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def top_menu() -> InlineKeyboardMarkup:
        """Меню рейтингов"""
        keyboard = [
            [
                InlineKeyboardButton("💰 Ըստ փողի", callback_data="top_money"),
                InlineKeyboardButton("👑 Ըստ կոչման", callback_data="top_rank")
            ],
            [
                InlineKeyboardButton("⭐ Ըստ հեղինակության", callback_data="top_reputation"),
                InlineKeyboardButton("🏘️ Ըստ տարածքների", callback_data="top_territories")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def profile_actions() -> InlineKeyboardMarkup:
        """Действия с профилем"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Վիճակագրություն", callback_data="profile_stats"),
                InlineKeyboardButton("🏆 Ձեռքբերումներ", callback_data="profile_achievements")
            ],
            [
                InlineKeyboardButton("🔙 Հետ", callback_data="main_menu")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def jail_menu() -> InlineKeyboardMarkup:
        """Меню тюрьмы"""
        keyboard = [
            [
                InlineKeyboardButton("🏃‍♂️ Կազմակերպել փախուստ", callback_data="organize_escape")
            ],
            [
                InlineKeyboardButton("⏰ Մնացած ժամանակ", callback_data="jail_time")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def confirm_action(action: str, data: str = "") -> InlineKeyboardMarkup:
        """Подтверждение действия"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Այո", callback_data=f"confirm_{action}_{data}"),
                InlineKeyboardButton("❌ Ոչ", callback_data="cancel")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def back_button(menu: str) -> InlineKeyboardMarkup:
        """Кнопка назад"""
        keyboard = [
            [InlineKeyboardButton("🔙 Հետ", callback_data=menu)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def number_keyboard(max_num: int, callback_prefix: str) -> InlineKeyboardMarkup:
        """Клавиатура с числами"""
        keyboard = []
        row = []
        
        for i in range(1, max_num + 1):
            row.append(InlineKeyboardButton(str(i), callback_data=f"{callback_prefix}_{i}"))
            
            if len(row) == 3:  # 3 кнопки в ряду
                keyboard.append(row)
                row = []
        
        if row:  # Добавляем оставшиеся кнопки
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Հետ", callback_data="cancel")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def custom_keyboard(buttons: List[List[Dict]]) -> InlineKeyboardMarkup:
        """
        Создает кастомную клавиатуру
        buttons: [[{"text": "Текст", "callback_data": "data"}, ...], ...]
        """
        keyboard = []
        
        for row in buttons:
            keyboard_row = []
            for button in row:
                keyboard_row.append(InlineKeyboardButton(
                    button["text"], 
                    callback_data=button["callback_data"]
                ))
            keyboard.append(keyboard_row)
        
        return InlineKeyboardMarkup(keyboard)

# Глобальный экземпляр клавиатур
keyboards = Keyboards() 