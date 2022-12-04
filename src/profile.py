import logging
from . import helper
from . import add_group
from .pymongo_run import get_database
 
 
 
 
def run(message, bot):
    msg = bot.reply_to(message, 'Please enter your email')
    bot.register_next_step_handler(msg, post_email_input, bot)
 
 
def post_email_input(message, bot):
    chat_id = str(message.chat.id)
    try:
        email = message.text
        if not add_group.validate_email_input([email]):
            raise Exception(f"Sorry the email format is not correct: {email}")
        print("----SUCCESS!----")
 
        dbname = get_database()
        collection_name = dbname["USER_EMAILS"]
        item = {str(message.chat.id):email}
        collection_name.insert_one(item)
        message = bot.send_message(message.chat.id, 'Successfully added your email! \n')
       
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = ""
        commands = helper.get_commands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)
 
