import motor.motor_asyncio
from datetime import datetime

class MongoDB:
    def __init__(self, uri, db_name="telegram_game"):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.users = self.db["users"]

    async def get_user(self, user_id):
        return await self.users.find_one({"user_id": user_id})

    async def create_user(self, user_id, username, name):
        user_data = {
            "user_id": user_id,
            "username": username,
            "name": name,
            "money": 1000,
            "rank": "Շեստյորկա",
            "reputation": {"копы": 0, "мафия": 0, "граждане": 0},
            "territories": [],
            "inventory": [],
            "jail_time": None,
            "jail_start": None,
            "daily_bonus_time": None,
            "last_crime_time": None,
            "last_casino_time": None,
            "last_territory_income": None,
            "gang": None,
            "statistics": {
                "games_played": 0,
                "games_won": 0,
                "crimes_committed": 0,
                "crimes_successful": 0,
                "money_earned": 0,
                "money_lost": 0
            },
            "achievements": [],
            "created_at": datetime.now().isoformat(),
            "banned": False
        }
        await self.users.insert_one(user_data)
        return user_data

    async def update_user(self, user_id, updates: dict):
        await self.users.update_one({"user_id": user_id}, {"$set": updates})

    async def get_top_users(self, by="money", limit=10):
        sort_key = by if by in ["money", "rank"] else None
        if by == "reputation":
            cursor = self.users.find().sort([("reputation.копы", -1), ("reputation.мафия", -1), ("reputation.граждане", -1)]).limit(limit)
        elif sort_key:
            cursor = self.users.find().sort(sort_key, -1).limit(limit)
        else:
            cursor = self.users.find().limit(limit)
        return [user async for user in cursor]

    async def get_all_users(self):
        cursor = self.users.find()
        return [user async for user in cursor] 