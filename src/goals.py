# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

# goals.py

# Module providing goal functions for Telegram bot
from .helper import get_goals_collection, log_and_reply_error


def run(message, bot):
    """This is the run function for goal commands."""
    text = message.json['text'].lower()

    if text.startswith("/setgoal"):
        prompt_set_goal(message, bot)
    elif text.startswith("/checkgoals"):
        show_goals_status(message, bot)
    elif text.startswith("/addsavings"):
        prompt_add_savings(message, bot)
    else:
        return


def prompt_set_goal(message, bot):
    """Prompts user to set a new savings goal."""
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        "Enter your savings goal in the format: [goal_name] [target_amount]\n"
        "Example: Trip 500"
    )
    bot.register_next_step_handler(msg, process_set_goal, bot)


def process_set_goal(message, bot):
    """Processes the input for setting a new savings goal."""
    try:
        chat_id = message.chat.id
        parts = message.text.split(maxsplit=2)
        if len(parts) != 2:
            raise ValueError(
                "Invalid format. Use: [goal_name] [target_amount]."
            )

        goal_name, target_amount = parts[0], float(parts[1])

        # Fetch or initialize user's goals
        goals_collection = get_goals_collection()
        user_goals = goals_collection.find_one({"chatid": str(chat_id)}) or {
            "chatid": str(chat_id), "goals": {}
        }

        # Add or update the goal
        user_goals["goals"][goal_name] = {
            "target": target_amount,
            "saved": 0.0
        }
        goals_collection.update_one(
            {"chatid": str(chat_id)},
            {"$set": user_goals},
            upsert=True
        )

        bot.send_message(
            chat_id,
            f"🎯 Goal '{goal_name}' set with a target of ${target_amount:.2f}!"
        )
    except ValueError:
        bot.send_message(chat_id, "Target amount must be a valid number.")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)


def show_goals_status(message, bot):
    """Displays progress for all savings goals."""
    try:
        chat_id = message.chat.id
        goals_collection = get_goals_collection()
        user_goals = goals_collection.find_one({"chatid": str(chat_id)})

        if not user_goals or not user_goals.get("goals"):
            bot.send_message(
                chat_id, "You have no savings goals set. Use /setGoal to add one.")
            return

        # Build a progress report
        report = "📊 *Your Savings Goals Progress:*\n\n"
        for goal_name, details in user_goals["goals"].items():
            target, saved = details["target"], details["saved"]
            progress = (saved / target) * 100 if target > 0 else 0
            status = "✅ Completed!" if saved >= target else f"{
                progress:.2f}% achieved"
            report += f"*{goal_name}*\n  - Target: ${
                target:.2f}\n  - Saved: ${
                saved:.2f}\n  - Progress: {status}\n\n"

        bot.send_message(chat_id, report, parse_mode="Markdown")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)


def prompt_add_savings(message, bot):
    """Prompts user to add savings towards a goal."""
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        "Enter the goal name and amount to add in the format: [goal_name] [amount_saved]\n"
        "Example: Trip 50"
    )
    bot.register_next_step_handler(msg, process_add_savings, bot)


def process_add_savings(message, bot):
    """Processes the input for adding savings to a goal."""
    try:
        chat_id = message.chat.id
        parts = message.text.split(maxsplit=2)
        if len(parts) != 2:
            raise ValueError(
                "Invalid format. Use: [goal_name] [amount_saved].")

        goal_name, amount_saved = parts[0], float(parts[1])

        # Fetch and update savings for the goal
        goals_collection = get_goals_collection()
        user_goals = goals_collection.find_one({"chatid": str(chat_id)})

        if not user_goals or goal_name not in user_goals.get("goals", {}):
            bot.send_message(
                chat_id, f"Goal '{goal_name}' not found. Use /setGoal to create it.")
            return

        user_goals["goals"][goal_name]["saved"] += amount_saved
        goals_collection.update_one(
            {"chatid": str(chat_id)}, {"$set": user_goals})

        bot.send_message(
            chat_id, f"💰 Added ${
                amount_saved:.2f} to '{goal_name}'.")
    except ValueError:
        bot.send_message(chat_id, "Amount must be a valid number.")
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)
