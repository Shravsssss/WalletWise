import os
import json
from mock.mock import patch
from telebot import types
from src import add, helper
from mock import ANY


DATE_FORMAT = '%d-%b-%Y'
TIME_FORMAT = '%H:%M'
MONTH_FORMAT = '%b-%Y'
helper.load_config()


@patch('telebot.telebot')
def test_run(mock_telebot):
    """This is the test function for run method"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    message = create_message("hello from test run!")
    add.run(message, mock_value)
    assert mock_value.reply_to.called


@patch('telebot.telebot')
def test_post_category_selection_working(mock_telebot):
    """This is the test function for post
    category selection working method"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True

    message = create_message("hello from testing!")
    add.post_category_selection(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_post_category_selection_no_matching_category(mock_telebot, mocker):
    """This is the test function for post category
    selection with no matching category method"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = []
    mock_value.reply_to.return_value = True

    mocker.patch.object(add, 'helper')
    add.helper.get_spend_categories.return_value = None

    message = create_message("hello from testing!")
    add.post_category_selection(message, mock_value)
    assert mock_value.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_working(mock_telebot):
    """This is the test function for post amount input working"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True

    message = create_message("hello from testing!")
    add.post_category_selection(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_post_amount_input_working_withdata(mock_telebot, mocker):
    """This is the test function for post amount input
    working with data method"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mocker.patch.object(add, 'helper')
    add.helper.validate_entered_amount.return_value = 10
    # add.helper.write_json.return_value = True
    add.helper.get_date_format.return_value = DATE_FORMAT
    add.helper.get_time_format.return_value = TIME_FORMAT

    mocker.patch.object(add, 'option')
    add.option.return_value = {11, "here"}

    message = create_message("hello from testing!")
    add.post_amount_input(message, mock_value, 'Food')
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_post_amount_input_nonworking(mock_telebot, mocker):
    """This is the testing funciton for post amount input nonworking method"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add, 'helper')
    add.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    add.post_amount_input(message, mock_value, 'Food')
    assert mock_value.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_working_withdata_chatid(mock_telebot, mocker):
    """This is the test function for post amount input working
    with data and chat id method"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mocker.patch.object(add, 'helper')
    add.helper.validate_entered_amount.return_value = 10
    # add.helper.write_json.return_value = True
    add.helper.get_date_format.return_value = DATE_FORMAT
    add.helper.get_time_format.return_value = TIME_FORMAT

    mocker.patch.object(add, 'option')
    add.option = {11, "here"}
    test_option = {}
    test_option[11] = "here"
    add.option = test_option

    message = create_message("hello from testing!")
    add.post_amount_input(message, mock_value, 'Food')
    assert mock_value.send_message.called
    assert mock_value.send_message.called_with(11, ANY)


# def test_add_user_record_nonworking(mocker):
#     """This is the test function for add user record non working method"""
#     mocker.patch.object(add, 'helper')
#     add.helper.read_json.return_value = {}
#     addeduserrecord = add.add_user_record(1, "record : test")
#     assert addeduserrecord 


# def test_add_user_record_working(mocker):
#     """This is the test function for add user record working function"""
#     mock_user_data = test_read_json()
#     mocker.patch.object(add, 'helper')
#     add.helper.read_json.return_value = mock_user_data
#     addeduserrecord = add.add_user_record(1, "record : test")
#     if len(mock_user_data) + 1 == len(addeduserrecord):
#         assert True


def create_message(text):
    """This is the create message function"""
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")
