#!/usr/bin/python3

import datetime
import pymysql
import telebot
from telebot.types import Message
from bot.EconomKino import logger, const, markups, token, functions

db = pymysql.connect(host="eu-cdbr-west-02.cleardb.net",
                     user="bdb28d30c292d7",
                     password="4ad2b3a3",
                     db="heroku_982b4fce6d3c135")
cursor = db.cursor()

sql_insert_new_user = "INSERT INTO heroku_982b4fce6d3c135.users(user_id, chosen_date) " \
                                  "VALUES(%s, %s);"


bot = telebot.TeleBot(token.TOKEN)
print("It's working...")


@bot.message_handler(commands=['start'])
def message_handler(message: Message):
    bot.send_message(message.from_user.id,
                     text=('Привіт!\nЯ Економ Кіно Бот ' + const.POPCORN_EMOJI),
                     reply_markup=markups.main_menu)
    logger.log_message(message)


# Ярік лишив, як ти просив | XD
@bot.message_handler(commands=['help'])
def message_handler(message: Message):
    bot.send_message(message.from_user.id, const.INFO, reply_markup=markups.main_menu)
    logger.log_message(message)


# ------------------------------------------------------------- #
#                  Processing Reply Keyboard                    #
# ------------------------------------------------------------- #
@bot.message_handler(content_types='text')
def back(message: Message):
    if message.text == const.LEFTWARDS_ARROW_EMOJI + ' Назад':
        bot.send_message(message.from_user.id, '...', reply_markup=markups.main_menu)

    # Main menu
    elif message.text == const.CINEMA_EMOJI + ' Старт':
        bot.send_message(message.from_user.id, 'Виберіть день:', reply_markup=markups.dates)
    elif message.text == const.LOCATION_EMOJI + ' Локації':
        bot.send_message(message.from_user.id, 'Виберіть кінотеатр:', reply_markup=markups.cinemas)
    elif message.text == const.INFO_EMOJI + ' Інфо':
        bot.send_message(message.from_user.id, const.INFO, reply_markup=markups.back)

    # Cinemas location
    elif message.text == 'Multiplex: Victoria Gardens':
        bot.send_message(message.from_user.id, 'Шукаю Локацію ' + const.SEARCH_EMOJI)
        bot.send_location(message.from_user.id, 49.807352, 23.977764)
    elif message.text == 'Планета Кіно: Forum':
        bot.send_message(message.from_user.id, 'Шукаю Локацію ' + const.SEARCH_EMOJI)
        bot.send_location(message.from_user.id, 49.849907, 24.022289)
    elif message.text == 'Планета Кіно: King Cross':
        bot.send_message(message.from_user.id, 'Шукаю Локацію ' + const.SEARCH_EMOJI)
        bot.send_location(message.from_user.id, 49.7738874, 24.0087695)
    elif message.text == 'Multiplex: Spartak':
        bot.send_message(message.from_user.id, 'Шукаю Локацію ' + const.SEARCH_EMOJI)
        bot.send_location(message.from_user.id, 49.869772, 24.0223554)
    logger.log_message(message)


# ------------------------------------------------------------- #
#                 Processing Inline Keyboard                    #
# ------------------------------------------------------------- #
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # -------------------------- Dates -------------------------- #
    if call.data == datetime.datetime.strftime(markups.today, '%Y-%m-%d'):
        sql_get_date = "SELECT * FROM heroku_982b4fce6d3c135.users WHERE user_id = %s;" % call.from_user.id
        cursor.execute(sql_get_date)
        results = cursor.fetchall()

        if len(results) == 0:
            global sql_insert_new_user
            cursor.execute(sql_insert_new_user, (call.from_user.id, call.data))
            db.commit()
        else:
            sql_update_date = "UPDATE heroku_982b4fce6d3c135.users SET chosen_date = '%s' " \
                              "WHERE user_id = %s;" % (call.data, call.from_user.id)
            cursor.execute(sql_update_date)
            db.commit()

        bot.edit_message_text(
            text="Фільми, які будуть в прокаті у цей день: ",
            chat_id=call.from_user.id,
            message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_films)

    elif call.data == datetime.datetime.strftime(markups.today_plus_one, '%Y-%m-%d'):
        sql_get_date = "SELECT * FROM heroku_982b4fce6d3c135.users WHERE user_id = %s;" % call.from_user.id
        cursor.execute(sql_get_date)
        results = cursor.fetchall()

        if len(results) == 0:
            cursor.execute(sql_insert_new_user, (call.from_user.id, call.data))
            db.commit()
        else:
            sql_update_date = "UPDATE heroku_982b4fce6d3c135.users SET chosen_date = '%s' " \
                              "WHERE user_id = %s;" % (call.data, call.from_user.id)
            cursor.execute(sql_update_date)
            db.commit()

        bot.edit_message_text(
            text="Фільми, які будуть в прокаті у цей день:",
            chat_id=call.from_user.id,
            message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_one_films)

    elif call.data == datetime.datetime.strftime(markups.today_plus_two, '%Y-%m-%d'):
        sql_get_date = "SELECT * FROM heroku_982b4fce6d3c135.users WHERE user_id = %s;" % call.from_user.id
        cursor.execute(sql_get_date)
        results = cursor.fetchall()

        if len(results) == 0:
            sql_insert_new_user = "INSERT INTO heroku_982b4fce6d3c135.users(user_id, chosen_date) " \
                                  "VALUES(%s, %s);"
            cursor.execute(sql_insert_new_user, (call.from_user.id, call.data))
            db.commit()
        else:
            sql_update_date = "UPDATE heroku_982b4fce6d3c135.users SET chosen_date = '%s' " \
                              "WHERE user_id = %s;" % (call.data, call.from_user.id)
            cursor.execute(sql_update_date)
            db.commit()

        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_two_films)

    elif call.data == datetime.datetime.strftime(markups.today_plus_three, '%Y-%m-%d'):
        sql_get_date = "SELECT * FROM heroku_982b4fce6d3c135.users WHERE user_id = %s;" % call.from_user.id
        cursor.execute(sql_get_date)
        results = cursor.fetchall()

        if len(results) == 0:
            sql_insert_new_user = "INSERT INTO heroku_982b4fce6d3c135.users(user_id, chosen_date) " \
                                  "VALUES(%s, %s);"
            cursor.execute(sql_insert_new_user, (call.from_user.id, call.data))
            db.commit()
        else:
            sql_update_date = "UPDATE heroku_982b4fce6d3c135.users SET chosen_date = '%s' " \
                              "WHERE user_id = %s;" % (call.data, call.from_user.id)
            cursor.execute(sql_update_date)
            db.commit()

        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_three_films)

    elif call.data == datetime.datetime.strftime(markups.today_plus_four, '%Y-%m-%d'):
        sql_get_date = "SELECT * FROM heroku_982b4fce6d3c135.users WHERE user_id = %s;" % call.from_user.id
        cursor.execute(sql_get_date)
        results = cursor.fetchall()

        if len(results) == 0:
            sql_insert_new_user = "INSERT INTO heroku_982b4fce6d3c135.users(user_id, chosen_date) " \
                                  "VALUES(%s, %s);"
            cursor.execute(sql_insert_new_user, (call.from_user.id, call.data))
            db.commit()
        else:
            sql_update_date = "UPDATE heroku_982b4fce6d3c135.users SET chosen_date = '%s' " \
                              "WHERE user_id = %s;" % (call.data, call.from_user.id)
            cursor.execute(sql_update_date)
            db.commit()

        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_four_films)

    elif call.data == datetime.datetime.strftime(markups.today_plus_five, '%Y-%m-%d'):
        sql_get_date = "SELECT * FROM heroku_982b4fce6d3c135.users WHERE user_id = %s;" % call.from_user.id
        cursor.execute(sql_get_date)
        results = cursor.fetchall()

        if len(results) == 0:
            sql_insert_new_user = "INSERT INTO heroku_982b4fce6d3c135.users(user_id, chosen_date) " \
                                  "VALUES(%s, %s);"
            cursor.execute(sql_insert_new_user, (call.from_user.id, call.data))
            db.commit()
        else:
            sql_update_date = "UPDATE heroku_982b4fce6d3c135.users SET chosen_date = '%s' " \
                              "WHERE user_id = %s;" % (call.data, call.from_user.id)
            cursor.execute(sql_update_date)
            db.commit()

        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_five_films)

    # -------------------------- Sessions -------------------------- #
    elif call.data in markups.callback_data_list:
        sql_get_user = "SELECT * FROM heroku_982b4fce6d3c135.users WHERE user_id = %s;" % call.from_user.id
        cursor.execute(sql_get_user)
        results = cursor.fetchall()

        film_index = (markups.callback_data_list.index(call.data))
        film_name = markups.film_names_list[film_index]
        chosen_date = str(results[0][1])
        available_sessions = str()

        # available_sessions += 14 * const.popcorn + '\n'
        available_sessions += '\n' + const.FILM_PROJECTOR_EMOJI + ' \"' + film_name + '\"\n'
        available_sessions += const.CALENDAR_EMOJI + ' ' + chosen_date[8:10] + \
                              '.' + chosen_date[5:7] + '.' + \
                              chosen_date[0:4] + '\n'
        available_sessions += '\n' + 13 * const.POPCORN_EMOJI + '\n'

        sql_get_date = "SELECT * FROM heroku_982b4fce6d3c135.economkino " \
                       "where date = '%s' AND film = '%s' order by price;" % (chosen_date, film_name)

        cursor.execute(sql_get_date)
        results = cursor.fetchall()
        session_number = 1
        for row in results:
            price = row[4]
            time = str(row[5])
            technology = row[6]
            cinema = row[1]
            tickets = row[7]
            if session_number != 1:
                # available_sessions += '\n' + 13 * const.fires + '\n'
                available_sessions += '~~~~~~~~~~~~~~~~~~~~~~~'
            available_sessions += '\nСеанс ' + const.DIGIT_KEYCAPS_EMOJI[session_number]
            available_sessions += '\nКінотеатр: %s ' \
                                  '\nТехгологія: %s' \
                                  '\nПочаток: %s' \
                                  '\nЦіна: %s грн.' \
                                  '\n<a href="%s">Купити квиток</a>\n' % (const.CINEMAS_LIST[cinema],
                                                                              technology, time[0:5],
                                                                              price, tickets)

            session_number += 1

        bot.edit_message_text(text=available_sessions,
                              parse_mode='HTML',
                              disable_web_page_preview=True,
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        if datetime.datetime.strftime(markups.today, '%Y-%m-%d') == chosen_date:
            bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markups.today_sessions)

        elif datetime.datetime.strftime(markups.today_plus_one, '%Y-%m-%d') == chosen_date:
            bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markups.today_plus_one_sessions)

        elif datetime.datetime.strftime(markups.today_plus_two, '%Y-%m-%d') == chosen_date:
            bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markups.today_plus_two_sessions)

        elif datetime.datetime.strftime(markups.today_plus_three, '%Y-%m-%d') == chosen_date:
            bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markups.today_plus_three_sessions)

        elif datetime.datetime.strftime(markups.today_plus_four, '%Y-%m-%d') == chosen_date:
            bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markups.today_plus_four_sessions)

        elif datetime.datetime.strftime(markups.today_plus_five, '%Y-%m-%d') == chosen_date:
            bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                          message_id=call.message.message_id,
                                          reply_markup=markups.today_plus_five_sessions)

    # ----------------------- Sessions back ---------------------- #
    elif call.data == "today_sessions_back":
        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_films)

    elif call.data == "today_plus_one_sessions_back":
        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_one_films)

    elif call.data == "today_plus_two_sessions_back":
        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_two_films)

    elif call.data == "today_plus_three_sessions_back":
        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_three_films)

    elif call.data == "today_plus_four_sessions_back":
        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_four_films)

    elif call.data == "today_plus_five_sessions_back":
        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_five_films)

    # --------------------------- Else --------------------------- #
    elif call.data == "show_mode_back":
        bot.edit_message_text(text="Фільми, які будуть в прокаті у цей день:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.today_plus_one_films)

    elif call.data == "films_back":
        bot.edit_message_text(text="Виберіть бажану дату:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.dates)

    elif call.data == "dates_refresh":
        bot.edit_message_text(text="Виберіть бажану дату:",
                              chat_id=call.from_user.id,
                              message_id=call.message.message_id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                      message_id=call.message.message_id,
                                      reply_markup=markups.dates)
    logger.log_call(call)


bot.polling(timeout=60)
