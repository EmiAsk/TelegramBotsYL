from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup


TOKEN = '1606352297:AAHcEj_5VsoPt3xsn8Z6wPPzop6gc5wjFio'
# @yandexlyceum2yearbot - БОТ


POEM = 'наша таня\nгромко плачет\nуронила в\nречку мячик'.split('\n')


def poem(update, context):
    n = context.user_data.get('line', 0)
    if n == 0:
        update.message.reply_text(POEM[n])
        context.user_data['line'] = 1

    elif update.message.text.lower() == POEM[n].lower():
        if n in (len(POEM) - 1, len(POEM) - 2):
            if n == (len(POEM) - 2):
                update.message.reply_text(POEM[n + 1])
            update.message.reply_text('Поздравляю! Вы выиграли!')
            del context.user_data['line']
            return ConversationHandler.END

        update.message.reply_text(POEM[n + 1])
        context.user_data['line'] += 2

    else:
        update.message.reply_text('нет, не так',
                                  reply_markup=ReplyKeyboardMarkup([['/suphler']],
                                                                   one_time_keyboard=True))
    return 1


def hint(update, context):
    msg = POEM[context.user_data['line']]
    update.message.reply_text(f'Подсказка (первая половина строчки стиха): '
                              f'{msg[:len(msg) // 2]}')


def stop(update, context):
    del context.user_data['line']

    update.message.reply_text("Всего доброго!",
                              reply_markup=ReplyKeyboardMarkup([['/start']],
                                                               one_time_keyboard=True))
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', poem)],


    states={
        1: [CommandHandler('suphler', hint), CommandHandler('stop', stop, pass_user_data=True),
            MessageHandler(Filters.text, poem, pass_user_data=True)]

    },
    fallbacks=[CommandHandler('stop', stop, pass_user_data=True)]
    # Точка прерывания диалога. В данном случае — команда /stop.

)

updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(conv_handler)

updater.start_polling()

updater.idle()
