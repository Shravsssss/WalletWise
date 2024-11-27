# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

from mock import patch
from telebot import types
from src import profile

DATE_FORMAT = '%d-%b-%Y'
TIME_FORMAT = '%H:%M'
MONTH_FORMAT = '%b-%Y'


def create_message(text):
    """This is the funtion to create message"""
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


@patch('telebot.telebot')
def test_run(mock_telebot):
    """This is the test funtion to run"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    message = create_message("hello from test run!")
    profile.run(message, mock_value)


@patch('telebot.telebot')
def test_post_email_input(mock_telebot):
    """This is the test function to post email input"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    profile.add_group.validate_email_input.return_value = True
    # profile.helper.read_json.return_value = {}
    message = create_message("pbrr@gmail.com")
    message.text = "pbrr@gmail.com"
    # profile.helper.write_json.return_value = True
    profile.post_email_input(message, mock_value)

    # call exceptions
    message.text = None
    profile.post_email_input(message, mock_value)
