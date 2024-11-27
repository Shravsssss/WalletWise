import unittest
from unittest.mock import Mock, patch
from src.helper import set_config, get_database
from src.currencyConvert import (
    start_currency_convert,
    handle_currency_selection,
    handle_amount_input,
    convert_currency,
    user_data
)

class TestCurrencyConversionBot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up mock database before running tests."""
        set_config()  # Ensure the default settings are set for tests.
        cls.mock_db = get_database()

        # Insert mock data into the database
        cls.mock_db["USER_EXPENSES"].insert_one({
            "chatid": "12345",
            "input_currency": "USD",
            "output_currency": None,
            "amount": None
        })

    @classmethod
    def tearDownClass(cls):
        """Clean up the mock database after tests."""
        cls.mock_db["USER_EXPENSES"].delete_many({"chatid": "12345"})

    def setUp(self):
        # Initialize user_data for testing
        user_data[12345] = {'input_currency': 'USD', 'output_currency': None, 'amount': None}

    def test_default_input_currency_usd(self):
        bot = Mock()
        message = Mock()
        message.chat.id = 12345
        start_currency_convert(bot, message)
        self.assertEqual(user_data[12345]['input_currency'], 'USD')

    def test_default_output_currency_none(self):
        bot = Mock()
        message = Mock()
        message.chat.id = 12345
        start_currency_convert(bot, message)
        self.assertIsNone(user_data[12345]['output_currency'])

    def test_currency_selection(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        for currency in ['EUR', 'INR', 'GBP', 'JPY', 'RUB', 'AUD', 'NZD', 'KWD', 'BHD', 'OMR']:
            with self.subTest(currency=currency):
                call.data = f'currency_{currency}'
                handle_currency_selection(bot, call)
                self.assertEqual(user_data[12345]['output_currency'], currency)

    @patch('src.helper.validate_entered_amount', return_value=100)
    def test_valid_amount_input_100(self, mock_validate_amount):
        bot = Mock()
        message = Mock()
        message.chat.id = 12345
        message.text = "100"

        # Set the output_currency to ensure the logic proceeds
        user_data[12345]['output_currency'] = 'EUR'

        handle_amount_input(bot, message)
        self.assertEqual(user_data[12345]['amount'], 100.0)

    @patch('src.helper.validate_entered_amount', return_value=50.5)
    def test_valid_amount_input_50_5(self, mock_validate_amount):
        bot = Mock()
        message = Mock()
        message.chat.id = 12345
        message.text = "50.5"

        # Set the output_currency to ensure the logic proceeds
        user_data[12345]['output_currency'] = 'INR'

        handle_amount_input(bot, message)
        self.assertEqual(user_data[12345]['amount'], 50.5)

    @patch('requests.get')
    def test_convert_currency_small_amount(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"EUR": 0.85}
        }
        result = convert_currency('USD', 'EUR', 0.01)
        self.assertAlmostEqual(result, 0.0085, places=4)

    @patch('requests.get')
    def test_convert_currency_large_amount(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"INR": 75.0}
        }
        result = convert_currency('USD', 'INR', 1000000)
        self.assertEqual(result, 75000000.0)

    @patch('requests.get')
    def test_convert_currency_rate(self, mock_get):
        conversion_rates = {
            "EUR": 0.85, "GBP": 0.75, "JPY": 110, "INR": 75
        }
        for currency, rate in conversion_rates.items():
            with self.subTest(currency=currency):
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = {
                    "result": "success",
                    "conversion_rates": {currency: rate}
                }
                result = convert_currency('USD', currency, 100)
                self.assertEqual(result, 100 * rate)

if __name__ == '__main__':
    unittest.main()
