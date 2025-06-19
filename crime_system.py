"""
Модуль криминальной системы
Реализует преступления, тюрьму, территории и банды
"""

import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
from config import CRIMES, TERRITORIES, COOLDOWNS

logger = logging.getLogger(__name__)

class CrimeSystem:
    def __init__(self):
        self.active_escapes = {}  # Активные попытки побега
    
    def commit_crime(self, user_id: int, crime_type: str, user_data: Dict) -> Dict:
        """
        Совершает преступление
        Возвращает результат с наградами или наказанием
        """
        if crime_type not in CRIMES:
            return {"success": False, "message": "Անհայտ հանցագործություն"}
        
        crime_info = CRIMES[crime_type]
        
        # Проверяем требования
        if user_data["money"] < crime_info["min_money"]:
            return {
                "success": False, 
                "message": f"Պետք է նվազագույնը {crime_info['min_money']} մետաղադրամ {crime_type}-ի համար"
            }
        
        # Проверяем кулдаун
        if user_data.get("last_crime_time"):
            last_crime = datetime.fromisoformat(user_data["last_crime_time"])
            if datetime.now() - last_crime < timedelta(seconds=COOLDOWNS["crime"]):
                remaining = COOLDOWNS["crime"] - (datetime.now() - last_crime).seconds
                return {
                    "success": False,
                    "message": f"Սպասեք {remaining} վայրկյան հաջորդ հանցագործությունից առաջ"
                }
        
        # Проверяем, не в тюрьме ли игрок
        if user_data.get("jail_time"):
            jail_end = datetime.fromisoformat(user_data["jail_time"])
            if jail_end > datetime.now():
                return {"success": False, "message": "Դուք բանտում եք! Սպասեք ազատ արձակմանը"}
        
        # Определяем успех преступления
        success = random.random() < crime_info["success_rate"]
        
        if success:
            # Успешное преступление
            reward = random.randint(*crime_info["reward"])
            new_money = user_data["money"] + reward
            
            # Обновляем репутацию
            new_reputation = user_data["reputation"].copy()
            for faction, change in crime_info["reputation_change"].items():
                new_reputation[faction] += change
            
            # Обновляем статистику
            new_stats = user_data["statistics"].copy()
            new_stats["crimes_committed"] += 1
            new_stats["crimes_successful"] += 1
            new_stats["money_earned"] += reward
            
            return {
                "success": True,
                "crime_success": True,
                "reward": reward,
                "new_money": new_money,
                "reputation_changes": crime_info["reputation_change"],
                "new_reputation": new_reputation,
                "new_stats": new_stats,
                "message": f"✅ Հաջող {crime_type}! +{reward} մետաղադրամ"
            }
        else:
            # Неудачное преступление - тюрьма
            jail_time = crime_info["jail_time"]
            jail_end = datetime.now() + timedelta(seconds=jail_time)
            
            # Обновляем репутацию (меньше, чем при успехе)
            new_reputation = user_data["reputation"].copy()
            for faction, change in crime_info["reputation_change"].items():
                new_reputation[faction] += change // 2  # Меньше изменения репутации
            
            # Обновляем статистику
            new_stats = user_data["statistics"].copy()
            new_stats["crimes_committed"] += 1
            
            return {
                "success": True,
                "crime_success": False,
                "jail_time": jail_end.isoformat(),
                "reputation_changes": {k: v // 2 for k, v in crime_info["reputation_change"].items()},
                "new_reputation": new_reputation,
                "new_stats": new_stats,
                "message": f"🚔 Բռնվեցին! {crime_type} չհաջողվեց: Բանտ {jail_time//60} րոպե"
            }
    
    def organize_escape(self, user_id: int, user_data: Dict) -> Dict:
        """
        Организует побег из тюрьмы
        """
        if not user_data.get("jail_time"):
            return {"success": False, "message": "Դուք բանտում չեք"}
        
        jail_end = datetime.fromisoformat(user_data["jail_time"])
        if jail_end <= datetime.now():
            return {"success": False, "message": "Դուք բանտում չեք"}
        
        # Проверяем, не пытается ли уже сбежать
        if user_id in self.active_escapes:
            return {"success": False, "message": "Փախուստը արդեն կազմակերպված է"}
        
        # Стоимость побега зависит от оставшегося времени
        remaining_time = (jail_end - datetime.now()).total_seconds()
        escape_cost = max(100, int(remaining_time // 10))
        
        if user_data["money"] < escape_cost:
            return {
                "success": False,
                "message": f"Պետք է {escape_cost} մետաղադրամ փախուստ կազմակերպելու համար"
            }
        
        # Шанс успешного побега зависит от связей с копами
        cop_connections = user_data["reputation"].get("копы", 0)
        escape_chance = min(0.8, 0.3 + (cop_connections * 0.02))
        
        success = random.random() < escape_chance
        
        if success:
            # Успешный побег
            new_money = user_data["money"] - escape_cost
            
            return {
                "success": True,
                "escape_success": True,
                "cost": escape_cost,
                "new_money": new_money,
                "message": f"🏃‍♂️ Փախուստը հաջողվեց! Ծախսված {escape_cost} մետաղադրամ"
            }
        else:
            # Неудачный побег - увеличиваем срок
            additional_time = int(remaining_time // 2)
            new_jail_end = jail_end + timedelta(seconds=additional_time)
            
            return {
                "success": True,
                "escape_success": False,
                "cost": escape_cost,
                "new_jail_time": new_jail_end.isoformat(),
                "message": f"🚔 Փախուստը չհաջողվեց! Ժամկետը երկարացվեց {additional_time//60} րոպեով"
            }
    
    def buy_territory(self, user_id: int, territory_name: str, user_data: Dict) -> Dict:
        """
        Покупает территорию
        """
        if territory_name not in TERRITORIES:
            return {"success": False, "message": "Անհայտ տարածք"}
        
        territory_info = TERRITORIES[territory_name]
        
        # Проверяем, есть ли уже эта территория
        if territory_name in user_data["territories"]:
            return {"success": False, "message": "Դուք արդեն ունեք այս տարածքը"}
        
        # Проверяем деньги
        if user_data["money"] < territory_info["cost"]:
            return {
                "success": False,
                "message": f"Պետք է {territory_info['cost']} մետաղադրամ {territory_name} գնելու համար"
            }
        
        # Покупаем территорию
        new_money = user_data["money"] - territory_info["cost"]
        new_territories = user_data["territories"] + [territory_name]
        
        return {
            "success": True,
            "territory_name": territory_name,
            "cost": territory_info["cost"],
            "income": territory_info["income"],
            "new_money": new_money,
            "new_territories": new_territories,
            "message": f"🏘️ Գնված տարածք {territory_name}! Եկամուտ: {territory_info['income']} մետաղադրամ/ժամ"
        }
    
    def collect_territory_income(self, user_id: int, user_data: Dict) -> Dict:
        """
        Собирает доход с территорий
        """
        if not user_data["territories"]:
            return {"success": False, "message": "У вас нет территорий"}
        
        # Проверяем кулдаун
        if user_data.get("last_territory_income"):
            last_income = datetime.fromisoformat(user_data["last_territory_income"])
            if datetime.now() - last_income < timedelta(seconds=COOLDOWNS["territory_income"]):
                remaining = COOLDOWNS["territory_income"] - (datetime.now() - last_income).seconds
                return {
                    "success": False,
                    "message": f"Подождите {remaining//60} минут перед следующим сбором"
                }
        
        # Вычисляем доход
        total_income = 0
        territory_incomes = {}
        
        for territory_name in user_data["territories"]:
            if territory_name in TERRITORIES:
                income = TERRITORIES[territory_name]["income"]
                risk = TERRITORIES[territory_name]["risk"]
                
                # Есть риск потерять территорию
                if random.random() < risk:
                    # Территория захвачена
                    new_territories = [t for t in user_data["territories"] if t != territory_name]
                    return {
                        "success": True,
                        "territory_lost": territory_name,
                        "new_territories": new_territories,
                        "message": f"💥 Территория {territory_name} захвачена конкурентами!"
                    }
                else:
                    total_income += income
                    territory_incomes[territory_name] = income
        
        new_money = user_data["money"] + total_income
        
        return {
            "success": True,
            "total_income": total_income,
            "territory_incomes": territory_incomes,
            "new_money": new_money,
            "message": f"💰 Собран доход: +{total_income} монет"
        }
    
    def attack_territory(self, attacker_id: int, target_id: int, attacker_data: Dict, target_data: Dict) -> Dict:
        """
        Атакует территорию другого игрока
        """
        if not target_data["territories"]:
            return {"success": False, "message": "У цели нет территорий для захвата"}
        
        if not attacker_data["territories"]:
            return {"success": False, "message": "У вас должны быть свои территории для атаки"}
        
        # Проверяем, не в тюрьме ли атакующий
        if attacker_data["jail_time"] > 0:
            return {"success": False, "message": "Вы в тюрьме! Не можете атаковать"}
        
        # Выбираем случайную территорию цели
        target_territory = random.choice(target_data["territories"])
        
        # Шанс успеха зависит от разницы в репутации мафии
        attacker_mafia_rep = attacker_data["reputation"].get("мафия", 0)
        target_mafia_rep = target_data["reputation"].get("мафия", 0)
        
        success_chance = 0.3 + (attacker_mafia_rep - target_mafia_rep) * 0.01
        success_chance = max(0.1, min(0.9, success_chance))
        
        success = random.random() < success_chance
        
        if success:
            # Успешная атака
            new_attacker_territories = attacker_data["territories"] + [target_territory]
            new_target_territories = [t for t in target_data["territories"] if t != target_territory]
            
            # Изменения репутации
            attacker_rep = attacker_data["reputation"].copy()
            attacker_rep["мафия"] += 5
            attacker_rep["граждане"] -= 3
            
            target_rep = target_data["reputation"].copy()
            target_rep["мафия"] -= 2
            
            return {
                "success": True,
                "attack_success": True,
                "territory": target_territory,
                "new_attacker_territories": new_attacker_territories,
                "new_target_territories": new_target_territories,
                "attacker_rep_changes": {"мафия": 5, "граждане": -3},
                "target_rep_changes": {"мафия": -2},
                "new_attacker_rep": attacker_rep,
                "new_target_rep": target_rep,
                "message": f"⚔️ Территория {target_territory} захвачена!"
            }
        else:
            # Неудачная атака
            attacker_rep = attacker_data["reputation"].copy()
            attacker_rep["мафия"] -= 3
            attacker_rep["копы"] -= 2
            
            return {
                "success": True,
                "attack_success": False,
                "attacker_rep_changes": {"мафия": -3, "копы": -2},
                "new_attacker_rep": attacker_rep,
                "message": f"💥 Атака на {target_territory} провалилась!"
            }
    
    def get_available_crimes(self, user_data: Dict) -> List[Dict]:
        """Получает список доступных преступлений"""
        available = []
        
        for crime_name, crime_info in CRIMES.items():
            if user_data["money"] >= crime_info["min_money"]:
                available.append({
                    "name": crime_name,
                    "success_rate": crime_info["success_rate"],
                    "reward_range": crime_info["reward"],
                    "jail_time": crime_info["jail_time"],
                    "reputation_changes": crime_info["reputation_change"]
                })
        
        return available
    
    def get_available_territories(self, user_data: Dict) -> List[Dict]:
        """Получает список доступных территорий"""
        available = []
        
        for territory_name, territory_info in TERRITORIES.items():
            if territory_name not in user_data["territories"]:
                available.append({
                    "name": territory_name,
                    "cost": territory_info["cost"],
                    "income": territory_info["income"],
                    "risk": territory_info["risk"]
                })
        
        return available

# Глобальный экземпляр криминальной системы
crime_system = CrimeSystem() 