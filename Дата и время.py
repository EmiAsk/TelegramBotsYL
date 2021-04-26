from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from datetime import datetime

TOKEN = '1606352297:AAHcEj_5VsoPt3xsn8Z6wPPzop6gc5wjFio'
# @yandexlyceum2yearbot - БОТ


def echo(update, context):
    update.message.reply_text(f'Я получил сообщение {update.message.text}')


def start(update, context):
    update.message.reply_text(
        "Привет! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!")


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def time(update, context):
    now_time = datetime.now().strftime('%H:%M:%S')
    update.message.reply_text(f"Время: {now_time}")


def date(update, context):
    now_time = datetime.now().strftime('%d-%m-%Y')
    update.message.reply_text(f'Дата: {now_time}')


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("date", date))

    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()