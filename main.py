from telebot import TeleBot
from telebot import types
import config
import constants
import datetime
from user import User
from time import sleep

bot = TeleBot(config.token)

command_list = ["start", "help", "t"]

select_type = None
problem = None


def get_current_time():
    now = datetime.datetime.now() - datetime.timedelta(minutes=7)

    return now.strftime("%H:%M")


def show_log(message):
    msg = message.text
    chat_id = message.chat.id

    if msg and chat_id:
        current_time = get_current_time()
        print("{} {} - {}".format(current_time, chat_id, msg))


def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(constants.viber)
    markup.add(constants.whats_app)
    markup.add(constants.skype)
    markup.add(constants.telegram)

    return markup


def get_number_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(types.KeyboardButton(constants.send_number, request_contact=True))

    return markup


def remove_keyboard():
    return types.ReplyKeyboardRemove()


def send_to_psy(message, username_skype=None):

    global select_type
    # global username_skype

    print(select_type)

    user = User(message, select_type)

    info = user.get_info()

    if username_skype:
        info += "\nusername от Skype: {}".format(username_skype)

    if problem:
        info += "\nОпис проблемы: {}".format(problem)

    bot.send_message(constants.admin_chat_id, info)
    sleep(10)


@bot.message_handler(commands=command_list)
def command_handler(message):
    msg = str(message.text)
    chat_id = message.chat.id

    global user

    if msg == "/start":
        bot.send_message(chat_id, constants.start_text)
        reply_msg = bot.send_message(message.chat.id, constants.send_detail_your_problem)
        bot.register_next_step_handler(reply_msg, process_send_problem)
        # bot.send_message(chat_id, constants.start_text, reply_markup=get_keyboard())

    elif msg == "/t":
        bot.send_message(chat_id, "Bot is run!)")
    else:
        bot.send_message(chat_id, constants.not_found_answer)

    show_log(message)


@bot.message_handler(content_types=["text"])
def text_handler(message):
    msg = str(message.text)
    chat_id = message.chat.id

    global select_type

    if msg == "test":
        bot.send_message(chat_id, "Test func is success!)")

    if msg == constants.viber or msg == constants.whats_app or msg == constants.telegram:
        select_type = msg
        bot.send_message(chat_id, constants.send_number_please, reply_markup=get_number_keyboard())

    elif msg == constants.skype:
        select_type = msg
        reply_msg = bot.send_message(chat_id, constants.send_skype_username_please)
        bot.register_next_step_handler(reply_msg, process_send_skype_username)

    else:
        bot.send_message(chat_id, constants.not_found_answer)

    show_log(message)


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    bot.send_message(message.chat.id, constants.success_answer, reply_markup=remove_keyboard())
    send_to_psy(message)


# callback functions
def process_send_skype_username(message):

    # global username_skype

    username_skype = str(message.text)

    bot.send_message(message.chat.id, constants.success_answer, reply_markup=remove_keyboard())
    send_to_psy(message, username_skype=username_skype)


def process_send_problem(message):

    global problem

    problem = str(message.text)

    bot.send_message(message.chat.id, constants.select_social_network, reply_markup=get_keyboard())


def main():
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as ex:
        bot.send_message(chat_id=constants.admin_chat_id,
                         text="psychological bot shutdown...\nError description: {}".format(str(ex)))


if __name__ == "__main__":
    main()
