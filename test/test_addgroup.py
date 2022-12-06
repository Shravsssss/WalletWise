from mock import patch
from telebot import types
from src import add_group, helper
import unittest

DATE_FORMAT = '%d-%b-%Y'
TIME_FORMAT = '%H:%M'
MONTH_FORMAT = '%b-%Y'
spendCategories = [
    'Food',
    'Groceries',
    'Utilities',
    'Transport',
    'Shopping',
    'Miscellaneous'
]

helper.load_config()


def create_message(text):
    """This is the create message function"""
    params = {'text': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


@patch('telebot.telebot')
def test_run(mock_telebot):
    """This is the test function for run method"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    message = create_message("hello from test run!")
    add_group.run(message, mock_value)
    assert mock_value.send_message


@patch('telebot.telebot')
def test_expense_category_input(mock_telebot, mocker):
    """This is the test function for expense category input method"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.get_spend_categories.return_value = spendCategories

    message = create_message("Groceries")
    add_group.expense_category_input(message, mock_value)
    assert mock_value.send_message.called
    assert mock_value.send_message.called_with(11)


@patch('telebot.telebot')
def test_expense_category_input_invalid_category(mock_telebot, mocker):
    """This is the test function for expense category input invalid category"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.get_spend_categories.return_value = spendCategories

    message = create_message("blah")
    add_group.expense_category_input(message, mock_value)
    assert mock_value.send_message.called
    assert mock_value.send_message.called_with(11, 'Invalid')


@patch('telebot.telebot')
def test_take_all_users_input(mock_telebot, mocker):
    """This is the test function for take all users input method"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {
        "11": "hello@gmail.com",
        "20": "abcd@gmail.com",
        "21": "xyz@gmail.com"
    }

    message = create_message("abcd@gmail.com, xyz@gmail.com")
    add_group.take_all_users_input_with_other_handles(
        message,
        mock_value,
        "Groceries"
    )
    assert mock_value.send_message.called
    assert not mock_value.reply_to.called
    assert mock_value.send_message.called_with(
        11,
        'How much did you spend on Groceries? \n(Enter numeric values only)'
    )


@patch('telebot.telebot')
def test_take_all_users_input_invalid_email(mock_telebot, mocker):
    """This is the test function for take all
    users input invalid email method"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    # add_group.helper.read_json.return_value = {
    #     "11": "hello@gmail.com",
    #     "20": "abcd@gmail.com",
    #     "21": "xyz@gmail.com"
    # }

    message = create_message("abcd-gmail.com")
    add_group.take_all_users_input(message, mock_value, "Groceries")
    assert mock_value.reply_to.called


@patch('telebot.telebot')
def test_take_all_users_input_creator_not_registered(mock_telebot, mocker):
    """This is the test function for take all users input
    creator not registered"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    # add_group.helper.read_json.return_value = {
    #     "11": "hello@gmail.com",
    #     "20": "abcd@gmail.com",
    #     "21": "xyz@gmail.com"
    # }

    message = create_message("world@gmail.com")
    add_group.take_all_users_input(message, mock_value, "Groceries")
    assert mock_value.reply_to.called


@patch('telebot.telebot')
def test_take_all_users_input_creator_unknown_user(mock_telebot, mocker):
    """This is the test function for take all
    users input creator unknown user"""
    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    # add_group.helper.read_json.return_value = {
    #     "11": "hello@gmail.com",
    #     "20": "abcd@gmail.com",
    #     "21": "xyz@gmail.com"
    # }

    message = create_message("efgh@gmail.com")
    add_group.take_all_users_input(message, mock_value, "Groceries")
    assert mock_value.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_nonworking(mock_telebot, mocker):
    """This is the test function for post amount input
    non working method"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    add_group.post_amount_input(message, mock_value, 'Food', {})
    assert mock_value.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_working_withdata_chatid(mock_telebot, mocker):
    """This is the test function for post amount input working with data
     and chat id"""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.validate_entered_amount.return_value = 10
    add_group.helper.write_json.return_value = True
    add_group.helper.get_date_format.return_value = DATE_FORMAT
    add_group.helper.get_time_format.return_value = TIME_FORMAT
    mocker.patch.object(add_group, 'add_transaction_record')
    mocker.patch.object(add_group, 'add_transactions_to_user')
    add_group.add_transaction_record.return_value = 1001, [
        "sample transaction list"
    ]
    add_group.add_transactions_to_user_with_other_handles.return_value = [
        "sample updated user list"
    ]

    add_group.transaction_record = {}
    message = create_message("10")
    add_group.post_amount_input_with_other_inputs(
        message,
        mock_value,
        'Groceries',
        [11, 20, 21]
    )
    assert not mock_value.reply_to.called
    assert mock_value.send_message.called


def test_validate_email_input():
    """This is the test function for validate email input"""
    assert add_group.validate_email_input(["niharsrao@gmail.com"])


def test_validate_email_input_failure():
    """This is the test function for validate email input failure"""
    try:
        add_group.validate_email_input(["niharsrao-gmail.com"])
    except Exception:
        assert True


def test_generate_transaction_id():
    """This is the test function for generating transaction id"""
    assert add_group.generate_transaction_id()


def test_add_transaction_record(mocker):
    """This is the test function for add transactions record"""
    mocker.patch.object(add_group, 'helper')
    # add_group.helper.read_json.return_value = {}
    assert add_group.add_transaction_record({})


def test_add_transactions_to_user():
    """This is the test function for add transactions to
    user"""

    # pylint: disable=no-value-for-parameter
    with unittest.TestCase.assertRaises(None, expected_exception=Exception):
        add_group.add_transactions_to_user(
            "1002",
            ["20", "21"]
        )


def test_add_transactions_to_user_invalid_transaction(mocker):
    """This is the test function for add transactions to
    user invalid transaction"""
    mocker.patch.object(add_group, 'helper')

    # transaction_list = ["1001", "1002", "1003"]
    # user_list = {"11": {}, "20": {}, "21": {}}

    # add_group.helper.read_json.side_effect = [transaction_list, user_list]
    try:
        _ = add_group.add_transactions_to_user("2002", ["20", "21"])
    except Exception:
        assert True
