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
from . import budget
from . import goals
from . import recurring_expenses
from . import export_expenses
from . import report
from . import income
from . import currencyConvert  # New import for currency conversion
from .pymongo_run import get_database
from .plots import create_time_series_plot, predict_expenses
import os

# Load configuration
helper.load_config()

bot = telebot.TeleBot(config.TOKEN)
dbname = get_database()
collection_name = dbname["USER_EMAILS"]
telebot.logger.setLevel(logging.INFO)

# Define listener for requests by user
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

# defines how the /start and /help commands have to be handled/processed
# Start and menu commands


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
# Add individual and group expenses


@bot.message_handler(commands=['add'])
def command_add(message):
    add.run(message, bot)

# function to add a new group expense


@bot.message_handler(commands=['addGroup'])
def command_addgroup(message):
    add_group.run(message, bot)

# function to fetch expenditure history of the user
# Fetch expenditure history, profile, display, and erase commands


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

# Show owings and settle balances


@bot.message_handler(commands=['showOwings'])
def command_owings(message):
    show_owings.run(message, bot)


@bot.message_handler(commands=['settleUp'])
def command_settle(message):
    settle_up.run(message, bot)

# function to add a new individual expense


@bot.message_handler(commands=['crypto'])
def command_add(message):
    """This is the command add function"""
    crypto.run(message, bot)

# Register /setBudget command


@bot.message_handler(commands=['setBudget'])
def command_setBudget(message):
    """This is the command add function to run setBudget"""
    budget.run(message, bot)

# Register /checkBudget command


@bot.message_handler(commands=['checkBudget'])
def command_checkBudget(message):
    """This is the command add function to run checkBudget"""
    budget.run(message, bot)

# Register /setGoal command


@bot.message_handler(commands=["setGoal"])
def command_setGoal(message):
    """This is the command add function to run setGoal"""
    goals.run(message, bot)

# Register /checkGoals command


@bot.message_handler(commands=["checkGoals"])
def command_checkGoals(message):
    """This is the command add function to run checkGoals"""
    goals.run(message, bot)

# Register /addSavings command


@bot.message_handler(commands=["addSavings"])
def command_addSavings(message):
    """This is the command add function to run addSavings"""
    goals.run(message, bot)

# Register /addRecurringExpenses command


@bot.message_handler(commands=["addRecurringExpense"])
def command_addRecurringExpense(message):
    """This is the command add function to run addRecurringExpense"""
    recurring_expenses.run(message, bot)

# Register /listRecurringExpenses command


@bot.message_handler(commands=["listRecurringExpenses"])
def command_listRecurringExpenses(message):
    """This is the command add function to run listRecurringExpenses"""
    recurring_expenses.run(message, bot)

# Register /addIncome command


@bot.message_handler(commands=["addIncome"])
def command_addIncome(message):
    """This is the command add function to run addIncome"""
    income.run(message, bot)


# Register /netSavings command


@bot.message_handler(commands=["netSavings"])
def command_netSavings(message):
    """This is the command add function to run netSavings"""
    income.run(message, bot)


# Register /exportExpenses command


@bot.message_handler(commands=["exportExpenses"])
def command_exportExpenses(message):
    """This is the command add function to run exportExpenses"""
    export_expenses.run(message, bot)

# Register /weeklyReport command


@bot.message_handler(commands=["weeklyReport"])
def command_weeklyReport(message):
    """This is the command add function to run weeklyReport"""
    report.run(message, bot)

# Register /monthlyReport command


@bot.message_handler(commands=["monthlyReport"])
def command_monthlyReport(message):
    """This is the command add function to run monthlyReport"""
    report.run(message, bot)

# function to show calendar for user to select dates
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
