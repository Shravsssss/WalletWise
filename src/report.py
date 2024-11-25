# report.py

from datetime import datetime, timedelta
from collections import defaultdict
from .helper import fetch_personal_expenses, get_group_expenses_file, log_and_reply_error


def run(message, bot):
    """Main entry point for /weeklyReport and /monthlyReport commands."""
    chat_id = message.chat.id
    command = message.text.lower()

    if command == "/weeklyreport":
        period_start = datetime.now() - timedelta(days=7)
        report_period = "Weekly"
    elif command == "/monthlyreport":
        period_start = datetime.now() - timedelta(days=30)
        report_period = "Monthly"
    else:
        bot.reply_to(
            message,
            "Invalid command. Use /weeklyReport or /monthlyReport.")
        return

    try:
        # Fetch and aggregate data
        personal_expenses = fetch_personal_expenses_for_period(
            chat_id, period_start)
        group_expenses = fetch_group_expenses_for_period(chat_id, period_start)
        total_expenses, category_totals = aggregate_expenses(
            personal_expenses + group_expenses)

        # Generate and send summary report
        report_text = generate_summary_report(
            report_period, total_expenses, category_totals)
        bot.send_message(chat_id, report_text, parse_mode="Markdown")

    except Exception as e:
        log_and_reply_error(chat_id, bot, e)


def fetch_personal_expenses_for_period(chat_id, start_date):
    """Fetches personal expenses for the user within the specified period."""
    user_expenses = fetch_personal_expenses(chat_id)
    if not user_expenses or "personal_expenses" not in user_expenses:
        return []

    filtered_expenses = []
    for expense in user_expenses["personal_expenses"]:
        date_str, category, amount_str = expense.split(", ")
        expense_date = datetime.strptime(date_str, "%d-%b-%Y %H:%M")
        if expense_date >= start_date:
            filtered_expenses.append(
                {"type": "Personal", "category": category, "amount": float(amount_str)})

    return filtered_expenses


def fetch_group_expenses_for_period(chat_id, start_date):
    """Fetches group expenses for the user within the specified period."""
    user_expenses = fetch_personal_expenses(chat_id)
    if not user_expenses or "group_expenses" not in user_expenses:
        return []

    group_expense_ids = user_expenses["group_expenses"]
    group_expenses_collection = get_group_expenses_file()
    filtered_expenses = []

    for expense_id in group_expense_ids:
        group_expense = group_expenses_collection.get(expense_id)
        if not group_expense:
            continue

        expense_date = datetime.strptime(
            group_expense["created_at"], "%d-%b-%Y %H:%M")
        if expense_date >= start_date:
            user_share = group_expense["members"].get(str(chat_id))
            if user_share:
                filtered_expenses.append(
                    {"type": "Group", "category": group_expense["category"], "amount": user_share})

    return filtered_expenses


def aggregate_expenses(expenses):
    """Aggregates expenses to calculate total spending and category-wise totals."""
    total_expenses = 0
    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
        total_expenses += expense["amount"]

    return total_expenses, category_totals


def generate_summary_report(report_period, total_expenses, category_totals):
    """Generates a text summary report."""
    if total_expenses == 0:
        return f"📊 *{report_period} Expense Report*\n\nNo expenses recorded during this period."

    report = f"📊 *{report_period} Expense Report*\n\n"
    report += f"🗓 *Period:* Last {7 if report_period == 'Weekly' else 30} Days\n"
    report += f"💸 *Total Spending:* ${total_expenses:.2f}\n\n"
    report += "*Top Categories:*\n"

    sorted_categories = sorted(
        category_totals.items(),
        key=lambda x: x[1],
        reverse=True)
    for category, amount in sorted_categories[:5]:  # Show top 5 categories
        report += f"- {category}: ${amount:.2f}\n"

    report += "\n⚠️ *Anomalies:*\n"
    anomalies = detect_anomalies(category_totals, total_expenses)
    if anomalies:
        report += "\n".join(anomalies)
    else:
        report += "No anomalies detected."

    return report


def detect_anomalies(category_totals, total_expenses):
    """Detects anomalies in spending patterns."""
    anomalies = []
    for category, amount in category_totals.items():
        if amount > total_expenses * \
                0.5:  # Example: More than 50% of total spending in one category
            anomalies.append(f"🚨 High spending on {category}: ${amount:.2f} ({(amount / total_expenses) * 100:.1f}%)")
    return anomalies
