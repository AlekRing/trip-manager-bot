from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re
import os

TOKEN = os.environ.get('BOT_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a place name and Google Maps URL.')

def echo(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    pattern = r"(.+?)\s(https://maps\.app\.goo\.gl/.+)"
    match = re.search(pattern, message)
    if match:
        place_name, url = match.groups()
        response = f"[{place_name}]({url})"
        update.message.reply_markdown(response)
    else:
        update.message.reply_text("Please send a place name followed by a Google Maps URL.")

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
