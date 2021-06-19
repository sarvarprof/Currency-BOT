from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, Dispatcher, Filters, CallbackContext, \
    CommandHandler, MessageHandler, CallbackQueryHandler
import local_settings
import requests
from telegram.ext.filters import Filters
updater = Updater(token=local_settings.TELEGRAM_TOKEN)
from mwt import MWT


def start(update: Update, context: CallbackContext):
    update.message.reply_text('Salom!',reply_markup=ReplyKeyboardMarkup( keyboard=[[KeyboardButton(text='/currency')]],resize_keyboard=True))

@MWT(timeout=60*60)
def get_currency():
    response = requests.get('https://nbu.uz/uz/exchange-rates/json/')
    results = response.json()

    if len(results):
        print('Currency data obtained')
        return results
    else:
        return None
def currency(update: Update, context: CallbackContext):
    keyboard = generate_list()
    update.message.reply_text(
        'Valyutani tanla:',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )
def generate_list():
    results = get_currency()
    print(results)
    keyboard = []
    for i in range(6):
        currency_key = []
        for j in range(4):
            n = i * 4 + j
            cur = results[n]['code']
            currency_key.append(InlineKeyboardButton(f"{cur}", callback_data=cur))
        keyboard.append(currency_key)
    return keyboard

def callback_handler(update: Update, context: CallbackContext):
    keyboard = generate_list()
    data = update.callback_query.data
    results = get_currency()
    if len(results):
        for i in range(len(results)):
            if data == results[i]['code']:
                update.callback_query.message.edit_text(f"1 {results[i]['code']}  {results[i]['cb_price']} som \n"
                                                              f"Yangilangan vaqti: {results[i]['date']}\n\n"
                                                              'Valyutani tanla:',
                    reply_markup = InlineKeyboardMarkup(inline_keyboard=keyboard))



dispatcher: Dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('Start', start))
#dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(CommandHandler('currency', currency))
dispatcher.add_handler(MessageHandler(Filters.all, start))
dispatcher.add_handler(CallbackQueryHandler(callback_handler))

updater.start_polling()
updater.idle()
