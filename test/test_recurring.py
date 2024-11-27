# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

from unittest.mock import patch
from telebot import types
from src import recurring_expenses, helper, goals
from mock import ANY
from datetime import datetime


@patch('telebot.telebot')
def test_run_with_setgoal(mock_telebot):
    """
    Test the run function with the /setrecurringexpense command.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/setrecurringexpense")
    recurring_expenses.run(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_run_with_invalid_command(mock_telebot):
    """
    Test the run function with an invalid command.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/invalidcommand")
    recurring_expenses.run(message, mock_value)
    assert not mock_value.send_message.called


@patch('telebot.telebot')
def test_prompt_set_recurring_expense(mock_telebot):
    """
    Test the prompt_set_recurring_expense function.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/setrecurringexpense")
    recurring_expenses.prompt_set_recurring_expenses(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_set_recurring_expense_valid(mock_telebot, mocker):
    """
    Test the process_set_recurring_expense function with valid input.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.list_recurring_expenses')
    recurring_expense_collection_mock = helper.list_recurring_expenses.return_value
    recurring_expense_collection_mock.find_one.return_value = {
        "chatid": "79860", "recurring_expenses": {}}

    message = create_message("Rent 700 monthly")
    recurring_expenses.process_set_recurring_expenses(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_set_recurring_expense_invalid(mock_telebot):
    """
    Test the process_set_recurring_expense function with invalid input.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("Invalid input")
    recurring_expenses.process_set_recurring_expenses(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_list_recurring_no_recurring(mock_telebot, mocker):
    """
    Test the test_list_recurring function when no recurring expenses are set.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.list_recurring_expenses')
    recurring_collection_mock = helper.list_recurring_expenses.return_value
    recurring_collection_mock.find_one.return_value = None

    message = create_message("/listrecurringexpenses")
    recurring_expenses.list_recurring_expenses(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_list_recurring_with_recurring(mock_telebot, mocker):
    """
    Test the test_list_recurring function with recurring expenses.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.list_recurring_expenses')
    recurring_collection_mock = helper.list_recurring_expenses.return_value
    recurring_collection_mock.find_one.return_value = {
        "chatid": "12345",
        "goals": {"Rent": {"amount": 700, "interval": "monthly"}}
    }

    message = create_message("/listrecurringexpenses")
    recurring_expenses.list_recurring_expenses(message, mock_value)
    assert mock_value.send_message.called


def create_message(text: str) -> types.Message:
    """
    Helper function to create a simulated Telegram message.

    Args:
        text (str): The message text to simulate.

    Returns:
        types.Message: Simulated Telegram message object.
    """
    user = types.User(id=79860, is_bot=False, first_name='test_user')
    chat = types.Chat(id=79860, type='private')
    return types.Message(
        message_id=1,
        from_user=user,
        date=datetime.now(),
        chat=chat,
        content_type='text',
        options={},
        json_string={'text': text}
    )
