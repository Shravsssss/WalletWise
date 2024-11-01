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
from . import show_owings
from . import settle_up
from . import currencyConvert  # New import for currency conversion
from .pymongo_run import get_database

# Load configuration
helper.load_config()

bot = telebot.TeleBot(config.TOKEN)
dbname = get_database()
collection_name = dbname["USER_EMAILS"]
telebot.logger.setLevel(logging.INFO)

# Listener for requests by user
def listener(user_requests):
    """This is the listener function"""
    for req in user_requests:
        if req.content_type == 'text':
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

# Start and menu commands
@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    """This is the start and menu commands"""
    chat_id = m.chat.id

    text_intro = """
        Welcome to WalletBuddy - a one-stop solution to track your 
        expenses with your friends! \n
        Here is a list of available commands, please enter a command 
        of your choice so that I can 
        assist you further: \n\n"""

    commands = helper.get_commands()
    for command_key, command_value in commands.items():
        text_intro += "/" + command_key + ": "
        text_intro += command_value + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True

# Add individual and group expenses
@bot.message_handler(commands=['add'])
def command_add(message):
    add.run(message, bot)

@bot.message_handler(commands=['addGroup'])
def command_addgroup(message):
    add_group.run(message, bot)

# Fetch expenditure history, profile, display, and erase commands
@bot.message_handler(commands=['history'])
def command_history(message):
    history.run(message, bot)

@bot.message_handler(commands=['profile'])
def command_profile(message):
    profile.run(message, bot)

@bot.message_handler(commands=['display'])
def command_display(message):
    display.run(message, bot)

@bot.message_handler(commands=['erase'])
def command_erase(message):
    erase.run(message, bot)

# Show owings and settle balances
@bot.message_handler(commands=['showOwings'])
def command_owings(message):
    show_owings.run(message, bot)

@bot.message_handler(commands=['settleUp'])
def command_settle(message):
    settle_up.run(message, bot)

# Show calendar for date selection
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(helper.calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    display_calendar.run(call, bot)

# Currency conversion command
@bot.message_handler(commands=['currencyConvert'])
def command_currency_convert(message):
    currencyConvert.start_currency_convert(bot, message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('currency_'))
def currency_selection_callback(call):
    currencyConvert.handle_currency_selection(bot, call)

@bot.message_handler(func=lambda message: message.text.isdigit())
def amount_input_handler(message):
    currencyConvert.handle_amount_input(bot, message)

# Main function
def main():
    try:
        bot.polling(none_stop=True)
    except Exception as exception:
        logging.exception(str(exception))
        time.sleep(3)
        print("Connection Timeout")

if __name__ == '__main__':
    main()
