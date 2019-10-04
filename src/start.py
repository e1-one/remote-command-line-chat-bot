import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def read_config_file():
    with open('config.json', 'r') as f:
        import json
        return json.load(f)


def start():
    config = read_config_file()

    from src.db.userdb import set_db, create_user_tables

    config_db_file = config['sqlite_db_path'];
    if config_db_file:
        logging.info(f'DB module initialization. dbFile path is: {config_db_file}')
        set_db(config_db_file)
    else:
        logging.info(f'DB module initialization with default dbFile path')
    create_user_tables()

    from telegram.ext import CommandHandler, Updater
    from src.callbacks import run, cd, login, start, error_callback

    updater = Updater(token=config['token'], use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('run', run))
    dispatcher.add_handler(CommandHandler('cd', cd))
    dispatcher.add_handler(CommandHandler('login', login))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_error_handler(error_callback)
    logging.info('Starting updates polling')
    updater.start_polling()


if __name__ == '__main__':
    start()
