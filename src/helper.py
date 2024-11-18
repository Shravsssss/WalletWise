# Module providing regular expression functions
import re
import os
import json
import configparser
from telebot_calendar import Calendar, CallbackData, ENGLISH_LANGUAGE
from .pymongo_run import get_database
from datetime import datetime
import logging

# calendar initialized
calendar = Calendar(language=ENGLISH_LANGUAGE)
calendar_1_callback = CallbackData(
    "calendar_1",
    "action",
    "year",
    "month",
    "day"
)

user_expenses_format = {
    "personal_expenses": [],
    "group_expenses": []
}

commands = {
    'menu': 'Display this menu',
    'add': 'Record/Add a new spending',
    'addGroup': 'Add a group expense',
    'display': 'Show sum of expenditure for the current day/month',
    'history': 'Display spending history',
    'erase': 'Clear/Erase all your records',
    'profile': 'Manage your user profile',
    'showOwings': 'Show owed amount details',
    'settleUp': 'Settle up pending dues',
    'crypto' : 'Record or Add a new crypto spending',
    'setBudget' : 'Set budget for current month by category',
    'checkBudget' : 'Check the budget for current month',
    'setGoal' : 'Set a new savings goal',
    'checkGoals' : 'Check progress towards your savings goals',
    'addSavings' : 'Add saved money towards a specific goal',
    'trend': 'View your expense trend over time',
    'predict': 'Get expense predictions for the next 30 days',
    'currencyConvert': 'Convert to a different Currency',
}

date_range = []

config = configparser.ConfigParser()
DB = {}
CONFIG_FILE_NAME = "config.ini"


def set_config():
    """This is the set config function"""
    # config["files"] = {
    #     "UserExpenses": "user_expenses.json",
    #     "GroupExpenses": "group_expenses.json",
    #     "UserProfile": "user_emails.json"
    # }
    global DB
    DB = get_database()
    config["settings"] = {
        "ApiToken": "5835138340:AAHjrLvMQtVgOwAGstAoEdb20WqjJZ1sQK4",
        #"ApiToken": "8113186837:AAEu20LqkGTx2CGS9lqunMuvDw1JzUAPJx8",
        #"ApiToken": "7835402356:AAFPFp2j8QLa7E_qFCMxVw5e0NTeSET9Jj8",
        "ExpenseCategories": """Food,Groceries,Utilities,
            Transport,Shopping,Miscellaneous""",
        "CryptoCategories": """"Bitcoin,Ethereum,Ripple,Litecoin""",
        "ExpenseChoices": "Date,Category,Cost",
        "DisplayChoices": "All Expenses,Category Wise,Shared Expense"
    }

    # with open(CONFIG_FILE_NAME, 'w+') as configfile:
    #     config.write(configfile)


def load_config():
    """This is the load config file"""
    config.read(CONFIG_FILE_NAME)


def get_group_expenses_file():
    """This is the get group expenses file function"""
    # setConfig()
    filename = get_database()["GROUP_EXPENSES"].find()
    group_expenses_dict = {}
    for doc in filename:
        for key in doc:
            if key != "_id":
                group_expenses_dict[key] = doc[key]
    # print(d)
    return group_expenses_dict


def get_user_profile_file():
    """This is the get user profile file function"""
    # setConfig()
    filename = get_database()["USER_EMAILS"].find()
    user_profile_dict = {}
    for doc in filename:
        for key in doc:
            if key != "_id":
                user_profile_dict[key] = doc[key]
    # print(d)
    return user_profile_dict


def read_json(filename):
    """This is the read json function"""
    try:
        if not os.path.exists(filename):
            with open(filename, 'w') as json_file:
                json_file.write('{}')
            return json.dumps('{}')
        elif os.stat(filename).st_size != 0:
            with open(filename) as file:
                file_data = json.load(file)
            return file_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def write_json(file_data, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(file_data, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print('Sorry, the data file could not be found.')


def validate_entered_amount(amount_entered):
    """This is the validate entered amount function"""
    if amount_entered is None:
        return 0
    if re.match(
        "^[1-9][0-9]{0,14}\\.[0-9]*$",
        amount_entered
    ) or re.match(
        "^[1-9][0-9]{0,14}$",
        amount_entered
    ):
        amount = round(float(amount_entered), 2)
        if amount > 0:
            return str(amount)
    return 0


def get_user_history(chat_id):
    """This is the get user history function"""
    user_history = get_database()["USER_EXPENSES"] \
        .find_one({"chatid": str(chat_id)})
    # print(userHistory)
    if bool(user_history):
        return user_history
    else:
        print("EMPTY")
        return None

def get_crypto_types():
    """This is the get crypto spend categories function"""
    crypto_categories = config.get('settings', 'CryptoCategories')
    crypto_categories = crypto_categories.split(",")
    return crypto_categories

def get_spend_categories():
    """This is the get spend categories function"""
    categories = config.get('settings', 'ExpenseCategories')
    categories = categories.split(",")
    return categories

def get_currency_options():
    """This is the get currency options function"""
    categories = config.get('settings', 'CurrencyCategories')
    categories = categories.split(",")
    return categories


def get_spend_display_options():
    """This is the get spend display options function"""
    choices = config.get('settings', 'DisplayChoices')
    choices = choices.split(",")
    return choices


def get_expense_choices():
    """This is the get expense choices function"""
    choices = config.get('settings', 'ExpenseChoices')
    choices = choices.split(",")
    return choices


def get_api_token():
    """This is the get api token function"""
    return config['settings']['ApiToken']


def get_data_availability_messages(element):
    """This is the get data availability messages"""
    messages = {
        1: "No expense found for user",
        2: "No shared expense found for user ",
        5: "No expense data for selected dates",
        6: "No expense data for selected dates and category"
    }
    return messages[element]


def get_decision_choices():
    """This is the get decision choices function"""
    return ['Yes', 'No']


def get_commands():
    """This is the get commands function"""

    return commands


def get_date_format():
    """This is the get date format function"""
    date_format = '%d-%b-%Y'
    return date_format


def get_time_format():
    """This is the get time format function"""
    time_format = '%H:%M'
    return time_format


def get_month_format():
    """This is the get month format function"""
    month_format = '%b-%Y'
    return month_format


def get_user_expenses_file():
    """This is the get user expenses function"""
    # setConfig()
    filename = config['files']['UserExpenses']
    return os.path.join("data", filename)


def create_new_user_record():
    """This is the create new user record function"""
    return user_expenses_format


def get_budgets_collection():
    """Returns the USER_BUDGETS collection."""
    db = get_database()
    return db["USER_BUDGETS"]


def get_expenses_collection():
    """Returns the USER_EXPENSES collection."""
    db = get_database()
    return db["USER_EXPENSES"]


def save_budget_for_category(chat_id, category, amount):
    """Saves or updates the budget for a specific category in the database."""
    budgets_collection = get_budgets_collection()
    budgets_collection.update_one(
        {"chatid": str(chat_id)},
        {"$set": {f"budgets.{category}": amount}},
        upsert=True
    )


def fetch_user_budget(chat_id):
    """Fetches the user's budget document from the database."""
    budgets_collection = get_budgets_collection()
    return budgets_collection.find_one({"chatid": str(chat_id)})


def fetch_personal_expenses(chat_id):
    """Fetches the user's personal expenses document from the database."""
    expenses_collection = get_expenses_collection()
    return expenses_collection.find_one({"chatid": str(chat_id)})


def is_expense_in_current_month(date):
    """Checks if a date is in the current month and year."""
    now = datetime.now()
    return date.month == now.month and date.year == now.year


def calculate_monthly_expenses(expenses):
    """Calculates total expenses per category for the current month."""
    monthly_expenses = {}
    for exp in expenses:
        date_str, category, amount_str = exp.split(", ")
        date = datetime.strptime(date_str, "%d-%b-%Y %H:%M")
        
        if is_expense_in_current_month(date):
            amount = float(amount_str)
            if category in monthly_expenses:
                monthly_expenses[category] += amount
            else:
                monthly_expenses[category] = amount

    return monthly_expenses


def parse_budget_input(text):
    """
    Parses and validates the budget input format.

    Ensures the input is in the format: [category] [amount]
    and validates that the category exists in the allowed categories.
    """
    parts = text.split()
    if len(parts) != 2:
        raise ValueError("Invalid format. Please use the format: [category] [amount].")
    
    category = parts[0]
    try:
        amount = float(parts[1])
    except ValueError:
        raise ValueError("Amount must be a number.")
    
    # Fetch valid categories from configuration
    categories = config.get('settings', 'ExpenseCategories').split(',')
    
    # Check if the category exists
    if category not in categories:
        raise ValueError(f"Invalid category. Allowed categories are: {', '.join(categories)}")
    
    return category, amount


def is_budget_set(user_budget, chat_id, bot):
    """Checks if the budget is set for the user."""
    if not user_budget or "budgets" not in user_budget:
        bot.send_message(chat_id, "You haven't set any budgets yet. Use /setBudget to set a budget.")
        return False
    return True


def has_expenses_this_month(user_expenses, chat_id, bot):
    """Checks if the user has any expenses for the current month."""
    if not user_expenses or "personal_expenses" not in user_expenses:
        bot.send_message(chat_id, "No expenses found for this month.")
        return False
    return True


def build_budget_report(budgets, monthly_expenses):
    """Builds the budget report message text."""
    report = "📊 *Monthly Budget Report*\n\n"
    for category, budget_amount in budgets.items():
        spent = monthly_expenses.get(category, 0)
        remaining = budget_amount - spent
        report += f"*{category}*\n"
        report += f"  - Budget: ${budget_amount:.2f}\n"
        report += f"  - Spent: ${spent:.2f}\n"
        report += f"  - Remaining: ${remaining:.2f}\n\n"
        
        # Add alerts for close-to or over budget
        if remaining < 0:
            report += f"⚠️ *Alert*: You have exceeded your budget for {category} by ${-remaining:.2f}!\n\n"
        elif remaining < budget_amount * 0.2:
            report += f"⚠️ *Warning*: You are close to reaching your budget for {category}.\n\n"

    return report


def log_and_reply_error(chat_id, bot, exception_value):
    """Logs the exception and replies to the user with an error message."""
    logging.exception(str(exception_value))
    bot.send_message(chat_id, 'An error occurred: ' + str(exception_value))

    
def get_goals_collection():
    """Returns the goals collection."""
    db = get_database()
    return db["USER_GOALS"]
