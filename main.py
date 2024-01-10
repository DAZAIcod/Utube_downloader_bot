import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ApplicationBuilder
from pytube import YouTube
import os, re

DOWNLOAD_LOCATION = "./temp/"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    await context.bot.send_message("Welcome to NeelTubeBot")

def download(update: Update, context:ContextTypes.DEFAULT_TYPE)-> None:
    user_id = update.message.from_user['id']
    link = update.message.text
    pattern = r"http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?"
    result = re.match(pattern,link)
    if result:
        youtube = YouTube(link)
        youtube_stream = youtube.streams.get_audio_only(subtype="mp4")
        youtube_stream.download(DOWNLOAD_LOCATION)
        file_name = youtube.streams.get_highest_resolution().default_filename
        file_dir = f"{DOWNLOAD_LOCATION}{file_name}"

        context.bot.send_video(chat_id=user_id, video=open(file_dir, 'rb'), supports_streaming=True)
        os.remove(file_dir)
    else:
        update.message.reply_text('Your link is not valid')


if __name__ == "__main__":
    proxy = 'https://ngrok.com/tos '
    application = ApplicationBuilder().token('6500601453:AAECM82Q-gRvMcUxQ3XQF56Kfz6mRLS8Z2U').build()
    # updater = Updater(token="6500601453:AAECM82Q-gRvMcUxQ3XQF56Kfz6mRLS8Z2U",request_kwargs={'read_timeout': 1000, 'connect_timeout':1000}, use_context=True)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.run_polling()


