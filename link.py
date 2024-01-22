from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import re
import os

TOKEN = os.environ.get('BOT_TOKEN')

def start(update, context):
    update.message.reply_text('Hello! Send me messages in the format: "Location Name\nGoogle Maps URL" on each line.')

def handle_message(update, context):
    message_text = update.message.text
    lines = message_text.strip().split('\n')

    reply_texts = []
    url_pattern = re.compile(r'https?://www\.google\.com/maps/place/')

    for line in lines:
        # Split the line into name and URL
        parts = line.rsplit(' ', 1) # Splitting from the end to get the last part as URL
        if len(parts) == 2 and url_pattern.match(parts[1]):
            location_name, url = parts
            reply_texts.append(f"[{location_name}]({url})")
        else:
            reply_texts.append("Invalid line format or URL")

    update.message.reply_text('\n'.join(reply_texts), parse_mode='Markdown', disable_web_page_preview=True)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
