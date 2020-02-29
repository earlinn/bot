from glob import glob
from emoji import emojize
import ephem
import logging
from pprint import pprint
from random import choice
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


with open(r'C:\projects\mybot\config.py') as config_file:
    api_key = config_file.readline()


def greet_user(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_data['emo'] = emo
    text = f'Привет {emo}'
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = f'Привет {update.message.chat.first_name} {emo}! Ты написала: {update.message.text}'
    logging.info("User %s, Chat id %s, Message %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
    print(user_text)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def get_user_emo(user_data):
    user_emoji = [
                  ':smiley_cat:', 
                  ':smiling_imp:', 
                  ':panda_face:', 
                  ':dog:'
                  ]
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(user_emoji), use_aliases=True)
        return user_data['emo']


def change_avatar(bot, update, user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text(
                              f'Новый аватар: {emo}', 
                              reply_markup=get_keyboard()
                              )


def planet(bot, update, user_data):
    user_input = update.message.text.split()
    planet, empty_date = user_input[1], 2
    if len(user_input) == empty_date:
        date = ephem.now()
    else:
        date = user_input[2]
    body = getattr(ephem, planet)
    coordinates = body(date)
    constellation = ephem.constellation(coordinates)
    print(constellation)
    update.message.reply_text(constellation, reply_markup=get_keyboard())


def planets(bot, update, user_data):
    all_planets = ephem._libastro.builtin_planets()
    for planet in all_planets:
        print(planet[2])
        update.message.reply_text(planet[2], reply_markup=get_keyboard())


def wordcount(bot, update, user_data):
    user_input = update.message.text.split()
    words_num, final_answer, ending = 0, '', ''
    empty_string = 1
    if len(user_input) == empty_string:
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
    update.message.reply_text(final_answer, reply_markup=get_keyboard())


def next_full_moon(bot, update, user_data):
    user_input = update.message.text.split()
    empty_date = 1
    if len(user_input) == empty_date:
        date = ephem.now()
    else:
        date = user_input[1]
    full_moon = ephem.next_full_moon(date)
    print(full_moon)
    update.message.reply_text(full_moon, reply_markup=get_keyboard())


def cat_send(bot, update, user_data):
    cat_images = glob('cats/cat*.jp*g')
    cat_gifs = glob('cats/gif_cats/cat*.*4')
    cat_pics = cat_images + cat_gifs
    final_pic = choice(cat_pics)
    if final_pic in cat_gifs:
        bot.send_document(
                          chat_id=update.message.chat.id, 
                          document=open(final_pic, 'rb'), 
                          reply_markup=get_keyboard()
                          )
    if final_pic in cat_images:
        bot.send_photo(
                       chat_id=update.message.chat.id, 
                       photo=open(final_pic, 'rb'), 
                       reply_markup=get_keyboard()
                       )


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text(
                              f'Готово {get_user_emo(user_data)}', 
                              reply_markup=get_keyboard()
                              )


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text(
                              f'Готово {get_user_emo(user_data)}', 
                              reply_markup=get_keyboard()
                              )


def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        [
                                           'Список планет', 
                                           '/planet', 
                                           'Котэ'
                                        ],
                                        [
                                           'Полнолуние', 
                                           '/wordcount',
                                           'Сменить аватар'
                                        ],
                                        [
                                            contact_button, 
                                            location_button
                                        ]
                                      ], resize_keyboard=True)
    return my_keyboard


def main():
    mybot = Updater(api_key, request_kwargs=PROXY)

    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))

    dp.add_handler(CommandHandler("planet", planet, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Созвездие)$', planet, pass_user_data=True))

    dp.add_handler(CommandHandler("planets", planets, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Список планет)$', planets, pass_user_data=True))
    
    dp.add_handler(CommandHandler("wordcount", wordcount, pass_user_data=True))
    #dp.add_handler(RegexHandler('^(Слова)$', wordcount, pass_user_data=True))
    
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Полнолуние)$', next_full_moon, pass_user_data=True))
    
    dp.add_handler(CommandHandler("cat", cat_send, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Котэ)$', cat_send, pass_user_data=True))

    dp.add_handler(RegexHandler('^(Сменить аватар)$', change_avatar, pass_user_data=True))
    
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))


    mybot.start_polling()
    mybot.idle()


main()
