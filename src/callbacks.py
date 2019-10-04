from telegram import ParseMode
from src.db.userdb import *
from src.oscommand import execute_command, check_dir


def start(update, context):
    index_message = '''
I'm a remote command executor bot, please talk to me!
What I can do:
/login *username* *password* `authenticates you`
/run *command* (params) `runs the command and returns output`
/cd *dir* `changes current working directory`
'''
    context.bot.send_message(chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN, text=index_message)


def check_auth(input_func):
    def callback_decorator(update, context):
        if is_authenticated(update.message.chat_id):
            input_func(update, context)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='You are not authenticated.')
    return callback_decorator


@check_auth
def cd(update, context):
    dir = context.args[0]
    if check_dir(dir):
        update_working_directory('admin', dir)  # todo: hardcoded
        context.bot.send_message(chat_id=update.message.chat_id, text='Current dir changed')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='Invalid directory')


@check_auth
def run(update, context):
    raw_output = execute_command(context.args)
    output = raw_output.replace('\\r\\n', '\n')
    if output:
        context.bot.send_message(chat_id=update.message.chat_id, text=output)


def login(update, context):
    if is_user_exists(context.args[0], context.args[1]):
        bind_chat_to_user(update.message.chat_id, context.args[0])
        context.bot.send_message(chat_id=update.message.chat_id, text='Authenticated. Access granted.')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='Invalid username/password')


def error_callback(update, context):
    logging.error(context.error)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"Ups. Server side error. {context.error} ")
