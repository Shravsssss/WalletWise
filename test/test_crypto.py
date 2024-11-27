# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

# tests/test_crypto.py

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from telebot import types
from src.crypto import run, post_crypto_selection, post_amount_input, add_user_record, option
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            'src')))


class TestCrypto(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.bot = MagicMock()
        self.chat_id = "123456"
        self.mock_message = MagicMock()
        self.mock_message.chat.id = self.chat_id
        self.mock_message.text = None

        # Reset the global `option` dictionary
        global option
        option = {}

        # Set up mock database connection
        self.mock_db = MagicMock()
        self.mock_collection = MagicMock()
        self.mock_db.__getitem__.return_value = self.mock_collection

    @patch('src.crypto.get_database')
    def test_run_function(self, mock_get_database):
        """Test the initial crypto selection menu."""
        mock_get_database.return_value = self.mock_db

        with patch('src.helper.get_crypto_types', return_value=['BTC', 'ETH']):
            run(self.mock_message, self.bot)

        self.bot.reply_to.assert_called_once()
        self.assertEqual(self.bot.register_next_step_handler.call_count, 1)

    @patch('src.crypto.get_database')
    def test_post_crypto_selection_invalid(self, mock_get_database):
        """Test invalid cryptocurrency selection."""
        mock_get_database.return_value = self.mock_db

        with patch('src.helper.get_crypto_types', return_value=['BTC', 'ETH']):
            self.mock_message.text = 'INVALID_CRYPTO'

            post_crypto_selection(self.mock_message, self.bot)

            self.bot.send_message.assert_any_call(
                self.chat_id, 'Invalid', reply_markup=unittest.mock.ANY
            )
            self.assertNotIn(self.chat_id, option)

    @patch('src.helper.read_json', return_value={})
    @patch('src.helper.create_new_user_record', return_value={'personal_expenses': []})
    @patch('src.crypto.get_database')
    def test_add_user_record(self, mock_get_database, mock_create_record, mock_read_json):
        """Test adding user record."""
        mock_get_database.return_value = self.mock_db

        record = "2024-01-01 12:00:00, BTC, 100"
        result = add_user_record(self.chat_id, record)

        self.assertIn(self.chat_id, result)
        self.assertIn(record, result[self.chat_id]['personal_expenses'])


if __name__ == '__main__':
    unittest.main()
