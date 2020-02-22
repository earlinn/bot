from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

import logging
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

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
    text = 'Вызван /planet'
    print(text)
    update.message.reply_text(text)
    user_text = ephem.Mars('2019/03/03')
    print(ephem.constellation(user_text))
    update.message.reply_text(user_text)


def planet_handler(bot, update):
    user_text = update.message.text
 #   planet = user_text.split()
 #   planet = planet[1]
    user_text = ephem.Mars('2019/03/03')
    print(ephem.constellation(user_text))
    update.message.reply_text(user_text)


def main():
    mybot = Updater(api_key, request_kwargs=PROXY)

    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", planet))
 #   dp.add_handler(MessageHandler(Filters.text, planet_handler))
 #   print(Filters.text) 

    mybot.start_polling()
    mybot.idle()


main()
