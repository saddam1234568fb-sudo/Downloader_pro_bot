import os
from functools import wraps
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import ADMIN_IDS, TEMP_DIR
import database as db

LANG = {
    'en': {
        'welcome': "🎬 <b>PRO MEDIA DOWNLOADER</b>\n\nWelcome to the most advanced media bot. Choose an option below:",
        'banned': "🚫 You are banned from using this bot.",
        'maintenance': "🔧 Bot is temporarily under maintenance.",
        'queue': "⏳ Your request is in queue...",
        'error': "❌ An error occurred processing your request.",
        'file_large': "❌ File is too large for Telegram limits."
    },
    'bn': {
        'welcome': "🎬 <b>প্রো মিডিয়া ডাউনলোডার</b>\n\nসবচেয়ে উন্নত মিডিয়া বটে স্বাগতম। নিচের একটি বিকল্প বেছে নিন:",
        'banned': "🚫 আপনাকে এই বট ব্যবহার থেকে নিষিদ্ধ করা হয়েছে।",
        'maintenance': "🔧 বট সাময়িকভাবে রক্ষণাবেক্ষণের অধীনে রয়েছে।",
        'queue': "⏳ আপনার অনুরোধ সারিতে আছে...",
        'error': "❌ আপনার অনুরোধ প্রক্রিয়া করতে একটি ত্রুটি হয়েছে।",
        'file_large': "❌ ফাইলটি টেলিগ্রাম লিমিটের চেয়ে বড়।"
    }
}

async def get_text(user_id, key):
    user = await db.get_user(user_id)
    lang = user['lang'] if user else 'en'
    return LANG.get(lang, LANG['en']).get(key, LANG['en'].get(key, key))

def admin_only(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            if update.callback_query:
                await update.callback_query.answer("⛔ Access Denied.", show_alert=True)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def not_banned(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        user = await db.get_user(user_id)
        if user and user['is_banned']:
            msg = await get_text(user_id, 'banned')
            if update.callback_query:
                await update.callback_query.answer(msg, show_alert=True)
            else:
                await update.message.reply_text(msg)
            return
        maintenance = await db.get_setting("maintenance", "0")
        if maintenance == "1" and user_id not in ADMIN_IDS:
            msg = await get_text(user_id, 'maintenance')
            if update.callback_query:
                await update.callback_query.answer(msg, show_alert=True)
            else:
                await update.message.reply_text(msg)
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def cleanup_temp_files(filepaths):
    for fp in filepaths:
        if fp and os.path.exists(fp):
            try:
                os.remove(fp)
            except Exception:
                pass

def build_main_menu(is_admin=False):
    keyboard = [
        [InlineKeyboardButton("🔗 Download Media", callback_data="menu:download")],
        [InlineKeyboardButton("🎵 Audio", callback_data="menu:audio"), InlineKeyboardButton("🎬 Vid→Aud", callback_data="menu:vid2aud")],
        [InlineKeyboardButton("🖼 Thumbnail", callback_data="menu:thumb"), InlineKeyboardButton("🌄 Wallpaper", callback_data="menu:wall")],
        [InlineKeyboardButton("✂️ Cutter", callback_data="menu:cut"), InlineKeyboardButton("🎞 GIF Maker", callback_data="menu:gif")],
        [InlineKeyboardButton("📜 History", callback_data="menu:history"), InlineKeyboardButton("👤 Profile", callback_data="menu:profile")],
        [InlineKeyboardButton("⭐ Premium", callback_data="menu:premium"), InlineKeyboardButton("⚙️ Settings", callback_data="menu:settings")],
        [InlineKeyboardButton("🌐 Language", callback_data="menu:lang"), InlineKeyboardButton("📢 Support", url="https://t.me/Support")]
    ]
    if is_admin:
        keyboard.append([InlineKeyboardButton("👑 ADMIN PANEL", callback_data="admin:main")])
    return InlineKeyboardMarkup(keyboard)
