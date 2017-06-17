# -*- coding: utf-8 -*-

import logging
import os

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import model

env_key = 'QZBOT_TOKEN'

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def host(bot, update):
    session = model.create_session(update.message.from_user.id)

    if not session:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=
            "You can't host a new game while you are participating in another one.")
        return

    bot.send_message(chat_id=update.message.chat_id, text="You're now hosting a session!")

def finish(bot, update):
    session = model.get_hosted_session(update.message.from_user.id)

    if session:
        if session.delete_instance():
            bot.send_message(
            chat_id=update.message.chat_id,
            text=
            "You are no longer hosting any sessions.")
    else:
        bot.send_message(
        chat_id=update.message.chat_id,
        text=
        "You are not hosting any sessions, nothing to finish.")

def main(token):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('host', host))
    dispatcher.add_handler(CommandHandler('finish', finish))

    updater.start_polling()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    model.create_tables()

    if env_key in os.environ:
        main(os.environ[env_key])
    else:
        print(f"The '{env_key}' environment variable doesn't exist.")
