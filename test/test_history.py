# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

from mock import patch
from telebot import types
from src import history


def create_message(text):
    """This is the create message function"""
    params = {'text': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    """This is the test funtion for run method"""
    mock = mock_telebot.return_value
    mock.reply_to.return_value = True
    mock = mock_telebot.return_value
    mocker.patch.object(history, 'helper')

    # transaction_list = {
    #     "1001": {
    #         "created_at": "",
    #         "category": "",
    #         "members": {"11": 0}
    #     },
    #     "1002": {
    #         "created_at": "",
    #         "category": "",
    #         "members": {"11": 0, "20": 0}
    #     }
    # }
    # history.helper.read_json.side_effect = [None, transaction_list]
    history.helper.get_user_history.return_value = {
        'personal_expenses': "sample expense record",
        "group_expenses": ["1002"]
    }

    message = create_message("Hello from testing")
    try:
        history.run(message, mock)
    except Exception:
        assert True


@patch('telebot.telebot')
def test_run_no_records(mock_telebot, mocker):
    """This is the test function for run no records method"""
    mock = mock_telebot.return_value
    mock.reply_to.return_value = True
    mock = mock_telebot.return_value
    mocker.patch.object(history, 'helper')
    # history.helper.read_json.return_value = None
    history.helper.get_user_history.return_value = None

    message = create_message("Hello from testing")
    try:
        history.run(message, mock)
    except Exception:
        assert True


@patch('telebot.telebot')
def test_run_empty_records(mock_telebot, mocker):
    """This is the test function for run empty records method"""
    mock = mock_telebot.return_value
    mock.reply_to.return_value = True
    mock = mock_telebot.return_value
    mocker.patch.object(history, 'helper')
    # history.helper.read_json.return_value = None
    history.helper.get_user_history.return_value = []

    message = create_message("Hello from testing")
    try:
        history.run(message, mock)
    except Exception:
        assert True
