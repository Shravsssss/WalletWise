from src.plots import (
    label_amount,
    get_amount_df,
    check_data_present,
    overall_plot,
    pie_plot,
    box_plot,
    create_time_series_plot,
    predict_expenses
)
import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import sys
import os

from datetime import datetime, timedelta
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'src')))

# Use correct path import
# Add src directory to path

# from src.plots import (
#     label_amount,
#     get_amount_df,
#     check_data_present,
#     overall_plot,
#     pie_plot,
#     box_plot,
#     create_time_series_plot,
#     predict_expenses
# )


class TestPlots(unittest.TestCase):
    def setUp(self):
        self.chat_id = "123456"
        self.start_date = datetime.now() - timedelta(days=30)
        self.end_date = datetime.now()

        # Mock expense data
        self.mock_expense_data = {
            'personal_expenses': [
                '01-Jan-2024 10:00, food, 100',
                '02-Jan-2024 11:00, transport, 50'
            ],
            'group_expenses': []
        }

    @patch('matplotlib.pyplot')
    def test_label_amount(self, mock_plt):
        """Test label_amount function"""
        y_values = [100, 200, 300]
        label_amount(y_values)
        self.assertEqual(mock_plt.text.call_count, len(y_values))

    @patch('src.helper.get_user_history')
    def test_get_amount_df(self, mock_get_history):
        """Test get_amount_df function"""
        mock_get_history.return_value = self.mock_expense_data

        df = get_amount_df(
            self.chat_id,
            2,
            self.mock_expense_data,
            {},
            "overall"
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertTrue(all(col in df.columns for col in [
                        'Date', 'Category', 'Amount']))

    def test_check_data_present(self):
        """Test check_data_present function"""
        with patch('src.helper.get_user_history') as mock_get_history:
            # Test no data
            mock_get_history.return_value = None
            self.assertEqual(check_data_present(self.chat_id, {}), 1)

            # Test only personal expenses
            mock_get_history.return_value = {
                'personal_expenses': ['some data'],
                'group_expenses': []
            }
            self.assertEqual(check_data_present(self.chat_id, {}), 2)

    @patch('matplotlib.pyplot')
    @patch('src.helper.get_user_history')
    def test_overall_plot(self, mock_get_history, mock_plt):
        """Test overall_plot function"""
        mock_get_history.return_value = self.mock_expense_data

        result = overall_plot(
            self.chat_id,
            self.start_date,
            self.end_date,
            {},
            {}
        )

        self.assertEqual(result, 7)  # Success case
        mock_plt.savefig.assert_called_once()

    @patch('src.plots.get_database')
    def test_create_time_series_plot(self, mock_db):
        """Test time series plot creation"""
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {
            'chatid': self.chat_id,
            'personal_expenses': self.mock_expense_data['personal_expenses']
        }
        mock_db.return_value = {'USER_EXPENSES': mock_collection}

        with patch('matplotlib.pyplot') as mock_plt:
            plot_path = create_time_series_plot(self.chat_id)

            self.assertIsNotNone(plot_path)
            self.assertTrue(plot_path.endswith('.png'))
            mock_plt.savefig.assert_called_once()

    @patch('src.plots.get_database')
    def test_predict_expenses(self, mock_db):
        """Test expense prediction"""
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {
            'chatid': self.chat_id,
            'personal_expenses': self.mock_expense_data['personal_expenses']
        }
        mock_db.return_value = {'USER_EXPENSES': mock_collection}

        with patch('matplotlib.pyplot') as mock_plt:
            plot_path, summary = predict_expenses(self.chat_id)

            self.assertIsNotNone(plot_path)
            self.assertIsInstance(summary, str)
            self.assertTrue('Expense Predictions Summary' in summary)
            mock_plt.savefig.assert_called_once()

    def test_predict_expenses_no_data(self):
        """Test prediction with no data"""
        with patch('src.plots.get_database') as mock_db:
            mock_collection = MagicMock()
            mock_collection.find_one.return_value = None
            mock_db.return_value = {'USER_EXPENSES': mock_collection}

            with self.assertRaises(Exception) as context:
                predict_expenses(self.chat_id)

            self.assertTrue('No expense data found' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
