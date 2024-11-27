# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

from unittest import mock
import pytest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime
from src import export_expenses


# from unittest.mock import patch, MagicMock, mock_open
# from datetime import datetime
# import src.export_expenses as export_expenses

@patch("builtins.open", new_callable=mock_open)
@patch("src.export_expenses.fetch_personal_expenses_for_date_range")
@patch("src.export_expenses.fetch_group_expenses_for_date_range")
@patch("os.remove")
@patch("src.export_expenses.generate_csv")
@patch("src.export_expenses.generate_pdf")
def test_process_export_request_with_csv(
    mock_generate_pdf, mock_generate_csv, mock_os_remove,
    mock_fetch_group_expenses, mock_fetch_personal_expenses, mock_open_file
):
    """
    Test process_export_request with CSV format.
    """
    # Mock fetch expenses functions
    mock_fetch_personal_expenses.return_value = [
        {"type": "Personal", "date": "2024-11-18 10:00",
            "category": "Food", "amount": "50"}
    ]
    mock_fetch_group_expenses.return_value = [
        {"type": "Group", "date": "2024-11-18 20:00",
            "category": "Dinner", "amount": "30"}
    ]

    # Mock CSV generation
    mock_generate_csv.return_value = "/tmp/test.csv"

    # Set export preferences
    export_expenses.user_export_preferences["12345"] = {
        "format": "CSV",
        "start_date": datetime(2024, 11, 16)
    }

    # Mock bot and message
    bot = MagicMock()
    message = MagicMock()
    message.chat.id = "12345"
    message.text = "2024-11-19"

    # Call the function
    export_expenses.process_export_request(message, bot)

    # Assertions
    mock_generate_csv.assert_called_once()
    bot.send_document.assert_called_once_with(
        "12345", mock_open_file.return_value)
    mock_os_remove.assert_called_once_with("/tmp/test.csv")


@patch("builtins.open", new_callable=mock_open)
@patch("src.export_expenses.fetch_personal_expenses_for_date_range")
@patch("src.export_expenses.fetch_group_expenses_for_date_range")
@patch("os.remove")
@patch("src.export_expenses.generate_csv")
@patch("src.export_expenses.generate_pdf")
def test_process_export_request_with_pdf(
    mock_generate_pdf, mock_generate_csv, mock_os_remove,
    mock_fetch_group_expenses, mock_fetch_personal_expenses, mock_open_file
):
    """
    Test process_export_request with PDF format.
    """
    # Mock fetch expenses functions
    mock_fetch_personal_expenses.return_value = [
        {"type": "Personal", "date": "2024-11-18 10:00",
            "category": "Food", "amount": "50"}
    ]
    mock_fetch_group_expenses.return_value = [
        {"type": "Group", "date": "2024-11-18 20:00",
            "category": "Dinner", "amount": "30"}
    ]

    # Mock PDF generation
    mock_generate_pdf.return_value = "/tmp/test.pdf"

    # Set export preferences
    export_expenses.user_export_preferences["12345"] = {
        "format": "PDF",
        "start_date": datetime(2024, 11, 16)
    }

    # Mock bot and message
    bot = MagicMock()
    message = MagicMock()
    message.chat.id = "12345"
    message.text = "2024-11-19"

    # Call the function
    export_expenses.process_export_request(message, bot)

    # Assertions
    mock_generate_pdf.assert_called_once()
    bot.send_document.assert_called_once_with(
        "12345", mock_open_file.return_value)
    mock_os_remove.assert_called_once_with("/tmp/test.pdf")


@patch("src.export_expenses.fetch_personal_expenses")
def test_fetch_personal_expenses_for_date_range(mock_fetch_personal_expenses):
    """
    Test fetch_personal_expenses_for_date_range.
    """
    # Mock personal expenses
    mock_fetch_personal_expenses.return_value = {
        "personal_expenses": ["19-Nov-2024 10:00, Food, 50"]
    }

    start_date = datetime(2024, 11, 16)
    end_date = datetime(2024, 11, 20)

    expenses = export_expenses.fetch_personal_expenses_for_date_range(
        "12345", start_date, end_date
    )

    # Assertions
    assert len(expenses) == 1
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["amount"] == "50"
    assert expenses[0]["date"] == "19-Nov-2024 10:00"


@patch("src.export_expenses.get_group_expenses_file")
@patch("src.export_expenses.fetch_personal_expenses")
def test_fetch_group_expenses_for_date_range(
    mock_fetch_personal_expenses, mock_get_group_expenses_file
):
    """
    Test fetch_group_expenses_for_date_range.
    """
    # Mock personal and group expenses
    mock_fetch_personal_expenses.return_value = {"group_expenses": ["group1"]}
    mock_get_group_expenses_file.return_value = {
        "group1": {
            "created_at": "18-Nov-2024 10:00",
            "category": "Dinner",
            "members": {"12345": 30}
        }
    }

    start_date = datetime(2024, 11, 16)
    end_date = datetime(2024, 11, 20)

    expenses = export_expenses.fetch_group_expenses_for_date_range(
        "12345", start_date, end_date
    )

    # Assertions
    assert len(expenses) == 1
    assert expenses[0]["category"] == "Dinner"
    assert expenses[0]["amount"] == "30.00"
    assert expenses[0]["date"] == "18-Nov-2024 10:00"
