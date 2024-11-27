# budget.py

# Module providing budget functions for Telegram bot
from telebot import types
from . import helper

helper.load_config()

option = {}


def run(message, bot):
    """This is the run function for budget commands."""
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove any previous choices
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for opt in helper.get_decision_choices():
        markup.add(opt)

    text = message.json['text'].lower()
    if text.startswith("/setbudget"):
        prompt_set_budget(message, bot)
    elif text.startswith("/checkbudget"):
        show_budget_status(message, bot)
    else:
        return


def prompt_set_budget(message, bot):
    """Prompts user to enter budget category and amount."""
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        "Please enter the category and amount you want to set for the budget in the format: [category] [amount]\n"
        "Example: Food 200")
    bot.register_next_step_handler(msg, process_budget_input, bot)


def process_budget_input(message, bot):
    """Processes budget category and amount input."""
    try:
        chat_id = message.chat.id
        category, amount = helper.parse_budget_input(message.text)
        helper.save_budget_for_category(chat_id, category, amount)
        bot.send_message(chat_id, f"Budget set for {category}: ${amount:.2f}")
    except ValueError as exception_value:
        bot.send_message(chat_id, str(exception_value))
    except Exception as exception_value:
        helper.log_and_reply_error(chat_id, bot, exception_value)


def show_budget_status(message, bot):
    """Displays current budget status and sends alerts if close to or over budget."""
    try:
        chat_id = message.chat.id
        user_budget = helper.fetch_user_budget(chat_id)
        user_expenses = helper.fetch_personal_expenses(chat_id)

        if not helper.is_budget_set(user_budget, chat_id, bot):
            return
        if not helper.has_expenses_this_month(user_expenses, chat_id, bot):
            return

        budgets = user_budget["budgets"]
        monthly_expenses = helper.calculate_monthly_expenses(
            user_expenses["personal_expenses"])
        report = helper.build_budget_report(budgets, monthly_expenses)
        bot.send_message(chat_id, report, parse_mode="Markdown")
    except Exception as exception_value:
        helper.log_and_reply_error(chat_id, bot, exception_value)
