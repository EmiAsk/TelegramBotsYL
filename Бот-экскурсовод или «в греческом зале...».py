from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup


TOKEN = '1606352297:AAHcEj_5VsoPt3xsn8Z6wPPzop6gc5wjFio'
# @yandexlyceum2yearbot - БОТ


def first_hall(update, context):
    kb = kbs['1']
    update.message.reply_text(
        "Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб! Сейчас вы в 1 зале,"
        "где стоят экспонаты мумии! Выберите номер зала, в который вы хотите пройти!",
        reply_markup=kb)

    return 1


def stop(update, context):
    update.message.reply_text("Всего доброго, не забудьте забрать верхнюю одежду в гардеробе",
                              reply_markup=ReplyKeyboardMarkup([['/start']]))
    return ConversationHandler.END


def second_hall(update, context):
    kb = kbs['2']
    update.message.reply_text(
        "Сейчас вы во 2 зале,"
        "где стоят экспонаты кроманьонцев! Выберите номер зала, в который вы хотите пройти!",
        reply_markup=kb)

    return 2


def third_hall(update, context):
    kb = kbs['3']
    update.message.reply_text(
        "Сейчас вы в 3 зале,"
        "где стоят экспонаты динозавров! Выберите номер зала, в который вы хотите пройти!",
        reply_markup=kb)

    return 3


def fourth_hall(update, context):
    kb = kbs['4']
    update.message.reply_text(
        "Сейчас вы в 4 зале,"
        "где стоят экспонаты неандертальцев! Выберите номер зала, в который вы хотите пройти!",
        reply_markup=kb)

    return 4


def first_hall_again(update, context):
    kb = kbs['1']
    update.message.reply_text(
        "Сейчас вы в 1 зале,"
        "где стоят экспонаты мумии! Выберите номер зала, в который вы хотите пройти!",
        reply_markup=kb)

    return 1


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', first_hall)],


    states={
        1: [CommandHandler('2', second_hall)],
        2: [CommandHandler('3', third_hall)],
        3: [CommandHandler('4', fourth_hall), CommandHandler('1', first_hall_again)],
        4: [CommandHandler('1', first_hall_again)]

    },
    fallbacks=[CommandHandler('stop', stop)]
    # Точка прерывания диалога. В данном случае — команда /stop.

)

updater = Updater(TOKEN, use_context=True)

kbs = {'1': ReplyKeyboardMarkup([['/2'], ['/stop']]),
       '2': ReplyKeyboardMarkup([['/3'], ['/stop']]),
       '3': ReplyKeyboardMarkup([['/4'], ['/1'], ['/stop']]),
       '4': ReplyKeyboardMarkup([['/1'], ['/stop']])}
dp = updater.dispatcher

dp.add_handler(conv_handler)

updater.start_polling()

updater.idle()
