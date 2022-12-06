import logging
from . import helper
from .pymongo_run import get_database


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
