import datetime
import json
import logging
import os
import random

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from settings import BOT_KEY

logging.basicConfig(
    format='%(levelname)s %(asctime)s: %(message)s',
    level=logging.INFO,
    filename='bot.log'
)

DEV_CHAT_ID = 309870404
SMILING_IMP = '😈'

JOKES = [
    'Дела идут, контора пишет, а касса деньги выдает',
    'Гуляй, Вася, жуй опилки, я - директор лесопилки',
    '¯\_(ツ)_/¯',
    'дили-дили, трали-вали',
    '',  # sometimes we should be serious
]

EXCLUDE_DATES = {
    '2019-05-01',
    '2019-05-02',
    '2019-05-03',
    '2019-05-04',
    '2019-05-05',

    '2019-05-09',
    '2019-05-10',
    '2019-05-11',
    '2019-05-12',

    '2019-06-12',

    '2019-11-04',

    '2019-12-31',

    '2020-01-01',
    '2020-01-02',
    '2020-01-03',
    '2020-01-04',
    '2020-01-05',
    '2020-01-06',
    '2020-01-07',
    '2020-01-08',

    '2020-02-24',

    '2020-03-09',

    '2020-05-01',
    '2020-05-04',
    '2020-05-05',
    '2020-05-11',

    '2020-06-12',

    '2020-11-04',
}

def log_user(user_obj):
    logging.info('User %s: %s %s', user_obj.id, user_obj.first_name, user_obj.last_name)


def all_clear(update, context):
    update.message.reply_text('Понятно')
    log_user(update.message.from_user)


def shrug(update, context):
    update.message.reply_text('¯\_(ツ)_/¯')


# def mention_all(update, context):
#     print('Вызван /all')
#     print(update.message.from_user.id, update.message.from_user.first_name, update.message.from_user.last_name)
#     log_user(update.message.from_user)
#     update.message.reply_html(MENTION_ALL)


# def mention_it(update, context):
#     log_user(update.message.from_user)
#     update.message.reply_html(MENTION_IT)


# def mention_managers(update, context):
#     log_user(update.message.from_user)
#     update.message.reply_html(MENTION_MANAGERS)


def show_help(update, context):
    log_user(update.message.from_user)
    update.message.reply_text(
        'Доступные команды:\n'
        '/all <text> - отправить уведомление всем\n'
        '/it <text> - отправить уведомление всем айтишникам\n'
        '/mng <text> - отправить уведомление всем менеджерам\n'
        '/shrug - deprecated. use builtin :shrug:\n'
        '/yoj_tebe_ponyatno\n'
        '/tasks - вывод задач Макса\n'
        '/add <text>\n'
        '/push <text> - добавить задачу Максу в конец списка\n'
        '/del <num>\n'
        '/pop <num> - убрать задачу номер num из списка\n'
        '/up <num> - поднять задачу номер num\n'
        '/down <num> - опустить задачу номер num\n'
        '/highest <num> - назначить задаче номер num наивысший приоритет\n'
        '/lowest <num> - назначить задаче номер num низший приоритет\n'
        '/help - этот вывод'
    )


# def timesheet_reminder(context):
#     job = context.bot
#     if datetime.datetime.now().weekday() in (5,6):
#         return
#     if datetime.datetime.now().strftime('%Y-%m-%d') in EXCLUDE_DATES:
#         return
#     context.bot.send_message(
#         chat_id=IQOS_GROUP_CHAT_ID,
#         text='Дамы и господа! Таймшит, будь он неладен!\n{}'.format(MENTION_ALL),
#         parse_mode=ParseMode.HTML
#     )

# TASK LIST
def check_permissions(update):
    allowed_users = ["generous_wind", ]
    # allowed_users = ["rumyantsevr"]
    if update.message.from_user.username not in allowed_users:
        update.message.reply_text('Sorry. No.')
        return False
    return True


def get_task_list():
    with open('task_list.json') as f:
        tasks = json.load(f)
        return tasks


def set_task_list(tasks):
    with open('task_list.json', 'w') as f:
        json.dump(tasks, f)


def task_list(update, context):
    logging.info("Умом Россию не понять...")
    user_obj = update.message.from_user
    print('TASKS INVOKED: User %s: %s %s' % (user_obj.id, user_obj.first_name, user_obj.last_name))
    tasks = get_task_list()
    if tasks:
        msg = '\n'.join(
            '{} {}'.format(c, task)
            for c, task in enumerate(tasks)
        )
    else:
        msg = random.choice(JOKES)
    # update.message.reply_markup('{}'.format(msg))
    if not msg:
        msg = 'The work is done \\(^.^)/'
    context.bot.send_message(
        chat_id=update.message.chat.id,
        # text='```\n{}\n```'.format(msg),
        text=msg,
        # parse_mode=ParseMode.MARKDOWN
    )


def push(update, context):
    has_perm = check_permissions(update)
    if not has_perm:
        return
    if not context.args:
        update.message.reply_text('You should add task info')
    tasks = get_task_list()
    tasks.append(' '.join(context.args))
    set_task_list(tasks)
    # update.message.reply_text('`Added {}`'.format(' '.join(context.args)))
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text='`Added: {} {}`'.format(len(tasks)-1, ' '.join(context.args)),
        parse_mode=ParseMode.MARKDOWN
    )


def pop(update, context):
    has_perm = check_permissions(update)
    if not has_perm:
        return
    tasks = get_task_list()
    if not context.args or not context.args[0].isdigit() or int(context.args[0]) > len(tasks):
        update.message.reply_text('Wrong argument')
        return
    task_num = int(context.args[0])
    removed = tasks.pop(task_num)
    # update.message.reply_text('Marked **{}** as done.'.format(removed))
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text='Marked `{}` as done.'.format(removed),
        parse_mode=ParseMode.MARKDOWN
    )
    set_task_list(tasks)


def task_up(update, context):
    args = context.args
    has_perm = check_permissions(update)
    if not has_perm:
        return
    tasks = get_task_list()
    if not args or not args[0].isdigit() or int(args[0]) > len(tasks) and int(args[0]) == 0:
        update.message.reply_text('Wrong argument')
        return
    task_num = int(args[0])
    moved = tasks.pop(task_num)
    tasks.insert(task_num-1, moved)
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text='Moved `{}` 1 position upper.'.format(moved),
        parse_mode=ParseMode.MARKDOWN
    )
    set_task_list(tasks)


def task_down(update, context):
    args = context.args
    has_perm = check_permissions(update)
    if not has_perm:
        return
    tasks = get_task_list()
    if not args or not args[0].isdigit() or int(args[0]) > len(tasks):
        update.message.reply_text('Wrong argument')
        return
    task_num = int(args[0])
    moved = tasks.pop(task_num)
    tasks.insert(task_num+1, moved)
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text='Moved `{}` 1 position lower.'.format(moved),
        parse_mode=ParseMode.MARKDOWN
    )
    set_task_list(tasks)


def highest(update, context):
    args = context.args
    has_perm = check_permissions(update)
    if not has_perm:
        return
    tasks = get_task_list()
    if not args or not args[0].isdigit() or int(args[0]) > len(tasks):
        update.message.reply_text('Wrong argument')
        return
    task_num = int(args[0])
    moved = tasks.pop(task_num)
    tasks.insert(0, moved)
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text='Moved `{}` to top.'.format(moved),
        parse_mode=ParseMode.MARKDOWN
    )
    set_task_list(tasks)


def lowest(update, context):
    args = context.args
    has_perm = check_permissions(update)
    if not has_perm:
        return
    tasks = get_task_list()
    if not args or not args[0].isdigit() or int(args[0]) > len(tasks):
        update.message.reply_text('Wrong argument')
        return
    task_num = int(args[0])
    moved = tasks.pop(task_num)
    tasks.append(moved)
    context.bot.send_message(
        chat_id=update.message.chat.id,
        text='Moved `{}` to bottom.'.format(moved),
        parse_mode=ParseMode.MARKDOWN
    )
    set_task_list(tasks)


# def greet_newcomers(update, context):
#     if update.message.new_chat_members:
#         log_user(update.message.from_user)
#         usernames = list()
#         user_ids = list()
#         for new_user in update.message.new_chat_members:
#             logging.info(
#                 'User joined id: %s, first_name: %s, last_name: %s, username: %s,',
#                 new_user.id, new_user.first_name, new_user.last_name, new_user.username
#             )
#             if new_user.username:
#                 usernames.append(new_user.username)
#             else:
#                 user_ids.append((new_user.id, new_user.first_name))
#         mention_string = list()
#         mention_string.append(' '.join(['@{}'.format(u) for u in usernames]))
#         for first_name, user_id in user_ids:
#             mention_string.append('<a href="tg://user?id={}">{}</a>'.format(user_id, first_name))

#         update.message.reply_html(
#             '{}\nWELCOME TO HELL {}'.format(' '.join(mention_string), SMILING_IMP)
#         )


# def listen_to_channel(update, context):
#     if update.message.text:
#         print(update.message.text)
#         log_user(update.message.from_user)


def test3(update, context):
    link = update.message.text.split()[-1]
    update.message.reply_html('<a href="{}">{}</a>'.format(link, link))


def main():
    print('RUN')

    if BOT_KEY == '':
        raise ValueError('BOT_KEY is empty. It should be defined in local_settings.py')

    # create task_list.json if needed
    if not os.path.exists('task_list.json'):
        with open('task_list.json', 'w') as f:
            f.write('[]')

    mybot = Updater(BOT_KEY, use_context=True, request_kwargs=PROXY)

    job_queue = mybot.job_queue
    # job_queue.run_repeating(
    #     timesheet_reminder, interval=24*60*60, first=datetime.time(hour=17, minute=30),
    # )

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("test3", test3))

    dp.add_handler(CommandHandler("help", show_help))
    dp.add_handler(CommandHandler("shrug", shrug))
    dp.add_handler(CommandHandler("yoj_tebe_ponyatno", all_clear))
    # dp.add_handler(CommandHandler("all", mention_all))
    # dp.add_handler(CommandHandler("it", mention_it))
    # dp.add_handler(CommandHandler("mng", mention_managers))

    dp.add_handler(CommandHandler("tasks", task_list))
    dp.add_handler(CommandHandler("push", push))
    dp.add_handler(CommandHandler("add", push))
    dp.add_handler(CommandHandler("pop", pop))
    dp.add_handler(CommandHandler("del", pop))
    dp.add_handler(CommandHandler("up", task_up))
    dp.add_handler(CommandHandler("down", task_down))
    dp.add_handler(CommandHandler("highest", highest))
    dp.add_handler(CommandHandler("lowest", lowest))

    # dp.add_handler(MessageHandler(
    #     Filters.status_update.new_chat_members, greet_newcomers
    # ))
    # dp.add_handler(MessageHandler(Filters.text, listen_to_channel))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
