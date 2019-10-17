import datetime


def log_message(message):
    print()
    print(datetime.datetime.now())
    print("Username: {0} (id = {1}) \nMessage: {2}".format(message.from_user.username,
                                                           str(message.from_user.id),
                                                           message.text))


def log_call(call):
    print()
    print(datetime.datetime.now())
    print("Username: {0} (id = {1}) \nCallback: {2}".format(call.from_user.username,
                                                            str(call.from_user.id),
                                                            call.data))
