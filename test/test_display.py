from mock import patch
from telebot import types
from src import display

decision = ['Yes', 'No']


def create_message(text):
    """This is the create message function"""
    params = {'text': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


@patch('telebot.telebot')
def test_run(mock_telebot):
    """This is the test function for run"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    message = create_message("hello from test run!")
    display.run(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_date_selections(mock_telebot):
    """This is the test function for date selections"""
    message = create_message("hello from test run!")
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True

    display.date_selections(message, mock_value)
    assert mock_value.send_message.called
