import transliterate as transliterate
import re


def day_of_week(x):
    str_week_day = ""
    if x == 0:
        str_week_day = "Mon"
    elif x == 1:
        str_week_day = "Tue"
    elif x == 2:
        str_week_day = "Wed"
    elif x == 3:
        str_week_day = "Thu"
    elif x == 4:
        str_week_day = "Fri"
    elif x == 5:
        str_week_day = "Sat"
    elif x == 6:
        str_week_day = "Sun"
    return str_week_day


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def to_callback_data(name):
    res = re.sub("[,.:;!?\-]", "", name)
    if is_english(res):
        return re.sub(" ", "_", res)
    else:
        return transliterate.translit(res, reversed=True).replace(' ', '_')

