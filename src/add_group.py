# Module providing logging functions
import logging
from datetime import datetime
import random
from telebot import types
from email_validator import validate_email
# Module providing helper functions
from . import helper
from .pymongo_run import get_database

option = {}
random.seed(2022)


def run(message, bot):
    """This is the run function"""
    # helper.read_json(helper.get_user_expenses_file())
    # helper.read_json(helper.get_group_expenses_file())
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choicex
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.get_spend_categories():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, expense_category_input, bot)


def expense_category_input(message, bot):
    """This is the expense category input function"""
    chat_id = message.chat.id
    try:
        selected_category = message.text
        exception_string = "Sorry I don't recognise this category "
        exception_string += selected_category + "!"
        if selected_category not in helper.get_spend_categories():
            bot.send_message(
                chat_id,
                'Invalid',
                reply_markup=types.ReplyKeyboardRemove()
            )
            raise Exception(exception_string)

        option[chat_id] = selected_category
        message_text = """Please enter comma separated email ids of all the \
        users you want to add in the expense. \n"""
        message = bot.send_message(chat_id, message_text)
        bot.register_next_step_handler(
            message,
            take_all_users_input,
            bot,
            selected_category
        )
    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, 'Oh no! ' + str(exception_value))
        display_text = ""
        commands = helper.get_commands()
        # generate help text out of the commands dictionary defined at the top
        for command_key, command_value in commands.items():
            display_text += "/" + command_key + ": "
            display_text += command_value + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def take_all_users_input(message, bot, selected_category):
    """This is the take all users input function"""
    chat_id = str(message.chat.id)
    try:
        emails = message.text
        email_ids = set([email.strip() for email in emails.split(",")])

        if not validate_email_input(email_ids):
            raise Exception(f"Sorry the email format is not correct: {emails}")
        dbname = get_database()
        collection_name = dbname["USER_EMAILS"]
        item_details = collection_name.find()
        emails_user_map = {}
        for i in item_details:
            j = list(i.keys())[1]
            emails_user_map[j] = i[j]
        print(emails_user_map)

        if chat_id not in emails_user_map:
            exception_message = """Sorry your email is not registered with us. 
            Please use the /profile command to do so."""
            raise Exception(exception_message)

        email_ids_present_in_expense = email_ids.intersection(
            set(emails_user_map.values())
        )
        if len(email_ids_present_in_expense) != len(email_ids):
            invalid_emails = list(
                email_ids.difference(
                    email_ids_present_in_expense
                )
            )
            exception_message = """Sorry one or more of 
                the email(s) are not registered with us: """ + invalid_emails
            raise Exception(exception_message)

        chat_ids_present_in_expense = [
            get_chat_id(email_id, emails_user_map)
            for email_id in email_ids_present_in_expense
        ]
        chat_ids_present_in_expense.insert(0, chat_id)
        print(chat_ids_present_in_expense)
        option[chat_id] = selected_category
        message = bot.send_message(
            chat_id,
            "How much did you spend on" +
            str(option[chat_id]) +
            "? \n(Enter numeric values only)"
        )
        bot.register_next_step_handler(
            message,
            post_amount_input,
            bot,
            selected_category,
            chat_ids_present_in_expense
        )
    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, 'Oh no! ' + str(exception_value))
        display_text = ""
        commands = helper.get_commands()
        # generate help text out of the commands dictionary defined at the top	
        for command_key, command_value in commands.items():
            display_text += "/" + command_key + ": "
            display_text += command_value + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def post_amount_input(
    message,
    bot,
    selected_category,
    chat_ids_present_in_expense
):
    """This is the post amount input function"""
    chat_id = message.chat.id
    try:
        transaction_record = {}
        amount_entered = message.text
        # validate
        amount_value = helper.validate_entered_amount(amount_entered)
        # cannot be $0 spending
        if amount_value == 0:
            raise Exception("Spent amount has to be a non-zero number.")
        amount_value = float(amount_value)
        print("---SUCCESS---")
        num_members = len(chat_ids_present_in_expense)
        member_share = amount_value / num_members
        transaction_record["total"] = amount_value
        transaction_record["category"] = str(selected_category)
        transaction_record["created_by"] = chat_ids_present_in_expense[0]
        transaction_record["members"] = {}

        for chat_id in chat_ids_present_in_expense:
            transaction_record["members"].update({chat_id: member_share})

        # add user_ids input
        date_of_entry = str(
            datetime.today().strftime(
                helper.get_date_format() +
                ' ' +
                helper.get_time_format()
            )
        )
        transaction_record["created_at"] = date_of_entry
        transaction_record["updated_at"] = None
        print(transaction_record)
        dbname = get_database()
        collection_name = dbname["GROUP_EXPENSES"]
        id_group = str(generate_transaction_id())
        item = {id_group: transaction_record}
        collection_name.insert_one(item)
        collection_name1 = dbname["USER_EXPENSES"]
        item_details = collection_name1.find()
        for chat in chat_ids_present_in_expense:
            flag = 0
            for i in item_details:
                if i['chatid'] == str(chat):
                    flag += 1
                    k = i['group_expenses']+[id_group]
                    collection_name1.update_one(
                        {"chatid": str(chat)},
                        {'$set': {"group_expenses": k}}
                    )
                    break
            if flag == 0:
                item = {
                    "chatid": str(chat),
                    "personal_expenses": [],
                    "group_expenses": [id_group]
                }
                collection_name1.insert_one(item)

    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, 'Oh no. ' + str(exception_value))
        display_text = ""
        commands = helper.get_commands()
        # generate help text out of the commands dictionary defined at the top
        for command_key, command_value in commands.items():
            display_text += "/" + command_key + ": "
            display_text += command_value + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def add_transaction_record(transaction_record):
    """This is the add transaction record function"""
    transaction_list = helper.get_group_expenses_file()
    transaction_id = str(generate_transaction_id())
    transaction_list[transaction_id] = transaction_record
    return transaction_id, transaction_list


def validate_email_input(email_ids):
    """This is the validate email input function"""
    for email in email_ids:
        if not validate_email(email.strip(), check_deliverability=True):
            return False

    return True


def generate_transaction_id():
    """This is the generate transaction id function"""
    r = random.randint(1000, 9999)*random.randint(1000, 9999)
    return r


def add_transactions_to_user(transaction_id, chat_ids):
    """This is the add transactions to user function"""
    transaction_list = helper.get_group_expenses_file()
    user_list = helper.get_user_expenses_file()

    if str(transaction_id) not in transaction_list:
        raise Exception(
            "Transaction " +
            transaction_id +
            "does not exist"
        )

    for user_id in chat_ids:
        existing_transactions = user_list[user_id].get('group_expenses', [])
        existing_transactions.append(transaction_id)
        user_list[user_id]['group_expenses'] = list(set(existing_transactions))

    return user_list


def get_chat_id(email_id, emails_user_map):
    """This is the get chat id function"""
    pos = list(emails_user_map.values()).index(email_id)
    user_id = list(emails_user_map.keys())[pos]
    return user_id
