#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime
import telebot
from telebot.types import CallbackQuery
from . import helper
from . import history
from . import display
from . import erase
from . import add
from . import config
from . import add_group
from . import display_calendar
from . import profile
from .pymongo_run import get_database

# helper.set_config()
helper.load_config()


bot = telebot.TeleBot(config.TOKEN)
dbname = get_database()
collection_name = dbname["USER_EMAILS"]
telebot.logger.setLevel(logging.INFO)


# Define listener for requests by user
def listener(user_requests):
    """This is the listener function"""
    for req in user_requests:
        if req.content_type == 'text':
            # print(req)
            print(
                str(datetime.now()) +
                "name:" +
                str(req.chat.first_name) +
                "chat_id:" +
                str(req.chat.id) +
                "\nmessage:" +
                str(req.text)
            )


bot.set_update_listener(listener)


# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    chat_id = m.chat.id
 
    text_intro = "Welcome to WalletBuddy - a one-stop solution to track your expenses with your friends! \n" \
                 "Here is a list of available commands, please enter a command of your choice so that I can " \
                 "assist you further: \n\n"
 
    commands = helper.get_commands()
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True
 
 
# function to add a new individual expense
@bot.message_handler(commands=['add'])
def command_add(message):
    add.run(message, bot)
 
 
# function to add a new group expense
@bot.message_handler(commands=['addGroup'])
def command_addgroup(message):
    add_group.run(message, bot)
 
 
# function to fetch expenditure history of the user
@bot.message_handler(commands=['history'])
def command_history(message):
    history.run(message, bot)
 
 
@bot.message_handler(commands=['profile'])
def command_profile(message):
    profile.run(message, bot)
 
 
# function to display total expenditure
@bot.message_handler(commands=['display'])
def command_display(message):
    display.run(message, bot)
 
 
# handles "/delete" command
@bot.message_handler(commands=['erase'])
def command_erase(message):
    erase.run(message, bot)
 
 
# function to show calendar for user to select dates
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(helper.calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    display_calendar.run(call, bot)
 
 
def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")
 
 
if __name__ == '__main__':
    main()
