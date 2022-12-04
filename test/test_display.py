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
def test_show_categories(mock_telebot):
    """This is the test function for show categories"""
    message = create_message("Yes")

    mock_value = mock_telebot.return_value
    mock_value.reply_to.return_value = True
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mock_value.reply_to.return_value = True
    display.helper.get_spend_categories.return_value = decision

    display.show_categories(message, mock_value)
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


# @patch('telebot.telebot')
# def test_run(mock_telebot, mocker):
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("hello from test run!")
#     display.run(message, mc)
#     assert mock_value.send_message.called


# @patch('telebot.telebot')
# def test_no_data_available(mock_telebot, mocker):
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("/spendings")
#     display.run(message, mc)
#     assert mock_value.send_message.called
#
#
# @patch('telebot.telebot')
# def test_invalid_format(mock_telebot, mocker):
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("luster")
#     try:
#         display.display_total(message, mc)
#         assert False
#     except Exception:
#         assert True
#
#
# @patch('telebot.telebot')
# def test_valid_format(mock_telebot, mocker):
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("Month")
#     try:
#         display.display_total(message, mc)
#         assert True
#     except Exception:
#         assert False
#
#
# @patch('telebot.telebot')
# def test_valid_format_day(mock_telebot, mocker):
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("Day")
#     try:
#         display.display_total(message, mc)
#         assert True
#     except Exception:
#         assert False
#
#
# @patch('telebot.telebot')
# def test_spending_run_working(mock_telebot, mocker):
#
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#    display.helper.get_user_history.return_value = MOCK_USER_DATA[
#        "894127939"
#    ]
#     display.helper.get_spend_display_options.return_value = [
#         "Day", "Month"]
#     display.helper.get_date_format.return_value = '%d-%b-%Y'
#     display.helper.get_month_format.return_value = '%b-%Y'
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("Day")
#     message.text = "Day"
#     display.run(message, mc)
#     # assert not mock_value.send_message.called
#
#
# @patch('telebot.telebot')
# def test_spending_display_working(mock_telebot, mocker):
#
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#     display.helper.get_user_history.return_value = MOCK_USER_DATA[
#         "894127939"
#     ]
#     display.helper.get_spend_display_options.return_value = [
#         "Day", "Month"]
#     display.helper.get_date_format.return_value = '%d-%b-%Y'
#     display.helper.get_month_format.return_value = '%b-%Y'
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("Day")
#     message.text = "Day"
#     display.display_total(message, mc)
#     # assert mock_value.send_message.called
#
#
# @patch('telebot.telebot')
# def test_spending_display_month(mock_telebot, mocker):
#
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#     display.helper.get_user_history.return_value = MOCK_USER_DATA[
#         "894127939"
#     ]
#     display.helper.get_spend_display_options.return_value = [
#         "Day", "Month"]
#     display.helper.get_date_format.return_value = '%d-%b-%Y'
#     display.helper.get_month_format.return_value = '%b-%Y'
#     mock_value = mock_telebot.return_value
#     mock_value.reply_to.return_value = True
#     message = create_message("Month")
#     message.text = "Month"
#     display.display_total(message, mc)
#     # assert mock_value.send_message.called
#
#
# def create_message(text):
#     params = {'messagebody': text}
#     chat = types.User(11, False, 'test')
#     return types.Message(894127939, None, None, chat, 'text', params, "")
#
#
# def test_read_json():
#     try:
#         if not os.path.exists('./test/dummy_expense_record.json'):
#             with open('./test/dummy_expense_record.json', 'w') as json_file:
#                 json_file.write('{}')
#             return json.dumps('{}')
#         elif os.stat('./test/dummy_expense_record.json').st_size != 0:
#             with open('./test/dummy_expense_record.json') as expense_record:
#                 expense_record_data = json.load(expense_record)
#             return expense_record_data
#
#     except FileNotFoundError:
#         print("---------NO RECORDS FOUND---------")
