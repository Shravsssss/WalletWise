# export_expenses.py

# Module providing export functionality for Telegram bot
import csv
import os
import logging
from fpdf import FPDF
from telebot import types
from datetime import datetime
from .helper import fetch_personal_expenses, log_and_reply_error, load_config

load_config()

def run(message, bot):
    """Run function for export commands."""
    chat_id = message.chat.id
    text = message.text.lower()

    if text.startswith("/exportexpenses"):
        prompt_export_expenses(message, bot)
    else:
        return

def prompt_export_expenses(message, bot):
    """Prompts user to specify format and date range for exporting expenses."""
    chat_id = message.chat.id
    msg = bot.send_message(
        chat_id,
        "Enter the format (csv or pdf) and date range for export in the format:\n"
        "[format] [start_date] [end_date]\n"
        "Example: csv 2024-01-01 2024-01-31"
    )
    bot.register_next_step_handler(msg, process_export_request, bot)

def process_export_request(message, bot):
    """Processes the export request and generates the requested file."""
    try:
        chat_id = message.chat.id
        parts = message.text.split(maxsplit=3)
        if len(parts) != 3:
            raise ValueError("Invalid format. Use: [format] [start_date] [end_date].")
        
        export_format, start_date, end_date = parts
        export_format = export_format.lower()
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if export_format not in ["csv", "pdf"]:
            raise ValueError("Format must be either 'csv' or 'pdf'.")

        # Fetch expenses from database
        expenses = fetch_expenses_for_date_range(chat_id, start_date, end_date)
        if not expenses:
            bot.send_message(chat_id, "No expenses found for the specified date range.")
            return

        # Generate and send the file
        if export_format == "csv":
            file_path = generate_csv(expenses, chat_id)
        elif export_format == "pdf":
            file_path = generate_pdf(expenses, chat_id)

        with open(file_path, "rb") as file:
            bot.send_document(chat_id, file)

        # Clean up the generated file
        os.remove(file_path)

    except ValueError as e:
        bot.send_message(chat_id, str(e))
    except Exception as e:
        log_and_reply_error(chat_id, bot, e)

def fetch_expenses_for_date_range(chat_id, start_date, end_date):
    """Fetches expenses for the user within a specified date range."""
    user_expenses = fetch_personal_expenses(chat_id)
    if not user_expenses or "personal_expenses" not in user_expenses:
        return []

    # Filter expenses by date range
    filtered_expenses = []
    for expense in user_expenses["personal_expenses"]:
        date_str, category, amount_str = expense.split(", ")
        expense_date = datetime.strptime(date_str, "%d-%b-%Y %H:%M")
        if start_date <= expense_date <= end_date:
            filtered_expenses.append({"date": date_str, "category": category, "amount": amount_str})
    
    return filtered_expenses

def generate_csv(expenses, chat_id):
    """Generates a CSV file for the expenses."""
    file_name = f"expenses_{chat_id}.csv"
    with open(file_name, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "Category", "Amount"])
        writer.writeheader()
        for expense in expenses:
            writer.writerow({"Date": expense["date"], "Category": expense["category"], "Amount": expense["amount"]})
    return file_name

def generate_pdf(expenses, chat_id):
    """Generates a PDF file for the expenses."""
    file_name = f"expenses_{chat_id}.pdf"
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Expense Report", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Generated on {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(10)

    # Table header
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(60, 10, txt="Date", border=1, align="C")
    pdf.cell(60, 10, txt="Category", border=1, align="C")
    pdf.cell(60, 10, txt="Amount", border=1, align="C")
    pdf.ln()

    # Table rows
    pdf.set_font("Arial", size=10)
    for expense in expenses:
        pdf.cell(60, 10, txt=expense["date"], border=1)
        pdf.cell(60, 10, txt=expense["category"], border=1)
        pdf.cell(60, 10, txt=expense["amount"], border=1)
        pdf.ln()

    pdf.output(file_name)
    return file_name
