# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

# recurring_epenses.py
from .helper import calculate_next_due_date, list_recurring_expenses, log_and_reply_error
from apscheduler.schedulers.background import BackgroundScheduler

# We do not add the recurring expenses automatically
# There will be an automatic reminder sent to the user though


def run(message, bot):
    """This is the run function for recurring expenses commands."""
    text = message.text.lower()

    if text.startswith("/addrecurringexpense"):
        prompt_set_recurring_expenses(message, bot)
    elif text.startswith("/listrecurringexpenses"):
        prompt_list_recurring_expenses(message, bot)
    else:
        return


def prompt_set_recurring_expenses(message, bot):
    """Prompts user to set a new recurring expenses."""
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        "Enter your recurring expenses in the format: [category] [amount] [interval]\n"
        "Example: Rent 500 Weekly\n"
        "Example: Utility 50 28"
    )
    bot.register_next_step_handler(msg, process_set_recurring_expenses, bot)


def process_set_recurring_expenses(message, bot):
    """Processes the input for setting a new recurring expenses."""
    try:
        # Start the APScheduler
        global scheduler
        scheduler = BackgroundScheduler()
        scheduler.start()

        chat_id = message.chat.id
        parts = message.text.split(maxsplit=3)
        if len(parts) != 3:
            raise ValueError(
                "Invalid format. Use: [category] [amount] [interval].")

        category, amount, interval = parts[0], float(parts[1]), parts[2]
        # Calculate next due date
        next_due_date = calculate_next_due_date(interval)

        # Fetch or initialize user's goals
        expense_collection = list_recurring_expenses()
        user_expense = expense_collection.find_one({"chatid": str(chat_id)}) or {
            "chatid": str(chat_id), "recurring_expenses": {}}

        # Add or update the goal
        user_expense["recurring_expenses"][category] = {
            "amount": amount, "interval": interval, "next": next_due_date}
        expense_collection.update_one({"chatid": str(chat_id)}, {
            "$set": user_expense}, upsert=True)

        bot.send_message(
            chat_id, f"🎯 Recurring Expense '{category}' set with an amount of ${amount:.2f} with {interval} intervals!")
        bot.send_message(
            chat_id, f"Your nexy due date for '{category}' will be on {next_due_date}")
        message = f"Your nexy due date for '{category}' will be on {next_due_date}"
        scheduler.add_job(
            send_reminder,
            'date',
            run_date=next_due_date,
            args=[chat_id, message, bot]
        )

    except ValueError:
        bot.send_message(chat_id, "Amount must be a valid number.")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)


def prompt_list_recurring_expenses(message, bot):
    """Displays all the recurring expenses."""
    try:
        chat_id = message.chat.id
        goals_collection = list_recurring_expenses()
        user_goals = goals_collection.find_one({"chatid": str(chat_id)})

        if not user_goals or not user_goals.get("recurring_expenses"):
            bot.send_message(
                chat_id, "You have no recurring expenses. Use /addRecurringExpense to add one.")
            return

        # Get the list of expenses
        report = "📊 *Your Recurring Expenses List:*\n\n"
        for category, details in user_goals["recurring_expenses"].items():
            amount, interval, next = details["amount"], details["interval"], details["next"]
            report += f"*{category}*\n  - Amount: ${amount:.2f}\n  - Interval: ${interval}. \
            The next due date is on {next}\n\n"

        bot.send_message(chat_id, report, parse_mode="Markdown")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)


def send_reminder(chat_id, message, bot):
    bot.send_message(chat_id, message)
