import database as db

async def get_premium_status(user_id):
    user = await db.get_user(user_id)
    if not user:
        return "FREE"
    return user['premium_tier']

async def set_premium(user_id, tier):
    async with aiosqlite.connect(db.DB_PATH) as conn:
        is_prem = 1 if tier in ["PRO", "ULTRA"] else 0
        await conn.execute("UPDATE users SET is_premium = ?, premium_tier = ? WHERE user_id = ?", (is_prem, tier, user_id))
        await conn.commit()
