#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime
from telebot.types import CallbackQuery
import telebot
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
from . import crypto
from .pymongo_run import get_database
from .plots import create_time_series_plot, predict_expenses
import os

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
    """This is the start and menu commands"""
    chat_id = m.chat.id
    text_intro = """
        Welcome to WalletWise - a one-stop solution to track your 
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

# function to add a new individual expense
@bot.message_handler(commands=['add'])
def command_add(message):
    """This is the command add function"""
    add.run(message, bot)

# function to add a new group expense
@bot.message_handler(commands=['addGroup'])
def command_addgroup(message):
    """This is the command add subgroup function"""
    add_group.run(message, bot)

# function to fetch expenditure history of the user
@bot.message_handler(commands=['history'])
def command_history(message):
    """This is the command history function"""
    history.run(message, bot)

@bot.message_handler(commands=['profile'])
def command_profile(message):
    """This is the command profile function"""
    profile.run(message, bot)

# function to display total expenditure
@bot.message_handler(commands=['display'])
def command_display(message):
    """This is the command display function"""
    display.run(message, bot)

# handles "/delete" command
@bot.message_handler(commands=['erase'])
def command_erase(message):
    """This is the command erase function"""
    erase.run(message, bot)

# function to show owings of the user
@bot.message_handler(commands=['showOwings'])
def command_owings(message):
    """This is the command showOwings function"""
    show_owings.run(message, bot)

# function to settle balances
@bot.message_handler(commands=['settleUp'])
def command_settle(message):
    """This is the command settleUp function"""
    settle_up.run(message, bot)

# function to add a new individual expense
@bot.message_handler(commands=['crypto'])
def command_add(message):
    """This is the command add function"""
    crypto.run(message, bot)

# function to show calendar for user to select dates
@bot.callback_query_handler(
    func=lambda call: call.data.startswith(helper.calendar_1_callback.prefix)
)
def callback_inline(call: CallbackQuery):
    """This is the callback inline function"""
    display_calendar.run(call, bot)

def main():
    """This is the main function"""
    try:
        bot.polling(none_stop=True)
    except Exception as exception:
        logging.exception(str(exception))
        time.sleep(3)
        print("Connection Timeout")


@bot.message_handler(commands=['trend'])
def show_trend(message):
    try:
        chat_id = str(message.chat.id)
        plot_path = create_time_series_plot(chat_id)
        
        with open(plot_path, 'rb') as photo:
            bot.send_photo(
                message.chat.id, 
                photo, 
                caption="Here's your expense trend:\n- Top: Daily expenses over time\n- Bottom: Total by category"
            )
            
    except Exception as e:
        print(f"Debug - Error in show_trend: {str(e)}")
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(commands=['predict'])
def show_prediction(message):
    try:
        chat_id = str(message.chat.id)
        plot_path, summary = predict_expenses(chat_id)
        
        # Send prediction plot
        with open(plot_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, 
                        caption="📈 Your Expense Predictions")
        
        # Send detailed summary
        bot.send_message(message.chat.id, summary, 
                        parse_mode='Markdown')
            
    except Exception as e:
        print(f"Error in show_prediction: {str(e)}")
        bot.reply_to(message, f"❌ Error: {str(e)}")

if __name__ == '__main__':
    main()


