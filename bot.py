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
    body = getattr(ephem, planet)
    coordinates = body(date)
    constellation = ephem.constellation(coordinates)
    print(constellation)
    update.message.reply_text(constellation)


def planets(bot, update):
    all_planets = ephem._libastro.builtin_planets()
    for planet in all_planets:
        print(planet[2])
        update.message.reply_text(planet[2])


def wordcount(bot, update):
    user_input = update.message.text.split()
    words_num, final_answer, ending = 0, '', ''
    if len(user_input) - 1 == 0:
        final_answer = 'Пустая строка'
    else:
        for word in range(1, len(user_input)):
            it_is_a_word = 0
            for character in user_input[word]:
                if character.isalpha():
                    it_is_a_word += 1
            if it_is_a_word:
                if not user_input[word].isdigit():
                    words_num += 1
        if words_num == 0:
            final_answer = 'Не введено ни одного слова'
        else:
            answer = words_num
            if answer % 10 == 1 and answer % 100 != 11:
                ending = 'слово'
            elif answer % 10 in [2, 3, 4] and answer % 100 not in [12, 13, 14]:
                ending = 'слова'
            else:
                ending = 'слов'
            final_answer = f'{answer} {ending}'
    print(final_answer)
    update.message.reply_text(final_answer)


def next_full_moon(bot, update):
    user_input = update.message.text.split()
    if len(user_input) == 1:
        date = ephem.now()
    else:
        date = user_input[1]
    full_moon = ephem.next_full_moon(date)
    print(full_moon)
    update.message.reply_text(full_moon)


def main():
    mybot = Updater(api_key, request_kwargs=PROXY)

    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(CommandHandler("planet", planet))
    dp.add_handler(CommandHandler("planets", planets))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))


    mybot.start_polling()
    mybot.idle()


main()
