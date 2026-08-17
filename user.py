from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database as db
from utils import build_main_menu, not_banned, get_text
from config import ADMIN_IDS
from downloader import extract_info, download_queue

@not_banned
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await db.add_user(user.id, user.first_name, user.username)
    is_admin = user.id in ADMIN_IDS
    text = await get_text(user.id, 'welcome')
    await update.message.reply_html(text, reply_markup=build_main_menu(is_admin))

@not_banned
async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return
    msg = await update.message.reply_text("🔍 Analyzing link...")
    info = await extract_info(url)
    if not info:
        await msg.edit_text("❌ Could not extract information from this link.")
        return
    
    title = info.get('title', 'Unknown')
    duration = info.get('duration_string', 'N/A')
    
    text = f"🔗 <b>MEDIA FOUND</b>\n\n🎬 <b>Title:</b> {title}\n⏱ <b>Duration:</b> {duration}\n\nSelect Quality:"
    
    keyboard = []
    formats = info.get('formats', [])
    seen_res = set()
    for f in formats:
        res = f.get('resolution')
        if res and res not in seen_res and f.get('vcodec') != 'none':
            seen_res.add(res)
            keyboard.append([InlineKeyboardButton(f"🎥 {res}", callback_data=f"dl:{f['format_id']}:mp4")])
            if len(keyboard) >= 5: break # Limit options for clean UI
            
    keyboard.append([InlineKeyboardButton("🎵 MP3 (Audio)", callback_data="dl:bestaudio:mp3")])
    keyboard.append([InlineKeyboardButton("🔙 Menu", callback_data="menu:main")])
    
    # Store URL in context for callback
    context.user_data['last_url'] = url
    await msg.edit_text(text, parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

@not_banned
async def user_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    if data == "menu:main":
        text = await get_text(user_id, 'welcome')
        await query.message.edit_text(text, parse_mode='HTML', reply_markup=build_main_menu(user_id in ADMIN_IDS))
    
    elif data.startswith("dl:"):
        _, format_id, ext = data.split(":")
        url = context.user_data.get('last_url')
        if not url:
            await query.answer("URL expired. Please send again.", show_alert=True)
            return
        
        await query.message.edit_text(await get_text(user_id, 'queue'))
        await download_queue.put((user_id, url, format_id, ext, query.message.message_id))
        
    await query.answer()
