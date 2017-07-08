# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, TypeHandler
import constants
import logging
import weather

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    greetings = "Hello, {user}! At this time, \n" \
                "bot can send you weather in any city \n" \
                "at this moment and for few days(1-16).\n" \
                "For current weather send \n/weather 'CITY_NAME'\n" \
                "For weather for few days send \n/weather 'CITY_NAME' 'NUM_OF_DAYS'"

    bot.send_message(chat_id=update.message.chat_id,
                     text=greetings.format(user=update.message.from_user.first_name))


def send_weather(bot, update, args):
    if len(args) == 1:
        bot.send_message(chat_id=update.message.chat_id, text=weather.get_weather(args[0]))
    elif len(args) == 2:
        bot.send_message(chat_id=update.message.chat_id, text=weather.get_weather_daily(args[0], args[1]))
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Use correct parameters')

def unknown_message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='I can`t recognize messages yet :(')

def unknown_command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Unknown command')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(token=constants.token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('weather', send_weather, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))
    dispatcher.add_handler(MessageHandler(Filters.text, unknown_message))
    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

