# Module providing regular expression functions
import re
import configparser
from telebot_calendar import Calendar, CallbackData, ENGLISH_LANGUAGE
from .pymongo_run import get_database

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
    'profile': 'Manage your user profile'
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
        # "ApiToken": "5835138340:AAHjrLvMQtVgOwAGstAoEdb20WqjJZ1sQK4",
        "ApiToken": "5835138340:AAHjrLvMQtVgOwAGstAoEdb20WqjJZ1sQK4",
        "ExpenseCategories": """Food,Groceries,Utilities,
            Transport,Shopping,Miscellaneous""",
        "ExpenseChoices": "Date,Category,Cost",
        "DisplayChoices": "All Expenses,Category Wise,Shared Expense"
    }

    # with open(CONFIG_FILE_NAME, 'w+') as configfile:
    #     config.write(configfile)


def load_config():
    """This is the load config file"""
    config.read(CONFIG_FILE_NAME)


def get_user_expenses_file():
    """This is the get user expenses file function"""
    # setConfig()
    filename = get_database()["USER_EXPENSES"].find()
    user_expenses_dict = {}
    for doc in filename:
        user_expenses_dict[doc["chatid"]] = doc
    return user_expenses_dict


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


# def read_json(filename):
#     try:
#         if not os.path.exists(filename):
#             with open(filename, 'w') as json_file:
#                 json_file.write('{}')
#             return json.dumps('{}')
#         elif os.stat(filename).st_size != 0:
#             with open(filename) as file:
#                 file_data = json.load(file)
#             return file_data

#     except FileNotFoundError:
#         print("---------NO RECORDS FOUND---------")


# def write_json(file_data, filename):
#     try:
#         with open(filename, 'w') as json_file:
#             json.dump(file_data, json_file, ensure_ascii=False, indent=4)
#     except FileNotFoundError:
#         print('Sorry, the data file could not be found.')


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


def create_new_user_record():
    """This is the create new user record function"""
    return user_expenses_format


def get_spend_categories():
    """This is the get spend categories function"""
    categories = config.get('settings', 'ExpenseCategories')
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
