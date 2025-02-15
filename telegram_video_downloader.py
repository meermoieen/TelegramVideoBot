import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not found! Make sure to set it in your .env file or GitHub Secrets.")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a video URL to download.")

# Video download handler
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'best',
        'noplaylist': True,
    }

    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⏳ Downloading the video...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = f"{info_dict.get('title', 'video')}.mp4"

            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(file_name, 'rb'))
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ Video '{file_name}' sent!")

            # Clean up the downloaded file
            os.remove(file_name)
    except yt_dlp.utils.DownloadError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Failed to download: {str(e)}")
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred: {str(e)}")

# Main function
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.run_polling()

if __name__ == '__main__':
    main()