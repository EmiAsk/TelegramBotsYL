from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardRemove


TOKEN = '1606352297:AAHcEj_5VsoPt3xsn8Z6wPPzop6gc5wjFio'
# @yandexlyceum2yearbot - БОТ


def task(context):
    """Выводит сообщение"""
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


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
def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        # args[0] должен содержать значение аргумента
        # (секунды таймера)
        due = int(context.args[0])
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
        text = f'Вернусь через {due} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        # Присылаем сообщение о том, что всё получилось.
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set <секунд>')


def unset_timer(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Хорошо, вернулся сейчас!' if job_removed else 'Нет активного таймера.'
    update.message.reply_text(text)


def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("set_timer", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer,
                                  pass_chat_data=True)
                   )

    updater.start_polling()

    updater.idle()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()