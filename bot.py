from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

import ephem
from pprint import pprint

with open(r'C:\projects\mybot\config.py') as config_file:
    api_key = config_file.readline()


def greet_user(bot, update):
    text = 'Вызван /start'
    print(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)


def planet(bot, update):
    user_input = update.message.text.split()
    planet = user_input[1]
    if len(user_input) == 2:
        date = ephem.now()
    else:
        date = user_input[2]
#    user_text = getattr(ephem, planet)(date)
    user_text = ephem.planet(date)
    constellation = ephem.constellation(user_text)
    print(constellation)
    update.message.reply_text(constellation)


def planets(bot, update):
    all_planets = ephem._libastro.builtin_planets()
    for planet in all_planets:
        print(planet[2])
        update.message.reply_text(planet[2])


def main():
    mybot = Updater(api_key, request_kwargs=PROXY)

    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(CommandHandler("planets", planets))
 

    mybot.start_polling()
    mybot.idle()


main()
