import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a video downloader bot. Just send me the URL of the video you want to download.")

# Video download handler
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Save the video with its title as the filename
        'format': 'best',                # Download the best available quality
        'noplaylist': True,              # Avoid downloading playlists
    }

    try:
        # Send a "Please wait" message
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⏳ Please wait, the video is being downloaded...")

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict.get('title', 'Unknown Title')
            file_name = f"{title}.mp4"  # Construct the file name

            # Send the video file to the user
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(file_name, 'rb'))

            # Send a confirmation message
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"✅ Video '{title}' has been downloaded and sent!")
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Failed to download the video. Error: {str(e)}")

# Main function to start the bot
def main() -> None:
    # Replace 'YOUR_API_TOKEN' with your bot's API token
    application = ApplicationBuilder().token("7428602061:AAEL5hiEvkS8X2j3zqGNCKXx070wo0UMa_E").build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()