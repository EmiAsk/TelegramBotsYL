from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from deep_translator import GoogleTranslator
# pip install deep_translator

TOKEN = '1606352297:AAHcEj_5VsoPt3xsn8Z6wPPzop6gc5wjFio'
# @yandexlyceum2yearbot - БОТ


def start(update, context):
    context.user_data['lang'] = ('ru', 'en')
    update.message.reply_text(
        "Привет! Я бот-переводчик. Выбери команду направления языка перевода!"
        " По умолчанию стоит перевод с русского на английский (/ruseng)",
        reply_markup=ReplyKeyboardMarkup([['/engrus', '/ruseng']], one_time_keyboard=True))

    return 1


def stop(update, context):
    update.message.reply_text("Всего доброго!",
                              reply_markup=ReplyKeyboardMarkup([['/start']],
                                                               one_time_keyboard=True))
    return ConversationHandler.END


def switch_to_rus(update, context):
    context.user_data['lang'] = ('en', 'ru')
    update.message.reply_text("Вы сменили язык перевода с английского на русский! Пишите фразу: ")


def switch_to_eng(update, context):
    context.user_data['lang'] = ('ru', 'en')
    update.message.reply_text("Вы сменили язык перевода с русского на английский! Пишите фразу: ")


def translate(update, context):
    src, trg = context.user_data['lang']
    msg = GoogleTranslator(source=src, target=trg).translate(update.message.text)
    update.message.reply_text(msg + '\n\n\n' +
                              "Вы все так же можете выбрать команду "
                              "направления языка перевода на клавиатуре!")


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        1: [CommandHandler('engrus', switch_to_rus), CommandHandler('ruseng', switch_to_eng),
            CommandHandler('stop', stop), MessageHandler(Filters.text, translate)],

    },
    fallbacks=[CommandHandler('stop', stop)]
    # Точка прерывания диалога. В данном случае — команда /stop.

)

updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(conv_handler)

updater.start_polling()

updater.idle()
