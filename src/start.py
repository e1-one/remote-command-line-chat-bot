import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def read_config_file():
    with open('config.json', 'r') as f:
        import json
        return json.load(f)


def configure_db(config_file):
    from src.db import set_db, create_user_tables, add_user

    set_db(config_file['sqlite_db_path'])
    create_user_tables()
    add_user(user=config_file['username'], password=config_file['password'])


def configure_and_start_telegram_dispatcher(config_file):
    from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
    from src.callbacks import login, start, text_message, error_callback

    updater = Updater(token=config_file['token'], use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('login', login))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message))
    dispatcher.add_error_handler(error_callback)
    logging.info('Starting updates polling')
    updater.start_polling()


def start_app():
    config = read_config_file()

    configure_db(config)
    configure_and_start_telegram_dispatcher(config)


if __name__ == '__main__':
    start_app()
