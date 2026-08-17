import logging
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN, PORT
import database as db
from keep_alive import start_server
from user import start_cmd, handle_url, user_callbacks
from admin import admin_callbacks
from downloader import process_queue_worker

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def post_init(application):
    await db.init_db()
    # Start the async download queue worker in background
    asyncio.create_task(process_queue_worker(application))
    logging.info("Database initialized and Worker started.")

def main():
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is missing!")
        return

    start_server(PORT)
    
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # Callback Handlers
    application.add_handler(CallbackQueryHandler(admin_callbacks, pattern="^admin:"))
    application.add_handler(CallbackQueryHandler(user_callbacks, pattern="^(menu|dl):"))

    application.run_polling()

if __name__ == '__main__':
    main()
