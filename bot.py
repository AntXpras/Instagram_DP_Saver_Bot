import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, commandhandler
import os
from instaloader import Instaloader, Profile
import time


'''Coded by Anish Gowda'''
'''Edited By @Xpras_id'''

L = Instaloader()
TOKEN = os.getenv("BOT_TOKEN")
APP_NAME = os.getenv("APP_NAME")
TELEGRAM_USERNAME = os.getenv("TELEGRAM_USERNAME")

welcome_msg = '''<b>S░░E░░L░░A░░M░░A░░T░░D░░A░░T░░A░░N░░G</b>🖐🖐
 
 <i>Kirimkan Saya Nama Pengguna instagram (username) setelah itu saya akan menunjuka profil pengguna tersebut</i>

contoh : <b>fuck.you</b> , <b>fuckyou</b> etc'''

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def acc_type(val):
    if(val):
        return "ⓟⓡⓘⓥⓐⓣⓔ"
    else:
        return "ⓟⓤⓑⓛⓘⓚ"

# Start the Bot


def start(update, context):
    id = update.message.chat_id
    name = update.message.from_user['username']
    update.message.reply_html(welcome_msg)


def help_msg(update, context):
    update.message.reply_text("Tidak ada Bantuan atau /help Karna cara menggunakan bot ini sangatlah mudah dan simpel")


def contact(update, context):
    keyboard = [[InlineKeyboardButton(
        "Contact Me", url=f"telegram.me/{TELEGRAM_USERNAME}")], ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Contact The Maker:', reply_markup=reply_markup)

# get the username and send the DP


def username(update, context):
    msg = update.message.reply_text("Download Info Profile...")
    query = update.message.text
    chat_id = update.message.chat_id
    try:
        user = Profile.from_username(L.context, query)
        caption_msg = f'''*Nama*: {user.full_name} \n*Followers*: {user.followers} \n🤩*Following*🤩: {user.followees}\
         \n🧐*Account Type*🧐: {acc_type(user.is_private)} \n\nTerimakasih telah menggunakan Bot ini Dont Forget To Join @cyntaxrobot'''
        context.bot.send_photo(
            chat_id=chat_id, photo=user.profile_pic_url,
            caption=caption_msg, parse_mode='MARKDOWN')
        msg.edit_text("Selesai.")
        time.sleep(5)
    except Exception:
        msg.edit_text("Coba lagi -- Cek username Benar atau Salah --")



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_msg))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(MessageHandler(Filters.text, username))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN,
                          webhook_url=f"https://{APP_NAME}.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
