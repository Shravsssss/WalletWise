import logging
from . import helper
from .pymongo_run import get_database
from . import add_group

def run(message, bot):
    """This is the run function"""
    msg = bot.reply_to(message, 'Please enter your email')
    bot.register_next_step_handler(msg, post_email_input, bot)


def post_email_input(message, bot):
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
        user_data = None
        for i in item_details:
            #print(i)
            if list(i.values())[1] == email:
                user_data = email
        if user_data is None:
            raise Exception("Sorry! email isn't present in database!")
        message = bot.send_message(
            chat_id,
            "Enter amount for settling up \n(Enter numeric values only)"
        )
        bot.register_next_step_handler(
            message,
            post_amount_input,
            bot        )
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



def post_amount_input(message, bot):
    """This is the post amount input function"""
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        # validate
        amount_value = helper.validate_entered_amount(amount_entered)
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")
        print("----SUCCESS!----")
        dbname = get_database()
        collection_name = dbname["USER_EXPENSES"]

        bot.send_message(chat_id,
            "----SETTLED UP!---"
        )
    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, 'Oh no. ' + str(exception_value))
