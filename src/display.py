# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

import time
from datetime import datetime
import os
from telebot import types
from . import plots
# Module providing helper functions
from . import helper

# getting json files

helper.load_config()


def run(message, bot):
    """This is the run function"""
    helper.date_range = []
    date_selections(message, bot)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for opt in helper.get_decision_choices():
        markup.add(opt)
    msg = bot.reply_to(
        message,
        'Do you want to see the expense charts?',
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, show_categories, bot)


def date_selections(message, bot):
    """This is the date selections function"""
    # print("date_selections")
    now = datetime.now()
    bot.send_message(
        message.chat.id,
        "Select start date",
        reply_markup=helper.calendar.create_calendar(
            name=helper.calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )
    bot.send_message(
        message.chat.id,
        "Select end date",
        reply_markup=helper.calendar.create_calendar(
            name=helper.calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )


def show_categories(message, bot):
    """This is the show categories function"""
    try:
        chat_id = message.chat.id
        opt = message.text
        if opt not in helper.get_decision_choices():
            exception_message = "Sorry wrong option " + opt + "!"
            raise Exception(exception_message)

        if opt == 'Yes':
            expense_dict = helper.get_user_expenses_file()
            transaction_dict = helper.get_group_expenses_file()
            history = helper.get_user_history(chat_id)
            if not history:
                bot.send_message(
                    chat_id,
                    "Oops! Looks like you do not have any spending records!"
                )
            else:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row_width = 2
                for mode in helper.get_spend_display_options():
                    markup.add(mode)
                msg = bot.reply_to(
                    message,
                    'Please select a category to see the total expense',
                    reply_markup=markup
                )
                bot.register_next_step_handler(
                    msg,
                    display_total,
                    bot,
                    expense_dict,
                    transaction_dict
                )
        else:
            bot.reply_to(
                message,
                "Okay, you selected No hence there is no chart displayed"
            )

    except Exception as exception_value:
        bot.reply_to(message, str(exception_value))


def expense_category(message, bot, expense_dict, transaction_dict):
    """This is the expense category funciton"""
    print("expense_categror")
    try:
        start_date = helper.date_range[0]
        end_date = helper.date_range[1]
        # print(start_date)
        # print(end_date)
        chat_id = message.chat.id
        choice_category = message.text
        if choice_category not in helper.get_spend_categories():
            exception_message = "Sorry I can't show spendings for "
            exception_message += choice_category + "!"
            raise Exception(exception_message)
        print("expense_category_plot")
        check = plots.categorical_plot(
            str(chat_id),
            start_date,
            end_date,
            choice_category,
            expense_dict
        )
        check1 = plots.hist_categorical_plot(
            str(chat_id),
            start_date,
            end_date,
            choice_category,
            expense_dict
        )
        check2 = plots.box_categorical_plot(
            str(chat_id),
            start_date,
            end_date,
            choice_category,
            expense_dict
        )
        print(check)
        if check != 7 or check1 != 7 or check2 != 7:
            plotmsg = helper.get_data_availability_messages(check)
            bot.reply_to(message, plotmsg)
        else:
            # print("executed")
            bot.send_photo(
                chat_id,
                photo=open(
                    'categorical_expenses.png',
                    'rb'
                )
            )
            bot.send_photo(chat_id, photo=open('hist.png', 'rb'))
            bot.send_photo(chat_id, photo=open('box_cat.png', 'rb'))
            os.remove('categorical_expenses.png')
            os.remove('hist.png')
            os.remove('box_cat.png')

    except Exception as exception_value:
        bot.reply_to(message, str(exception_value))


def display_total(message, bot, expense_dict, transaction_dict):
    """This is the display total function"""
    try:
        chat_id = message.chat.id
        choice = message.text
        start_date = helper.date_range[0]
        end_date = helper.date_range[1]

        if choice not in helper.get_spend_display_options():
            exception_message = "Sorry I can't show spendings for "
            exception_message += choice + "!"
            raise Exception(exception_message)

        history = helper.get_user_history(chat_id)
        if history is None:
            exception_message = """Oops! Looks like you do not
            have any spending records!"""
            raise Exception(exception_message)

        # show the bot "typing" (max. 5 secs)
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(0.5)

        if choice == 'All Expenses':
            print('diplay+total_all_exp')
            check = plots.overall_plot(
                str(chat_id),
                start_date,
                end_date,
                expense_dict,
                transaction_dict
            )
            check2 = plots.pie_plot(
                str(chat_id),
                start_date,
                end_date,
                expense_dict,
                transaction_dict
            )
            check3 = plots.box_plot(
                str(chat_id),
                start_date,
                end_date,
                expense_dict,
                transaction_dict
            )
            if check != 7 or check2 != 7 or check3 != 7:
                plotmsg = helper.get_data_availability_messages(check)
                bot.reply_to(message, plotmsg)
            else:
                bot.send_photo(
                    chat_id,
                    photo=open(
                        'overall_expenses.png',
                        'rb'
                    )
                )
                bot.send_photo(chat_id, photo=open('pie.png', 'rb'))
                bot.send_photo(chat_id, photo=open('box.png', 'rb'))
                os.remove('overall_expenses.png')
                os.remove('pie.png')
                os.remove('box.png')

        elif choice == 'Category Wise':
            # helper.read_json()
            print("display_total_categpr")
            chat_id = message.chat.id
            # helper.option.pop(chat_id, None)  # remove temp choice
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 2
            for category in helper.get_spend_categories():
                markup.add(category)
            msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
            bot.register_next_step_handler(
                msg,
                expense_category,
                bot,
                expense_dict,
                transaction_dict
            )

        elif choice == 'Shared Expense':
            check = plots.owe(str(chat_id), expense_dict, transaction_dict)
            if check != 7:
                plotmsg = helper.get_data_availability_messages(check)
                bot.reply_to(message, plotmsg)
            else:
                bot.send_photo(chat_id, photo=open('owe.png', 'rb'))
                os.remove('owe.png')

    except Exception as exception_value:
        bot.reply_to(message, str(exception_value))
