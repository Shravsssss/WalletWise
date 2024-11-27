from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src import report, helper
import pytest
# from src.pymongo_run import get_database
from datetime import datetime

# # Connect to the database
# @pytest.fixture(scope="module")
# def db():
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["test_walletwise"]
#     yield db
#     client.drop_database("test_walletwise")  # Cleanup after tests

# Add mock data to the database


@pytest.fixture
def setup_mock_data():
    expense_collection = helper.get_expenses_collection()
    # Insert mock personal expenses
    expense_collection.insert_one({
        "chatid": "12345",
        "personal_expenses": ["19-Nov-2024 10:00, Food, 50"],
        "group_expenses": ["55667430"]
    })

    # Insert mock group expenses
    helper.get_group_expenses().insert_one({
        "55667430": {
            "total": 100,
            "category": "Food",
            "created_by": "7121391035",
            "members": {
                "7121391035": 33.33,
                "7121391036": 33.33
            },
            "created_at": "18-Nov-2024 20:07",
            "updated_at": None
        }
    })

    yield

    # Teardown: Remove mock data after the test
    expense_collection.delete_many({"chatid": "12345"})
    expense_collection.delete_many({"_id": "group1"})


@patch('src.helper.fetch_personal_expenses')
@patch('telebot.TeleBot')
def test_run_with_weekly_report(mock_bot, mock_fetch_personal_expenses):
    """
    Test the run function with the /weeklyReport command.

    Args:
        mock_bot: Mocked TeleBot instance.
        mock_fetch_personal_expenses: Mocked fetch_personal_expenses function.
    """
    mock_bot_instance = mock_bot.return_value
    mock_fetch_personal_expenses.return_value = {
        "personal_expenses": ["20-Nov-2024 10:00, Food, 50"]}

    message = create_message("/weeklyreport")
    report.run(message, mock_bot_instance)

    assert mock_bot_instance.send_message.called


@patch('src.helper.fetch_personal_expenses')
@patch('telebot.TeleBot')
def test_run_with_monthly_report(mock_bot, mock_fetch_personal_expenses):
    """
    Test the run function with the /monthlyReport command.

    Args:
        mock_bot: Mocked TeleBot instance.
        mock_fetch_personal_expenses: Mocked fetch_personal_expenses function.
    """
    mock_bot_instance = mock_bot.return_value
    mock_fetch_personal_expenses.return_value = {
        "personal_expenses": ["01-Nov-2024 10:00, Travel, 200"]}

    message = create_message("/monthlyreport")
    report.run(message, mock_bot_instance)

    assert mock_bot_instance.send_message.called


@patch('telebot.TeleBot')
def test_run_with_invalid_command(mock_bot):
    """
    Test the run function with an invalid command.

    Args:
        mock_bot: Mocked TeleBot instance.
    """
    mock_bot_instance = mock_bot.return_value
    message = create_message("/invalidcommand")
    report.run(message, mock_bot_instance)

    assert mock_bot_instance.reply_to.called


def test_fetch_personal_expenses_for_period(setup_mock_data):
    """
    Test the fetch_personal_expenses_for_period function with data in the database.
    """
    start_date = datetime.strptime("16-Nov-2024 13:25", "%d-%b-%Y %H:%M")
    chat_id = "12345"

    # Replace fetch_personal_expenses with a direct DB query
    # def fetch_personal_expenses(chat_id):
    #     record = helper.get_expenses_collection().find_one({"chatid": chat_id})
    #     return record if record else {}

    # user_expenses = fetch_personal_expenses(chat_id)
    expenses = report.fetch_personal_expenses_for_period(chat_id, start_date)

    assert len(expenses) == 1
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["amount"] == 50.0


@patch('src.helper.get_group_expenses_file')
@patch('src.helper.fetch_personal_expenses')
def test_fetch_group_expenses_for_period(mock_fetch_personal_expenses, mock_get_group_expenses_file):
    """
    Test the fetch_group_expenses_for_period function with updated format.
    """
    # Mock personal expenses to return group expense IDs
    mock_fetch_personal_expenses.side_effect = lambda chat_id: (
        {"group_expenses": ["55667430"]}
        if chat_id == "7121391035"
        else {}
    )

    # Mock group expenses with the updated format
    mock_get_group_expenses_file.return_value = {
        "55667430": {
            "total": 100,
            "category": "Food",
            "created_by": "7121391035",
            "members": {
                "7121391035": 33.33,
                "7121391036": 33.33
            },
            "created_at": "18-Nov-2024 20:07",
            "updated_at": None
        }
    }

    start_date = datetime.strptime("16-Nov-2024 13:25", "%d-%b-%Y %H:%M")

    expenses = report.fetch_group_expenses_for_period("7121391035", start_date)

    assert len(expenses) == 1
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["amount"] == 33.33


def test_generate_summary_report():
    report_text = report.generate_summary_report(
        "Weekly",
        150.0,
        {"Food": 100.0, "Travel": 50.0}
    )

    assert "*Total Spending:* $150.00" in report_text
    assert "- Food: $100.00" in report_text
    assert "- Travel: $50.00" in report_text


def test_detect_anomalies():
    anomalies = report.detect_anomalies(
        {"Food": 100.0, "Travel": 20.0},
        total_expenses=150.0
    )

    assert len(anomalies) == 1
    assert "High spending on Food" in anomalies[0]


def test_aggregate_expenses():
    """
    Test the aggregate_expenses function.
    """
    expenses = [
        {"category": "Food", "amount": 50.0},
        {"category": "Travel", "amount": 100.0},
        {"category": "Food", "amount": 25.0},
    ]

    total, category_totals = report.aggregate_expenses(expenses)

    assert total == 175.0
    assert category_totals["Food"] == 75.0
    assert category_totals["Travel"] == 100.0


def create_message(text: str):
    """
    Helper function to create a simulated Telegram message.

    Args:
        text (str): The message text to simulate.

    Returns:
        MagicMock: Simulated Telegram message object.
    """
    message = MagicMock()
    message.chat.id = "12345"
    message.json = {"text": text}
    message.text = text
    return message
