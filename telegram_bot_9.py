from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import requests

reply_keyboard = [['/ru_en', '/en_ru', '/ru_tr', '/tr_ru']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

TRANS_DIRECTION_KEY = "trans-direction"


def start(update, context):
    update.message.reply_text("Я бот-переводчик. Перевожу слова.", reply_markup=markup)


def translater(updater, context):
    accompanying_text = "Переведено сервисом «Яндекс.Переводчик» http://translate.yandex.ru/."
    translator_uri = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    response = requests.get(translator_uri, params={
        "key": "trnsl.1.1.20170206T114843Z.150706f980933244.3131bc737246d8afe33e325ad0d875ed2d646f8b",
        "lang": context.user_data.get(TRANS_DIRECTION_KEY, "ru-en"),
        "text": updater.message.text
    })
    updater.message.reply_text("\n\n".join([response.json()["text"][0], accompanying_text]))


def ru_en(update, context):
    context.user_data[TRANS_DIRECTION_KEY] = "ru-en"
    update.message.reply_text("Используем направление перевода: " + context.user_data[TRANS_DIRECTION_KEY])


def en_ru(update, context):
    context.user_data[TRANS_DIRECTION_KEY] = "en-ru"
    update.message.reply_text("Используем направление перевода: " + context.user_data[TRANS_DIRECTION_KEY])


def ru_tr(update, context):
    context.user_data[TRANS_DIRECTION_KEY] = "ru-tr"
    update.message.reply_text("Используем направление перевода: " + context.user_data[TRANS_DIRECTION_KEY])


def tr_ru(update, context):
    context.user_data[TRANS_DIRECTION_KEY] = "tr-ru"
    update.message.reply_text("Используем направление перевода: " + context.user_data[TRANS_DIRECTION_KEY])


def main():
    updater = Updater("YOUR_TOKEN", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ru_en", ru_en, pass_user_data=True))
    dp.add_handler(CommandHandler("en_ru", en_ru, pass_user_data=True))
    dp.add_handler(CommandHandler("ru_tr", ru_tr, pass_user_data=True))
    dp.add_handler(CommandHandler("tr_ru", tr_ru, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, translater, pass_user_data=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
