# PRO MEDIA DOWNLOADER

A professional, production-ready Telegram Bot to download and process media securely and asynchronously.

## Features
- Async Downloads via `yt-dlp`
- Media processing via `FFmpeg` (Video -> Audio, GIF, Cut)
- SQLite Database User & Premium Management
- Secure Admin Panel (Restricted by Telegram ID)
- Multi-language support (English/Bengali)
- Background Task Queue (Avoids blocking event loop)
- Flask Health check for Render deployments

## Setup Instructions

### 1. Create Telegram Bot
Go to [@BotFather](https://t.me/BotFather) on Telegram, create a new bot, and copy the `BOT_TOKEN`.

### 2. Get your Telegram ID
Message [@userinfobot](https://t.me/userinfobot) to get your numeric ID (e.g., `6836865426`).

### 3. Run Locally
1. Install Python 3.11+ and FFmpeg on your machine.
2. Clone repository.
3. Create a `.env` file based on the template below.
4. Run:
   ```bash
   pip install -r requirements.txt
   python bot.py
