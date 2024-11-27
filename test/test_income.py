# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

from unittest.mock import patch
from telebot import types
from src import goals, helper, income
from mock import ANY
from datetime import datetime


@patch('telebot.telebot')
def test_run_with_setincome(mock_telebot):
    """
    Test the run function with the /setincom command.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/setincome")
    income.run(message, mock_value)
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
    income.run(message, mock_value)
    assert not mock_value.send_message.called


@patch('telebot.telebot')
def test_prompt_set_income(mock_telebot):
    """
    Test the prompt_set_income function.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/setincome")
    income.prompt_set_income(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_set_income_valid(mock_telebot, mocker):
    """
    Test the process_set_income function with valid input.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.list_income_sources')
    income_collection_mock = helper.list_income_sources.return_value
    income_collection_mock.find_one.return_value = {
        "chatid": "79860", "income_sources": {}}

    message = create_message("900 NCSU")
    income.process_set_income(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_set_income_invalid(mock_telebot):
    """
    Test the process_set_income function with invalid input.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("Invalid input")
    income.prompt_set_income(message, mock_value)
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
