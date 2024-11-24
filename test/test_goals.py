from unittest.mock import patch
from telebot import types
from src import goals, helper
from mock import ANY
from datetime import datetime


@patch('telebot.telebot')
def test_run_with_setgoal(mock_telebot):
    """
    Test the run function with the /setgoal command.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/setgoal")
    goals.run(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_run_with_checkgoals(mock_telebot):
    """
    Test the run function with the /checkgoals command.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/checkgoals")
    goals.run(message, mock_value)
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
    goals.run(message, mock_value)
    assert not mock_value.send_message.called


@patch('telebot.telebot')
def test_prompt_set_goal(mock_telebot):
    """
    Test the prompt_set_goal function.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/setgoal")
    goals.prompt_set_goal(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_set_goal_valid(mock_telebot, mocker):
    """
    Test the process_set_goal function with valid input.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.get_goals_collection')
    goals_collection_mock = helper.get_goals_collection.return_value
    goals_collection_mock.find_one.return_value = {
        "chatid": "12345", "goals": {}}

    message = create_message("Trip 500")
    goals.process_set_goal(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_set_goal_invalid(mock_telebot):
    """
    Test the process_set_goal function with invalid input.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("Invalid input")
    goals.process_set_goal(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_show_goals_status_no_goals(mock_telebot, mocker):
    """
    Test the show_goals_status function when no goals are set.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.get_goals_collection')
    goals_collection_mock = helper.get_goals_collection.return_value
    goals_collection_mock.find_one.return_value = None

    message = create_message("/checkgoals")
    goals.show_goals_status(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_show_goals_status_with_goals(mock_telebot, mocker):
    """
    Test the show_goals_status function with existing goals.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.get_goals_collection')
    goals_collection_mock = helper.get_goals_collection.return_value
    goals_collection_mock.find_one.return_value = {
        "chatid": "12345",
        "goals": {"Trip": {"target": 500, "saved": 200}}
    }

    message = create_message("/checkgoals")
    goals.show_goals_status(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_prompt_add_savings(mock_telebot):
    """
    Test the prompt_add_savings function.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("/addsavings")
    goals.prompt_add_savings(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_add_savings_valid(mock_telebot, mocker):
    """
    Test the process_add_savings function with valid input.

    Args:
        mock_telebot: Mocked telebot instance.
        mocker: Pytest mocker fixture.
    """
    mock_value = mock_telebot.return_value
    mocker.patch('src.helper.get_goals_collection')
    goals_collection_mock = helper.get_goals_collection.return_value
    goals_collection_mock.find_one.return_value = {
        "chatid": "12345",
        "goals": {"Trip": {"target": 500, "saved": 200}}
    }

    message = create_message("Trip 50")
    goals.process_add_savings(message, mock_value)
    assert mock_value.send_message.called


@patch('telebot.telebot')
def test_process_add_savings_invalid(mock_telebot):
    """
    Test the process_add_savings function with invalid input.

    Args:
        mock_telebot: Mocked telebot instance.
    """
    mock_value = mock_telebot.return_value
    message = create_message("Invalid input")
    goals.process_add_savings(message, mock_value)
    assert mock_value.send_message.called


def create_message(text: str) -> types.Message:
    """
    Helper function to create a simulated Telegram message.

    Args:
        text (str): The message text to simulate.

    Returns:
        types.Message: Simulated Telegram message object.
    """
    user = types.User(id=12345, is_bot=False, first_name='test_user')
    chat = types.Chat(id=12345, type='private')
    return types.Message(
        message_id=1,
        from_user=user,
        date=datetime.now(),
        chat=chat,
        content_type='text',
        options={},
        json_string={'text': text}
    )
