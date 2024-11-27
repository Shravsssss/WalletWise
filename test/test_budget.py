from unittest.mock import patch
from telebot import types
from src import budget, helper
from mock import ANY

DATE_FORMAT = '%d-%b-%Y'
TIME_FORMAT = '%H:%M'
MONTH_FORMAT = '%b-%Y'
helper.load_config()


@patch('telebot.telebot')
def test_run_with_setbudget(mock_telebot):
    """Test the run function with the /setbudget command."""
    mock_value = mock_telebot.return_value
    message = create_message("/setbudget")
    budget.run(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_run_with_checkbudget(mock_telebot):
    """Test the run function with the /checkbudget command."""
    mock_value = mock_telebot.return_value
    message = create_message("/checkbudget")
    budget.run(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_run_with_invalid_command(mock_telebot):
    """Test the run function with an invalid command."""
    mock_value = mock_telebot.return_value
    message = create_message("/invalidcommand")
    budget.run(message, mock_value)
    assert not mock_value.send_message.called


@patch('telebot.telebot')
def test_prompt_set_budget(mock_telebot):
    """Test the prompt_set_budget function."""
    mock_value = mock_telebot.return_value
    message = create_message("/setbudget")
    budget.prompt_set_budget(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_budget_input_valid(mock_telebot, mocker):
    """Test the process_budget_input function with valid input."""
    mock_value = mock_telebot.return_value
    mocker.patch.object(budget, 'helper')
    budget.helper.parse_budget_input.return_value = ('Food', 200)
    budget.helper.save_budget_for_category.return_value = True

    message = create_message("Food 200")
    budget.process_budget_input(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_budget_input_invalid(mock_telebot, mocker):
    """Test the process_budget_input function with invalid input."""
    mock_value = mock_telebot.return_value
    mock_value.send_message.return_value = True
    mocker.patch.object(budget, 'helper')
    budget.helper.parse_budget_input.side_effect = ValueError("Invalid format")

    message = create_message("Invalid input")
    budget.process_budget_input(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_show_budget_status_budget_not_set(mock_telebot, mocker):
    """Test the show_budget_status function when the budget is not set."""
    mock_value = mock_telebot.return_value
    mocker.patch.object(helper, 'is_budget_set', return_value=False)
    mocker.patch.object(helper, 'has_expenses_this_month', return_value=True)

    message = create_message("/checkbudget")
    budget.show_budget_status(message, mock_value)

    # Check that send_message was NOT called
    assert not mock_value.send_message.called


@patch('telebot.telebot')
def test_show_budget_status_no_expenses(mock_telebot, mocker):
    """Test the show_budget_status function when there are no expenses."""
    mock_value = mock_telebot.return_value
    mocker.patch.object(helper, 'is_budget_set', return_value=True)
    mocker.patch.object(helper, 'has_expenses_this_month', return_value=False)

    message = create_message("/checkbudget")
    budget.show_budget_status(message, mock_value)

    # Check that send_message was NOT called
    assert not mock_value.send_message.called


@patch('telebot.telebot')
def test_show_budget_status_valid(mock_telebot, mocker):
    """Test the show_budget_status function with valid data."""
    mock_value = mock_telebot.return_value
    mocker.patch.object(budget, 'helper')
    budget.helper.is_budget_set.return_value = True
    budget.helper.has_expenses_this_month.return_value = True
    budget.helper.fetch_user_budget.return_value = {"budgets": {"Food": 200}}
    budget.helper.fetch_personal_expenses.return_value = {
        "personal_expenses": [{"category": "Food", "amount": 150}]}
    budget.helper.calculate_monthly_expenses.return_value = {"Food": 150}
    budget.helper.build_budget_report.return_value = "Budget report"

    message = create_message("/checkbudget")
    budget.show_budget_status(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_show_budget_status_with_exception(mock_telebot, mocker):
    """Test the show_budget_status function with an exception."""
    mock_value = mock_telebot.return_value
    mocker.patch.object(helper, 'fetch_user_budget',
                        side_effect=Exception("Unexpected error"))
    mocker.patch.object(helper, 'log_and_reply_error')

    message = create_message("/checkbudget")
    budget.show_budget_status(message, mock_value)

    # Ensure error logging was called
    helper.log_and_reply_error.assert_called_once()
    # Ensure send_message was NOT called
    assert not mock_value.send_message.called


def create_message(text: str) -> types.Message:
    """
    Helper function to create a simulated Telegram message.

    Args:
        text (str): The message text to simulate.

    Returns:
        types.Message: Simulated Telegram message object.
    """
    user = types.User(id=7121391035, is_bot=False, first_name='test')
    chat = types.Chat(id=7121391035, type='private')
    return types.Message(
        message_id=1,
        from_user=user,
        date=None,
        chat=chat,
        content_type='text',
        options={},
        json_string={'text': text}
    )
