from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler


TOKEN = '1606352297:AAHcEj_5VsoPt3xsn8Z6wPPzop6gc5wjFio'
# @yandexlyceum2yearbot - БОТ


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")

    return 1


def stop(update, context):
    update.message.reply_text("Вы досрочно завершили опрос!")
    return ConversationHandler.END


def first_response(update, context):
    locality = update.message.text

    update.message.reply_text(
        "Какая погода в городе {locality}?".format(**locals()))
    return 2


def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    weather = update.message.text
    print(weather)
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def first_response_skip(update, context):
    update.message.reply_text("Какая у вас погода за окном?")
    return 2


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],


    states={
        1: [CommandHandler('skip', first_response_skip),
            MessageHandler(Filters.text, first_response),],
        2: [MessageHandler(Filters.text, second_response)],

    },
    fallbacks=[CommandHandler('stop', stop)]
    # Точка прерывания диалога. В данном случае — команда /stop.

)

updater = Updater(TOKEN, use_context=True)


dp = updater.dispatcher

dp.add_handler(conv_handler)

updater.start_polling()

updater.idle()
