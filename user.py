import constants

class User(object):
    phone_number = None
    chat_id = 0
    first_name = None
    last_name = None
    username = None
    type = None

    def __init__(self, message, type):

        if type != constants.skype:
            self.phone_number = str(message.contact.phone_number)
        else:
            self.phone_number = None

        self.chat_id = message.chat.id
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name
        self.username = message.from_user.username
        self.type = type

    def get_info(self):
        info = ""

        if self.phone_number:
            info += str("Номер телефону: {}".format(self.phone_number))

        if self.chat_id:
            info += "\nChat id: {}".format(self.chat_id)

        if self.first_name:
            info += "\nІм'я: {}".format(self.first_name)

        if self.last_name:
            info += "\nПрізвище: {}".format(self.last_name)

        if self.username:
            info += "\nЮзернейм: @{}".format(self.username)

        if self.type:
            info += "\nТип зв`язку: {}".format(self.type)

        return info