import asyncio
import yt_dlp
import os
import uuid
from config import TEMP_DIR
import media_tools
import database as db

download_queue = asyncio.Queue()

def extract_info_sync(url):
    ydl_opts = {'quiet': True, 'no_warnings': True, 'extract_flat': False}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception:
        return None

async def extract_info(url):
    return await asyncio.to_thread(extract_info_sync, url)

def download_sync(url, format_id, ext="mp4"):
    filename = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}.{ext}")
    ydl_opts = {
        'format': f'{format_id}+bestaudio/best' if ext == 'mp4' else format_id,
        'outtmpl': filename,
        'quiet': True,
        'merge_output_format': ext
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename
    except Exception:
        return None

async def process_queue_worker(app):
    while True:
        task = await download_queue.get()
        chat_id, url, format_id, ext, msg_id = task
        try:
            await app.bot.edit_message_text("⚙️ Processing download...", chat_id=chat_id, message_id=msg_id)
            filepath = await asyncio.to_thread(download_sync, url, format_id, ext)
            if filepath and os.path.exists(filepath):
                await app.bot.edit_message_text("✅ Uploading...", chat_id=chat_id, message_id=msg_id)
                with open(filepath, 'rb') as f:
                    if ext in ['mp4', 'mkv']:
                        await app.bot.send_video(chat_id=chat_id, video=f)
                    else:
                        await app.bot.send_audio(chat_id=chat_id, audio=f)
                await db.log_download(chat_id, "Media", "Video/Audio", format_id)
                await app.bot.delete_message(chat_id=chat_id, message_id=msg_id)
            else:
                await app.bot.edit_message_text("❌ Download failed.", chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            await app.bot.edit_message_text(f"❌ Error: {str(e)}", chat_id=chat_id, message_id=msg_id)
        finally:
            if 'filepath' in locals():
                media_tools.cleanup_temp_files([filepath])
            download_queue.task_done()
