import logging
from . import helper
from .pymongo_run import get_database
from . import add_group
from . import show_owings


def run(message, bot):
    """This is the run function"""
    [user_owing_details, user_details] = show_owings.run(message, bot)
    if len(user_owing_details):
        message = bot.reply_to(
            message,
            'Please enter the email of the user you want to settle up with'
        )
        bot.register_next_step_handler(
            message,
            input_settle_up_value,
            bot,
            user_owing_details,
            user_details
        )
    else:
        message = bot.reply_to(
            message,
            'No users to settle up with'
        )


def input_settle_up_value(message, bot, user_owing_details, user_details):
    """This is the post email input function"""
    chat_id = str(message.chat.id)
    try:
        email = message.text
        if not add_group.validate_email_input([email]):
            raise Exception(f"Sorry the email format is not correct: {email}")
        print("----SUCCESS!----")
        dbname = get_database()
        collection_name = dbname["USER_EMAILS"]
        item_details = collection_name.find()
        borrower_chatid = None
        for i in item_details:
            if list(i.values())[1] == email:
                borrower_chatid = list(i.keys())[1]
                borrower_email = email
        if borrower_chatid is None:
            raise Exception("Sorry! email isn't present in database!")
        message = bot.send_message(
            chat_id,
            "Enter amount for settling up \n(Enter numeric values only)"
        )
        bot.register_next_step_handler(
            message,
            post_amount_input,
            bot,
            user_owing_details,
            user_details,
            borrower_chatid,
            borrower_email
        )
    except Exception as exception:
        logging.exception(str(exception))
        bot.reply_to(message, 'Oh no! ' + str(exception))
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
    user_owing_details,
    user_details,
    borrower_chatid,
    borrower_email
):
    """This is the post amount input function"""
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        # validate
        amount_value = helper.validate_entered_amount(amount_entered)
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")
        print("----SUCCESS!----")

        flag = True
        # change in payer details
        for borrower in user_owing_details:
            b_chat_id = borrower["borrower_chatid"]
            if b_chat_id == borrower_chatid:
                borrower["amount"] -= float(amount_entered)
                flag = False
                break
        if flag:
            raise Exception(
                "You don't have a shared expense with the entered email.")
        dbname = get_database()
        collection_name = dbname["OWING_DETAILS"]

        print(user_owing_details)
        collection_name.update_one(
            {"payer_chatid": chat_id},
            {
                "$set": {
                    "borrowers": user_owing_details
                }
            })

        change_payer_info_in_borrower_helper_array = collection_name.find_one({
            "payer_chatid": borrower_chatid
        })["borrowers"]
        for payer in change_payer_info_in_borrower_helper_array:
            p_chatid = payer["borrower_chatid"]
            if p_chatid == chat_id:
                payer["amount"] += float(amount_entered)
                flag = False
                break
        collection_name.update_one(
            {"payer_chatid": borrower_chatid},
            {
                "$set": {
                    "borrowers": change_payer_info_in_borrower_helper_array
                }
            })

        bot.send_message(
            chat_id,
            "Settled up " + amount_entered + " with " + borrower_email
        )
    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, 'Oh no. ' + str(exception_value))
