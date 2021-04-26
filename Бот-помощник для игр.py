from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, CommandHandler
from random import randint


TOKEN = '1606352297:AAHcEj_5VsoPt3xsn8Z6wPPzop6gc5wjFio'
# @yandexlyceum2yearbot - БОТ


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text=f'Время истекло!', reply_markup=ReplyKeyboardRemove())


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


# Обычный обработчик, как и те, которыми мы пользовались раньше.
def set_timer(update, context, time, text):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = time
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое')
            return

        # Добавляем задачу в очередь
        # и останавливаем предыдущую (если она была)
        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            due,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Засёк {text}'
        if job_removed:
            text += ' Старая задача удалена.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text, reply_markup=unset_kb)

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер сброшен!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text, reply_markup=ReplyKeyboardMarkup([['/start']]))


def start(update, context):
    update.message.reply_text(
        "Выберите команду", reply_markup=markup)


def help(update, context):
    update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо.")


def get_message(update, context):
    msg = update.message.text
    if msg == 'вернуться назад':
        start(update, context)
    elif msg in DICES:
        answer = DICES[msg]()
        update.message.reply_text(','.join(answer))
        get_dices(update, context)
    elif msg in TIMES:
        answer = TIMES[msg]
        set_timer(update, context, answer, msg)
    else:
        update.message.reply_text('Я вас не понимаю')


def get_dices(update, context):
    update.message.reply_text(
        "Выбирайте", reply_markup=dice_kb)


def get_times(update, context):
    update.message.reply_text(
        "Выбирайте", reply_markup=times_kb)


DICES = {'кинуть один шестигранный кубик': lambda: (str(randint(1, 7)), ),
         'кинуть 2 шестигранных кубика одновременно': lambda: (str(randint(1, 7)),
                                                               str(randint(1, 7))),
         'кинуть 20-гранный кубик': lambda: (str(randint(1, 21)), )}

TIMES = {'30 секунд': 30, '1 минута': 60, '5 минут': 300}


updater = Updater(TOKEN, use_context=True)

# Получаем из него диспетчер сообщений.
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("dice", get_dices))
dp.add_handler(CommandHandler("timer", get_times))
dp.add_handler(CommandHandler("close", unset_timer))
dp.add_handler(MessageHandler(Filters.text, get_message))

reply_keyboard = [['/dice', '/timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

dices = [[d] for d in DICES.keys()] + [['вернуться назад']]
dice_kb = ReplyKeyboardMarkup(dices, one_time_keyboard=False)

times = [[t] for t in TIMES.keys()] + [['вернуться назад']]
times_kb = ReplyKeyboardMarkup(times, one_time_keyboard=True)

reply_keyboard = [['/close']]
unset_kb = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

updater.start_polling()

updater.idle()

