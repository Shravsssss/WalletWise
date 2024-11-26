# tests/test_crypto.py

from src.crypto import run, post_crypto_selection, post_amount_input, add_user_record, option
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the src directory to the Python path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'src')))


class TestCrypto(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.chat_id = "123456"
        self.mock_message = Mock()
        self.mock_message.chat.id = self.chat_id
        # Reset the option dictionary before each test
        global option
        option = {}

    @patch('src.helper.get_crypto_types')
    def test_run_function(self, mock_get_crypto_types):
        """Test the initial crypto selection menu"""
        mock_get_crypto_types.return_value = ['BTC', 'ETH']

        run(self.mock_message, self.bot)

        self.bot.reply_to.assert_called_once()
        self.assertEqual(self.bot.register_next_step_handler.call_count, 1)

    @patch('src.helper.get_crypto_types')
    def test_post_crypto_selection_valid(self, mock_get_crypto_types):
        """Test valid cryptocurrency selection"""
        mock_get_crypto_types.return_value = ['BTC', 'ETH']
        self.mock_message.text = 'BTC'

        post_crypto_selection(self.mock_message, self.bot)

        self.assertEqual(option[self.chat_id], 'BTC')
        self.assertEqual(self.bot.send_message.call_count, 1)

    @patch('src.helper.get_crypto_types')
    def test_post_crypto_selection_invalid(self, mock_get_crypto_types):
        """Test invalid cryptocurrency selection"""
        mock_get_crypto_types.return_value = ['BTC', 'ETH']
        self.mock_message.text = 'INVALID_CRYPTO'

        post_crypto_selection(self.mock_message, self.bot)

        self.bot.send_message.assert_called()
        self.assertNotIn(self.chat_id, option)

    @patch('src.helper.validate_entered_amount')
    @patch('src.crypto.get_database')
    def test_post_amount_input_valid(self, mock_db, mock_validate):
        """Test valid amount input"""
        mock_validate.return_value = 100.0
        mock_collection = Mock()
        mock_db.return_value = {'USER_EXPENSES': mock_collection}
        mock_collection.find.return_value = []

        self.mock_message.text = "100"
        option[self.chat_id] = 'BTC'

        post_amount_input(self.mock_message, self.bot, 'BTC')

        self.assertEqual(mock_collection.insert_one.call_count, 1)
        self.bot.send_message.assert_called()

    @patch('src.helper.read_json')
    @patch('src.helper.create_new_user_record')
    def test_add_user_record(self, mock_create_record, mock_read_json):
        """Test adding user record"""
        mock_read_json.return_value = {}
        mock_create_record.return_value = {'personal_expenses': []}

        record = "2024-01-01 12:00:00, BTC, 100"
        result = add_user_record(self.chat_id, record)

        self.assertIn(self.chat_id, result)
        self.assertIn(record, result[self.chat_id]['personal_expenses'])


if __name__ == '__main__':
    unittest.main()
