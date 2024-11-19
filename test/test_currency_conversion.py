from src.currencyConvert import start_currency_convert, handle_currency_selection, handle_amount_input, convert_currency, user_data
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Insert the path to the 'src' folder
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../src')))


class TestCurrencyConversionBot(unittest.TestCase):

    def setUp(self):
        # Initialize user_data[12345] to avoid KeyError
        user_data[12345] = {
            'input_currency': 'USD',
            'output_currency': None,
            'amount': None}

    def test_currency_selection_eur(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_EUR'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'EUR')

    def test_currency_selection_inr(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_INR'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'INR')

    def test_currency_selection_gbp(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_GBP'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'GBP')

    def test_currency_selection_jpy(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_JPY'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'JPY')

    def test_currency_selection_rub(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_RUB'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'RUB')

    def test_currency_selection_aud(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_AUD'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'AUD')

    def test_currency_selection_nzd(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_NZD'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'NZD')

    def test_currency_selection_kwd(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_KWD'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'KWD')

    def test_currency_selection_bhd(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_BHD'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'BHD')

    def test_currency_selection_omr(self):
        bot = Mock()
        call = Mock()
        call.message.chat.id = 12345
        call.data = 'currency_OMR'
        handle_currency_selection(bot, call)
        self.assertEqual(user_data[12345]['output_currency'], 'OMR')

    @patch('requests.get')
    def test_convert_currency_medium_amount(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"GBP": 0.75}
        }
        result = convert_currency('USD', 'GBP', 500)
        self.assertEqual(result, 500 * 0.75)

    @patch('requests.get')
    def test_convert_currency_to_jpy(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"JPY": 110}
        }
        result = convert_currency('USD', 'JPY', 100)
        self.assertEqual(result, 100 * 110)

    @patch('requests.get')
    def test_convert_currency_to_eur(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"EUR": 0.85}
        }
        result = convert_currency('USD', 'EUR', 100)
        self.assertEqual(result, 100 * 0.85)

    @patch('requests.get')
    def test_convert_currency_to_inr(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"INR": 75.0}
        }
        result = convert_currency('USD', 'INR', 100)
        self.assertEqual(result, 100 * 75.0)

    @patch('requests.get')
    def test_convert_currency_to_gbp(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"GBP": 0.75}
        }
        result = convert_currency('USD', 'GBP', 100)
        self.assertEqual(result, 100 * 0.75)

    @patch('requests.get')
    def test_convert_currency_to_jpy(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"JPY": 110}
        }
        result = convert_currency('USD', 'JPY', 100)
        self.assertEqual(result, 100 * 110)

    @patch('requests.get')
    def test_convert_currency_to_rub(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"RUB": 74.0}
        }
        result = convert_currency('USD', 'RUB', 100)
        self.assertEqual(result, 100 * 74.0)

    @patch('requests.get')
    def test_convert_currency_to_aud(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"AUD": 1.3}
        }
        result = convert_currency('USD', 'AUD', 100)
        self.assertEqual(result, 100 * 1.3)

    @patch('requests.get')
    def test_convert_currency_to_nzd(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"NZD": 1.4}
        }
        result = convert_currency('USD', 'NZD', 100)
        self.assertEqual(result, 100 * 1.4)

    @patch('requests.get')
    def test_convert_currency_to_kwd(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"KWD": 0.3}
        }
        result = convert_currency('USD', 'KWD', 100)
        self.assertEqual(result, 100 * 0.3)

    @patch('requests.get')
    def test_convert_currency_to_bhd(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"BHD": 0.38}
        }
        result = convert_currency('USD', 'BHD', 100)
        self.assertEqual(result, 100 * 0.38)

    @patch('requests.get')
    def test_convert_currency_to_omr(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": "success",
            "conversion_rates": {"OMR": 0.39}
        }
        result = convert_currency('USD', 'OMR', 100)
        self.assertEqual(result, 100 * 0.39)


if __name__ == '__main__':
    unittest.main()
