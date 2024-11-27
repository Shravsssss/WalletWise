# income.py
import logging
from telebot import types
from datetime import datetime
from .helper import calculate_monthly_income, log_and_reply_error, list_income_sources, calculate_monthly_expenses, fetch_personal_expenses, has_expenses_this_month


def run(message, bot):
    """This is the run function for income & net saving commands."""
    chat_id = message.chat.id
    text = message.text.lower()

    if text.startswith("/addincome"):
        prompt_set_income(message, bot)
        # Montly net savings
    elif text.startswith("/netsavings"):
        prompt_net_savings(message, bot)
    else:
        return


def prompt_set_income(message, bot):
    """Prompts user to set a new income expenses."""
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        "Enter your income in the format: [income] [description]\n"
        "Example: 500 Company"
    )
    bot.register_next_step_handler(msg, process_set_income, bot)


def process_set_income(message, bot):
    """Processes the input for setting a new income."""
    try:
        chat_id = message.chat.id
        parts = message.text.split(maxsplit=2)
        if len(parts) != 2:
            raise ValueError(
                "Invalid format. Use: [income] [description].")

        income, description = float(parts[0]), parts[1]

        # Fetch or initialize user's income
        expense_collection = list_income_sources()
        user_expense = expense_collection.find_one({"chatid": str(chat_id)}) or {
            "chatid": str(chat_id), "income_sources": {}}

        now = datetime.now()
        # Add or update the goal
        user_expense["income_sources"][description] = {
            "income": income, "date": now}
        expense_collection.update_one({"chatid": str(chat_id)}, {
            "$set": user_expense}, upsert=True)

        bot.send_message(
            chat_id, f"💶 Income source '{description}' set with an amount of ${income:.2f}!")
    except ValueError:
        bot.send_message(chat_id, "Amount must be a valid number.")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)


def prompt_net_savings(message, bot):
    """Displays all the recurring expenses."""
    try:
        chat_id = message.chat.id
        goals_collection = list_income_sources()
        user_income = goals_collection.find_one({"chatid": str(chat_id)}) or {
            "chatid": str(chat_id), "income_sources": {}}
        user_expenses = fetch_personal_expenses(chat_id)
        ex = 0
        if not has_expenses_this_month(user_expenses, chat_id, bot):
            ex = 0
        else:
            ex = calculate_monthly_expenses(fetch_personal_expenses(chat_id))

        inc = 0
        if not user_income or "income_sources" not in user_income:
            inc = 0
        else:
            inc = calculate_monthly_income(user_income)

        net_savings = inc - ex

        if inc != 0 and ex != 0:
            if net_savings <= 0:
                report += f"* 💸 OOPS! You gotta be careful, your net savings for this month is {net_savings}!\n\n"
            else:
                report += f"* 💸 Your net savings for this month is {net_savings}!\n\n"

            bot.send_message(chat_id, report, parse_mode="Markdown")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)
