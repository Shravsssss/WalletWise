# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

import os
from datetime import datetime
from telebot import types
from .helper import (
    fetch_personal_expenses,
    get_group_expenses_file,
    generate_pdf,
    generate_csv,
    log_and_reply_error,
)

# Temporary storage for user-specific export preferences
user_export_preferences = {}


def run(message, bot):
    """Run function for export commands."""
    chat_id = message.chat.id
    user_export_preferences[chat_id] = {}  # Initialize user preferences
    prompt_export_format(message, bot)


def prompt_export_format(message, bot):
    """Prompts user to select the export format."""
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("CSV", "PDF")
    msg = bot.reply_to(
        message,
        "Select the format for exporting expenses (CSV or PDF):",
        reply_markup=markup)
    bot.register_next_step_handler(msg, prompt_start_date, bot)


def prompt_start_date(message, bot):
    """Prompts the user to input the start date."""
    chat_id = message.chat.id
    export_format = message.text.upper()

    if export_format not in ["CSV", "PDF"]:
        bot.reply_to(
            message,
            "Invalid format. Please restart the process with /exportexpenses.")
        return

    # Save user preference for export format
    user_export_preferences[chat_id]["format"] = export_format
    msg = bot.reply_to(message, "Enter the start date (format: YYYY-MM-DD):")
    bot.register_next_step_handler(msg, prompt_end_date, bot)


def prompt_end_date(message, bot):
    """Prompts the user to input the end date."""
    chat_id = message.chat.id
    try:
        start_date = datetime.strptime(message.text.strip(), "%Y-%m-%d")
        user_export_preferences[chat_id]["start_date"] = start_date
        msg = bot.reply_to(message, "Enter the end date (format: YYYY-MM-DD):")
        bot.register_next_step_handler(msg, process_export_request, bot)
    except ValueError:
        bot.reply_to(
            message,
            "Invalid date format. Please restart the process with /exportexpenses.")


def process_export_request(message, bot):
    """Processes the export request and generates the requested file."""
    chat_id = message.chat.id
    try:
        end_date = datetime.strptime(message.text.strip(), "%Y-%m-%d")
        start_date = user_export_preferences[chat_id]["start_date"]

        if start_date > end_date:
            bot.reply_to(
                message,
                "Start date must be earlier than end date. Please restart the process.")
            return

        export_format = user_export_preferences[chat_id]["format"]

        # Fetch expenses for the selected date range
        personal_expenses = fetch_personal_expenses_for_date_range(
            chat_id, start_date, end_date)
        group_expenses = fetch_group_expenses_for_date_range(
            chat_id, start_date, end_date)
        expenses = personal_expenses + group_expenses

        if not expenses:
            bot.send_message(
                chat_id, "No expenses found for the selected date range.")
            return

        # Generate and send the file
        if export_format == "CSV":
            file_path = generate_csv(expenses, chat_id)
        elif export_format == "PDF":
            file_path = generate_pdf(expenses, chat_id)

        with open(file_path, "rb") as file:
            bot.send_document(chat_id, file)

        # Clean up
        os.remove(file_path)

    except ValueError:
        bot.reply_to(
            message,
            "Invalid date format. Please restart the process.")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)


def fetch_personal_expenses_for_date_range(chat_id, start_date, end_date):
    """Fetches personal expenses for the user within a date range."""
    user_expenses = fetch_personal_expenses(chat_id)
    if not user_expenses or "personal_expenses" not in user_expenses:
        return []

    filtered_expenses = []
    for expense in user_expenses["personal_expenses"]:
        date_str, category, amount_str = expense.split(", ")
        expense_date = datetime.strptime(date_str, "%d-%b-%Y %H:%M")
        if start_date <= expense_date <= end_date:
            filtered_expenses.append({
                "type": "Personal",
                "date": date_str,
                "category": category,
                "amount": amount_str
            })

    return filtered_expenses


def fetch_group_expenses_for_date_range(chat_id, start_date, end_date):
    """Fetches group expenses for the user within a date range."""
    # Fetch the user's group expense IDs
    user_expenses = fetch_personal_expenses(chat_id)
    if not user_expenses or "group_expenses" not in user_expenses:
        return []

    group_expense_ids = user_expenses["group_expenses"]
    # Access GROUP_EXPENSES collection
    group_expenses_collection = get_group_expenses_file()
    filtered_expenses = []

    # Iterate through group expense IDs to fetch data
    for expense_id in group_expense_ids:
        group_expense = group_expenses_collection.get(expense_id)
        if not group_expense:
            continue  # Skip if expense ID is invalid

        # Parse the group expense data
        expense_date = datetime.strptime(
            group_expense["created_at"], "%d-%b-%Y %H:%M")
        if start_date <= expense_date <= end_date:
            user_share = group_expense["members"].get(str(chat_id))
            if user_share:  # Include only if the user has a share
                filtered_expenses.append({
                    "type": "Group",
                    "date": group_expense["created_at"],
                    "category": group_expense["category"],
                    # Include only the user's share
                    "amount": f"{user_share:.2f}"
                })

    return filtered_expenses
