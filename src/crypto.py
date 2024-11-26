# crypto.py

# Module providing logging functions
import logging
from datetime import datetime
from telebot import types
# Module providing helper functions
from . import helper
from .pymongo_run import get_database

option = {}


def run(message, bot):
    """This is the run function"""
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.get_crypto_types():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Cryptocurrency', reply_markup=markup)
    bot.register_next_step_handler(msg, post_crypto_selection, bot)


def post_crypto_selection(message, bot):
    """This is the post cryptocurrency selection"""
    try:
        chat_id = message.chat.id
        selected_crypto = message.text
        if selected_crypto not in helper.get_crypto_types():
            bot.send_message(
                chat_id,
                'Invalid',
                reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(
                f"Sorry I don't recognize this cryptocurrency {selected_crypto}!")

        option[chat_id] = selected_crypto
        message = bot.send_message(
            chat_id, f"How much would you like to add to {option[chat_id]}? \n(Enter numeric values only)")
        bot.register_next_step_handler(
            message, post_amount_input, bot, selected_crypto)
    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, 'Oh no! ' + str(exception_value))
        display_text = ""
        commands = helper.get_commands()
        for command_key, command_value in commands.items():
            display_text += f"/{command_key}: {command_value}\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def post_amount_input(message, bot, selected_crypto):
    """This is the post amount input function"""
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)
        if amount_value == 0:
            raise Exception("Amount has to be a non-zero number.")
        print("----SUCCESS!----")

        date_of_entry = datetime.today().strftime(
            helper.get_date_format() + ' ' + helper.get_time_format()
        )
        text_string = f"{date_of_entry}, {option[chat_id]}, {amount_value}"

        dbname = get_database()
        collection_name = dbname["USER_EXPENSES"]
        item_details = collection_name.find()
        flag = 0
        for i in item_details:
            if i['chatid'] == str(chat_id):
                flag += 1
                k = i['personal_expenses'] + [text_string]
                collection_name.update_one(
                    {"chatid": str(chat_id)},
                    {'$set': {"personal_expenses": k}}
                )
                break
        if flag == 0:
            item = {
                "chatid": str(chat_id),
                "personal_expenses": [text_string],
                "group_expenses": []
            }
            collection_name.insert_one(item)

        bot.send_message(chat_id,f"The following transaction has been recorded: You added {amount_value} to {option[chat_id]} on {date_of_entry}")
    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, 'Oh no. ' + str(exception_value))


def add_user_record(chat_id, record_to_be_added):
    """This is the add user record function"""
    user_list = helper.read_json(helper.get_user_crypto_file())
    if str(chat_id) not in user_list:
        user_list[str(chat_id)] = helper.create_new_user_record()
    user_list[str(chat_id)]['personal_expenses'].append(record_to_be_added)
    return user_list
