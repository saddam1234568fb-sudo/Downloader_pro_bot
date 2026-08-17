import psutil
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database as db
from utils import admin_only
import downloader

@admin_only
async def admin_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "admin:main":
        async with aiosqlite.connect(db.DB_PATH) as conn:
            cursor = await conn.execute("SELECT COUNT(*) FROM users")
            total_users = (await cursor.fetchone())[0]
            cursor = await conn.execute("SELECT COUNT(*) FROM downloads")
            total_dl = (await cursor.fetchone())[0]
            
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        queue_size = downloader.download_queue.qsize()
        
        text = (f"👑 <b>ADMIN CONTROL CENTER</b>\n\n"
                f"👥 <b>Total Users:</b> {total_users}\n"
                f"📥 <b>Total Downloads:</b> {total_dl}\n"
                f"⏳ <b>Queue Size:</b> {queue_size}\n"
                f"🖥 <b>Server CPU:</b> {cpu}%\n"
                f"💾 <b>Server RAM:</b> {ram}%")
                
        kb = [
            [InlineKeyboardButton("👥 Users", callback_data="admin:users"), InlineKeyboardButton("📢 Broadcast", callback_data="admin:broadcast")],
            [InlineKeyboardButton("🧹 Clean Temp", callback_data="admin:clean"), InlineKeyboardButton("🔧 Maintenance", callback_data="admin:maint")],
            [InlineKeyboardButton("🔙 Exit Admin", callback_data="menu:main")]
        ]
        await query.message.edit_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(kb))
    
    elif data == "admin:clean":
        import glob
        from config import TEMP_DIR
        import os
        files = glob.glob(f"{TEMP_DIR}/*")
        for f in files:
            try: os.remove(f)
            except: pass
        await query.answer(f"Cleaned {len(files)} temporary files.", show_alert=True)
        
    elif data == "admin:maint":
        current = await db.get_setting("maintenance", "0")
        new_val = "0" if current == "1" else "1"
        await db.set_setting("maintenance", new_val)
        status = "ENABLED" if new_val == "1" else "DISABLED"
        await query.answer(f"Maintenance mode {status}", show_alert=True)

    await query.answer()
