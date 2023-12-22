import telebot
import argparse
import re
import os

import dotenv

dotenv.load_dotenv(os.path.join(os.environ.get("ENV_DIR", os.getcwd()), ".env"))

from_env = lambda key, default: os.environ.get(key, default)

BOT_TOKEN = from_env("telebot", False)

assert BOT_TOKEN, "Add telegram bot token to the .env file"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

WEBHOOK_URL = from_env("webhook_url", "")  # Replace with your server
bot.remove_webhook()  # Remove existing webhook
bot.set_webhook(url=os.path.join(WEBHOOK_URL, BOT_TOKEN))

help_message = """
/start - Show this help message
<text> - Generate QR code 
"""


parser = argparse.ArgumentParser()
parser.add_argument(
    "data",
    help="Text to generate qrcode from",
    nargs="*",
)
parser.add_argument(
    "-f", "-fit", action="store_true", default=True, help="Center the qrcode"
)
parser.add_argument("-v", "--version", type=int, help="QRcode version", default=1)
parser.add_argument(
    "-s",
    "--size",
    help="Size of each box",
    default=10,
    type=int,
)
parser.add_argument(
    "-b", "--border", help="Number of modules/dots around QR Code.", type=int, default=5
)
parser.add_argument("-fc", "--fill-color", help="Self explanatory", default="black")
parser.add_argument("-bc", "--back-color", help="Background color", default="white")


@bot.message_handler(commands=["start"])
def show_help(message):
    bot.send_message(message.chat.id, text=help_message)


@bot.message_handler(func=lambda msg: True)
def generate_qrcode(message):
    try:
        raw_string = re.sub(
            "--help", "", re.sub("-h", "", message.text)
        )  # ensures --help/-h aint parsed
        args = parser.parse_args(args=raw_string.split(" "))
        params = f"v1?data={args.data}&fit={args.fit}&version={args.version}&box_size={args.size}&border={args.border}&fill_color={args.fill_color}&back_color={args.back_color}"
        url_to_img = os.path.join(WEBHOOK_URL, params)
        bot.reply_to(message, f"[{args.data}]({url_to_img})")
    except Exception as e:
        bot.reply_to(message, e.args[1] if len(e.args) > 1 else str(e))
