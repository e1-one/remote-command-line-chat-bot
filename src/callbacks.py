from telegram import ParseMode

from src.db import *
from src.oscommand import execute_command_as_subprocess, change_working_dir


def start(update, context):
    index_message = '''
I'm a remote command executor bot, please talk to me!
What I can do:
Type command with parameters to the chat. For example, type: *echo hello* `program _echo_ with parameter _hello_ will be executed on the server, output will be returned to this chat`
/login *username* *password* `authenticates you`
/start `shows this message`
'''
    context.bot.send_message(chat_id=update.message.chat_id, parse_mode=ParseMode.MARKDOWN, text=index_message)


def check_auth(input_func):
    def callback_decorator(update, context):
        if is_authenticated(chat_id=update.message.chat_id):
            input_func(update, context)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='You are not authenticated.')

    return callback_decorator



@check_auth
def text_message(update, context):
    args_without_falsy = [x for x in update.message.text.split(' ') if x]
    if args_without_falsy[0] == 'cd':
        if change_working_dir(args_without_falsy[1]):
            # update_working_directory(user='admin', dir=dir)  # todo: hardcoded
            context.bot.send_message(chat_id=update.message.chat_id, text='Current dir changed')
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text='Invalid directory')
    raw_output = execute_command_as_subprocess(args_without_falsy)
    output = raw_output.replace('\\r\\n', '\n')
    if output:
        context.bot.send_message(chat_id=update.message.chat_id, text=output)


def login(update, context):
    if is_user_exists(user_name=context.args[0], user_pass=context.args[1]):
        bind_chat_to_user(chat_id=update.message.chat_id, user=context.args[0])
        context.bot.send_message(chat_id=update.message.chat_id, text='Authenticated. Access granted.')
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text='Invalid username/password')


def error_callback(update, context):
    logging.error(context.error)
    context.bot.send_message(chat_id=update.message.chat_id, text=f"Ups. Server side error. {context.error} ")
