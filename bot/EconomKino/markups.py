import pymysql as pymysql
import datetime as timedate
import telebot

from datetime import datetime
from telebot import types

from bot.EconomKino.functions import day_of_week
from bot.EconomKino.functions import to_callback_data
from bot.EconomKino import const


# Connect to Data Base
db = pymysql.connect(host="eu-cdbr-west-02.cleardb.net",
                     user="bdb28d30c292d7",
                     password="4ad2b3a3",
                     db="heroku_982b4fce6d3c135")
cursor = db.cursor()


# Main menu markup
main_menu = types.ReplyKeyboardMarkup(True, False)
main_menu.row(const.CINEMA_EMOJI + ' Старт', const.LOCATION_EMOJI + ' Локації', const.INFO_EMOJI + ' Інфо')


# Cinemas locations list
cinemas = types.ReplyKeyboardMarkup(True, False)
cinemas.row('Планета Кіно: Forum', 'Multiplex: Spartak')
cinemas.row('Планета Кіно: King Cross', 'Multiplex: Victoria Gardens')
cinemas.row(const.LEFTWARDS_ARROW_EMOJI + ' Назад')


# Back reply button markup
back = types.ReplyKeyboardMarkup(True, False)
back.row(const.LEFTWARDS_ARROW_EMOJI + ' Назад')


# ----------------------------------------------------------------------- #
#                       Generating dates markup                           #
# ----------------------------------------------------------------------- #
today = datetime.today()
today_plus_one = today + timedate.timedelta(1)
today_plus_two = today + timedate.timedelta(2)
today_plus_three = today + timedate.timedelta(3)
today_plus_four = today + timedate.timedelta(4)
today_plus_five = today + timedate.timedelta(5)

dates = telebot.types.InlineKeyboardMarkup()
dates.add(
    types.InlineKeyboardButton(
        text=(datetime.strftime(today, day_of_week(today.weekday()) + ': %d.%m')),
        callback_data=datetime.strftime(today, '%Y-%m-%d')),
    types.InlineKeyboardButton(
        text=(datetime.strftime(today_plus_one, day_of_week(today_plus_one.weekday()) + ': %d.%m')),
        callback_data=datetime.strftime(today_plus_one, '%Y-%m-%d')),
    types.InlineKeyboardButton(
        text=(datetime.strftime(today_plus_two, day_of_week(today_plus_two.weekday()) + ': %d.%m')),
        callback_data=datetime.strftime(today_plus_two, '%Y-%m-%d')))
dates.add(
    types.InlineKeyboardButton(
        text=(datetime.strftime(today_plus_three, day_of_week(today_plus_three.weekday()) + ': %d.%m')),
        callback_data=datetime.strftime(today_plus_three, '%Y-%m-%d')),
    types.InlineKeyboardButton(
        text=(datetime.strftime(today_plus_four, day_of_week(today_plus_four.weekday()) + ': %d.%m')),
        callback_data=datetime.strftime(today_plus_four, '%Y-%m-%d')),
    types.InlineKeyboardButton(
        text=(datetime.strftime(today_plus_five, day_of_week(today_plus_five.weekday()) + ': %d.%m')),
        callback_data=datetime.strftime(today_plus_five, '%Y-%m-%d')))
dates.add(
    types.InlineKeyboardButton(text=(const.REFRESH_EMOJI + " Оновити"), callback_data="dates_refresh"))
# ----------------------------------------------------------------------- #


# ------------------------------------------------------------------------#
#          Parse a list of movies that are available at cinemas           #
#                  on the chosen date and create markups                  #
# ------------------------------------------------------------------------#
film_names_list = []
callback_data_list = []

# Today films markup
today_films = types.InlineKeyboardMarkup()
today_film_list = "SELECT DISTINCT film FROM heroku_982b4fce6d3c135.economkino " \
                  "where date = '%s';" % datetime.strftime(today, '%Y-%m-%d')

cursor.execute(today_film_list)
results = cursor.fetchall()

for row in results:
    film_names_list.append(row[0])
    callback_data_list.append(to_callback_data(row[0]))
    today_films.add(types.InlineKeyboardButton(text=row[0], callback_data=to_callback_data(row[0])))
today_films.add(types.InlineKeyboardButton(text=const.LEFTWARDS_ARROW_EMOJI + ' Назад',
                                           callback_data="films_back"))

# Today + 1 films markup
today_plus_one_films = types.InlineKeyboardMarkup()
today_plus_one_film_list = "SELECT DISTINCT film FROM heroku_982b4fce6d3c135.economkino " \
                  "where date = '%s';" % datetime.strftime(today_plus_one, '%Y-%m-%d')

cursor.execute(today_plus_one_film_list)
results = cursor.fetchall()

for row in results:
    film_names_list.append(row[0])
    callback_data_list.append(to_callback_data(row[0]))
    today_plus_one_films.add(types.InlineKeyboardButton(text=row[0],
                                                        callback_data=to_callback_data(row[0])))
today_plus_one_films.add(types.InlineKeyboardButton(text=const.LEFTWARDS_ARROW_EMOJI + ' Назад',
                                                    callback_data="films_back"))

# Today + 2 films markup
today_plus_two_films = types.InlineKeyboardMarkup()
today_plus_two_film_list = "SELECT DISTINCT film FROM heroku_982b4fce6d3c135.economkino " \
                  "where date = '%s';" % datetime.strftime(today_plus_two, '%Y-%m-%d')

cursor.execute(today_plus_two_film_list)
results = cursor.fetchall()

for row in results:
    film_names_list.append(row[0])
    callback_data_list.append(to_callback_data(row[0]))
    today_plus_two_films.add(types.InlineKeyboardButton(text=row[0],
                                                        callback_data=to_callback_data(row[0])))
today_plus_two_films.add(types.InlineKeyboardButton(text=const.LEFTWARDS_ARROW_EMOJI + ' Назад',
                                                    callback_data="films_back"))

# Today + 3 films markup
today_plus_three_films = types.InlineKeyboardMarkup()
today_plus_three_film_list = "SELECT DISTINCT film FROM heroku_982b4fce6d3c135.economkino " \
                  "where date = '%s';" % datetime.strftime(today_plus_three, '%Y-%m-%d')

cursor.execute(today_plus_three_film_list)
results = cursor.fetchall()

for row in results:
    film_names_list.append(row[0])
    callback_data_list.append(to_callback_data(row[0]))
    today_plus_three_films.add(types.InlineKeyboardButton(text=row[0],
                                                          callback_data=to_callback_data(row[0])))
today_plus_three_films.add(types.InlineKeyboardButton(text=const.LEFTWARDS_ARROW_EMOJI + ' Назад',
                                                      callback_data="films_back"))

# Today + 4 films markup
today_plus_four_films = types.InlineKeyboardMarkup()
today_plus_four_film_list = "SELECT DISTINCT film FROM heroku_982b4fce6d3c135.economkino " \
                  "where date = '%s';" % datetime.strftime(today_plus_four, '%Y-%m-%d')

cursor.execute(today_plus_four_film_list)
results = cursor.fetchall()

for row in results:
    film_names_list.append(row[0])
    callback_data_list.append(to_callback_data(row[0]))
    today_plus_four_films.add(types.InlineKeyboardButton(text=row[0],
                                                         callback_data=to_callback_data(row[0])))
today_plus_four_films.add(types.InlineKeyboardButton(text=const.LEFTWARDS_ARROW_EMOJI + ' Назад',
                                                     callback_data="films_back"))

# Today + 5 films markup
today_plus_five_films = types.InlineKeyboardMarkup()
today_plus_five_film_list = "SELECT DISTINCT film FROM heroku_982b4fce6d3c135.economkino " \
                  "where date = '%s';" % datetime.strftime(today_plus_five, '%Y-%m-%d')

cursor.execute(today_plus_five_film_list)
results = cursor.fetchall()

for row in results:
    film_names_list.append(row[0])
    callback_data_list.append(to_callback_data(row[0]))
    today_plus_five_films.add(types.InlineKeyboardButton(text=row[0],
                                                         callback_data=to_callback_data(row[0])))
today_plus_five_films.add(types.InlineKeyboardButton(text=const.LEFTWARDS_ARROW_EMOJI + ' Назад',
                                                     callback_data="films_back"))
cursor.close()


# ---------------------- Sessions back markups ---------------------- #
today_sessions = types.InlineKeyboardMarkup()
today_sessions.add(types.InlineKeyboardButton(text=(const.LEFTWARDS_ARROW_EMOJI + " Назад"),
                                              callback_data="today_sessions_back"))

today_plus_one_sessions = types.InlineKeyboardMarkup()
today_plus_one_sessions.add(types.InlineKeyboardButton(text=(const.LEFTWARDS_ARROW_EMOJI + " Назад"),
                                                       callback_data="today_plus_one_sessions_back"))

today_plus_two_sessions = types.InlineKeyboardMarkup()
today_plus_two_sessions.add(types.InlineKeyboardButton(text=(const.LEFTWARDS_ARROW_EMOJI + " Назад"),
                                                       callback_data="today_plus_two_sessions_back"))

today_plus_three_sessions = types.InlineKeyboardMarkup()
today_plus_three_sessions.add(types.InlineKeyboardButton(text=(const.LEFTWARDS_ARROW_EMOJI + " Назад"),
                                                         callback_data="today_plus_three_sessions_back"))

today_plus_four_sessions = types.InlineKeyboardMarkup()
today_plus_four_sessions.add(types.InlineKeyboardButton(text=(const.LEFTWARDS_ARROW_EMOJI + " Назад"),
                                                        callback_data="today_plus_four_sessions_back"))

today_plus_five_sessions = types.InlineKeyboardMarkup()
today_plus_five_sessions.add(types.InlineKeyboardButton(text=(const.LEFTWARDS_ARROW_EMOJI + " Назад"),
                                                        callback_data="today_plus_five_sessions_back"))
# ----------------------------------------------------------------------- #
