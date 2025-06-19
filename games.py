"""
Модуль с игровой логикой казино
Реализует слоты, рулетку, блэкджек, кости и покер
"""

import random
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import logging
from config import SLOT_SYMBOLS

logger = logging.getLogger(__name__)

class CasinoGames:
    def __init__(self):
        self.deck = []
        self.reset_deck()
    
    def reset_deck(self):
        """Создает новую колоду карт"""
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [f"{rank}{suit}" for suit in suits for rank in ranks]
        random.shuffle(self.deck)
    
    def play_slots(self, bet: int) -> Dict:
        """
        Игра в слоты
        Возвращает результат с выигрышем и комбинацией
        """
        if bet <= 0:
            return {"success": False, "message": "Ставка должна быть больше 0"}
        
        # Генерируем 3 символа
        symbols = list(SLOT_SYMBOLS.keys())
        result = [random.choice(symbols) for _ in range(3)]
        
        # Проверяем выигрышные комбинации
        win_multiplier = 0
        win_message = ""
        
        # Три одинаковых символа
        if len(set(result)) == 1:
            symbol = result[0]
            win_multiplier = SLOT_SYMBOLS[symbol]
            win_message = f"🎉 ДЖЕКПОТ! Три {symbol} - x{win_multiplier}!"
        
        # Два одинаковых символа
        elif len(set(result)) == 2:
            # Находим символ, который встречается дважды
            for symbol in set(result):
                if result.count(symbol) == 2:
                    win_multiplier = SLOT_SYMBOLS[symbol] // 2
                    win_message = f"🎯 Два {symbol} - x{win_multiplier}!"
                    break
        
        # Нет выигрыша
        else:
            win_message = "😔 Не повезло! Попробуйте еще раз!"
        
        win_amount = bet * win_multiplier
        
        return {
            "success": True,
            "result": result,
            "win_amount": win_amount,
            "win_multiplier": win_multiplier,
            "message": win_message,
            "bet": bet
        }
    
    def play_roulette(self, bet_type: str, bet_value: str, bet_amount: int) -> Dict:
        """
        Игра в рулетку
        bet_type: "color", "number", "even_odd"
        """
        if bet_amount <= 0:
            return {"success": False, "message": "Ставка должна быть больше 0"}
        
        # Генерируем случайное число от 0 до 36
        number = random.randint(0, 36)
        
        # Определяем цвет числа
        if number == 0:
            color = "зеленый"
        elif number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
            color = "красный"
        else:
            color = "черный"
        
        win_amount = 0
        win_message = ""
        
        if bet_type == "color":
            if bet_value == color:
                win_amount = bet_amount * 2
                win_message = f"🎉 Выигрыш! {color.capitalize()} - x2!"
            else:
                win_message = f"😔 Не повезло! Выпал {color}"
        
        elif bet_type == "number":
            if str(number) == bet_value:
                win_amount = bet_amount * 35
                win_message = f"🎉 ДЖЕКПОТ! Число {number} - x35!"
            else:
                win_message = f"😔 Не повезло! Выпало число {number}"
        
        elif bet_type == "even_odd":
            if number == 0:
                win_message = "😔 Не повезло! Выпал 0"
            elif (number % 2 == 0 and bet_value == "четное") or (number % 2 == 1 and bet_value == "нечетное"):
                win_amount = bet_amount * 2
                win_message = f"🎉 Выигрыш! {bet_value.capitalize()} - x2!"
            else:
                win_message = f"😔 Не повезло! Выпало {'четное' if number % 2 == 0 else 'нечетное'} число"
        
        return {
            "success": True,
            "number": number,
            "color": color,
            "win_amount": win_amount,
            "message": win_message,
            "bet": bet_amount
        }
    
    def play_blackjack(self, bet: int) -> Dict:
        """
        Игра в блэкджек
        Возвращает начальные карты игрока и дилера
        """
        if bet <= 0:
            return {"success": False, "message": "Ставка должна быть больше 0"}
        
        self.reset_deck()
        
        # Раздаем карты
        player_cards = [self.deck.pop(), self.deck.pop()]
        dealer_cards = [self.deck.pop(), self.deck.pop()]
        
        # Скрываем одну карту дилера
        dealer_visible = [dealer_cards[0], "🂠"]
        
        return {
            "success": True,
            "player_cards": player_cards,
            "dealer_cards": dealer_cards,
            "dealer_visible": dealer_visible,
            "bet": bet,
            "game_state": "playing"
        }
    
    def blackjack_hit(self, player_cards: List[str], dealer_cards: List[str], bet: int) -> Dict:
        """Добавляет карту игроку в блэкджеке"""
        if len(self.deck) == 0:
            self.reset_deck()
        
        player_cards.append(self.deck.pop())
        player_score = self.calculate_blackjack_score(player_cards)
        
        if player_score > 21:
            return {
                "success": True,
                "player_cards": player_cards,
                "dealer_cards": dealer_cards,
                "win_amount": 0,
                "message": f"💥 Перебор! Ваш счет: {player_score}",
                "game_state": "bust"
            }
        
        return {
            "success": True,
            "player_cards": player_cards,
            "dealer_cards": dealer_cards,
            "game_state": "playing"
        }
    
    def blackjack_stand(self, player_cards: List[str], dealer_cards: List[str], bet: int) -> Dict:
        """Завершает игру в блэкджеке"""
        player_score = self.calculate_blackjack_score(player_cards)
        
        # Дилер берет карты до 17 или больше
        while self.calculate_blackjack_score(dealer_cards) < 17:
            if len(self.deck) == 0:
                self.reset_deck()
            dealer_cards.append(self.deck.pop())
        
        dealer_score = self.calculate_blackjack_score(dealer_cards)
        
        # Определяем победителя
        if dealer_score > 21:
            win_amount = bet * 2
            message = f"🎉 Дилер перебрал! Выигрыш: {win_amount} монет"
        elif player_score > dealer_score:
            win_amount = bet * 2
            message = f"🎉 Выигрыш! {player_score} vs {dealer_score}"
        elif player_score < dealer_score:
            win_amount = 0
            message = f"😔 Проигрыш! {player_score} vs {dealer_score}"
        else:
            win_amount = bet  # Возврат ставки
            message = f"🤝 Ничья! {player_score} vs {dealer_score}"
        
        return {
            "success": True,
            "player_cards": player_cards,
            "dealer_cards": dealer_cards,
            "win_amount": win_amount,
            "message": message,
            "game_state": "finished"
        }
    
    def calculate_blackjack_score(self, cards: List[str]) -> int:
        """Вычисляет счет в блэкджеке"""
        score = 0
        aces = 0
        
        for card in cards:
            if card == "🂠":  # Скрытая карта
                continue
            
            rank = card[:-1]  # Убираем масть
            
            if rank in ['J', 'Q', 'K']:
                score += 10
            elif rank == 'A':
                aces += 1
            else:
                score += int(rank)
        
        # Добавляем тузы
        for _ in range(aces):
            if score + 11 <= 21:
                score += 11
            else:
                score += 1
        
        return score
    
    def play_dice(self, bet: int, prediction: int) -> Dict:
        """
        Игра в кости
        prediction: предполагаемая сумма двух кубиков (2-12)
        """
        if bet <= 0:
            return {"success": False, "message": "Ставка должна быть больше 0"}
        
        if prediction < 2 or prediction > 12:
            return {"success": False, "message": "Предполагаемая сумма должна быть от 2 до 12"}
        
        # Бросаем два кубика
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        total = dice1 + dice2
        
        if total == prediction:
            # Выигрыш зависит от вероятности
            if prediction in [2, 12]:
                win_amount = bet * 30  # 1/36 вероятность
            elif prediction in [3, 11]:
                win_amount = bet * 15  # 2/36 вероятность
            elif prediction in [4, 10]:
                win_amount = bet * 10  # 3/36 вероятность
            elif prediction in [5, 9]:
                win_amount = bet * 7   # 4/36 вероятность
            elif prediction in [6, 8]:
                win_amount = bet * 6   # 5/36 вероятность
            else:  # 7
                win_amount = bet * 5   # 6/36 вероятность
            
            message = f"🎉 Угадали! {dice1} + {dice2} = {total} - x{win_amount//bet}!"
        else:
            win_amount = 0
            message = f"😔 Не угадали! {dice1} + {dice2} = {total}"
        
        return {
            "success": True,
            "dice": [dice1, dice2],
            "total": total,
            "prediction": prediction,
            "win_amount": win_amount,
            "message": message,
            "bet": bet
        }
    
    def play_poker(self, players: List[int], bets: Dict[int, int]) -> Dict:
        """
        Игра в покер (упрощенная версия)
        players: список ID игроков
        bets: словарь с ставками игроков
        """
        if len(players) < 2:
            return {"success": False, "message": "Нужно минимум 2 игрока"}
        
        self.reset_deck()
        
        # Раздаем карты
        player_hands = {}
        for player_id in players:
            player_hands[player_id] = [self.deck.pop(), self.deck.pop()]
        
        # Общие карты (флоп)
        community_cards = [self.deck.pop(), self.deck.pop(), self.deck.pop()]
        
        # Вычисляем силу рук
        hand_strengths = {}
        for player_id, hand in player_hands.items():
            strength = self.calculate_poker_hand_strength(hand + community_cards)
            hand_strengths[player_id] = strength
        
        # Определяем победителя
        winner_id = max(hand_strengths, key=hand_strengths.get)
        total_pot = sum(bets.values())
        
        return {
            "success": True,
            "player_hands": player_hands,
            "community_cards": community_cards,
            "hand_strengths": hand_strengths,
            "winner_id": winner_id,
            "total_pot": total_pot,
            "message": f"Победитель: игрок {winner_id} с рукой {hand_strengths[winner_id]}"
        }
    
    def calculate_poker_hand_strength(self, cards: List[str]) -> int:
        """
        Упрощенный расчет силы покерной руки
        Возвращает числовое значение силы руки
        """
        # Упрощенная реализация - считаем только пары
        ranks = [card[:-1] for card in cards]
        rank_counts = {}
        
        for rank in ranks:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
        
        # Находим максимальное количество одинаковых карт
        max_count = max(rank_counts.values()) if rank_counts else 0
        
        # Простая оценка силы руки
        if max_count == 4:
            return 8  # Каре
        elif max_count == 3:
            return 4  # Тройка
        elif max_count == 2:
            pairs = sum(1 for count in rank_counts.values() if count == 2)
            return 3 if pairs == 2 else 2  # Две пары или пара
        else:
            return 1  # Старшая карта

# Глобальный экземпляр игр
casino_games = CasinoGames() 