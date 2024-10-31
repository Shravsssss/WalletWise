import requests
from telebot import types
from .helper import get_spend_categories, validate_entered_amount

# Insert your ExchangeRate-API key here
EXCHANGE_RATE_API_KEY = "333481fb3782ac0721ff6bfc"

# User data to track selection
user_data = {}

def create_currency_menu(bot, chat_id, prompt="Select currency:"):
    # Inline keyboard for currency selection
    markup = types.InlineKeyboardMarkup()
    currencies = get_spend_categories()  # Replace with relevant currency list if needed
    buttons = [types.InlineKeyboardButton(c, callback_data=f"currency_{c}") for c in currencies]
    markup.add(*buttons)
    bot.send_message(chat_id, prompt, reply_markup=markup)

def start_currency_convert(bot, message):
    chat_id = message.chat.id
    user_data[chat_id] = {'input_currency': None, 'output_currency': None, 'amount': None}
    bot.send_message(chat_id, "Choose the input currency:")
    create_currency_menu(bot, chat_id)

def handle_currency_selection(bot, call):
    chat_id = call.message.chat.id
    currency = call.data.split('_')[1]

    if user_data[chat_id]['input_currency'] is None:
        user_data[chat_id]['input_currency'] = currency
        bot.send_message(chat_id, f"Input currency set to {currency}. Now choose the output currency:")
        create_currency_menu(bot, chat_id, prompt="Choose the output currency:")
    elif user_data[chat_id]['output_currency'] is None:
        user_data[chat_id]['output_currency'] = currency
        bot.send_message(chat_id, f"Output currency set to {currency}. Enter the amount to convert:")
    else:
        amount = user_data[chat_id].get('amount')
        input_currency = user_data[chat_id]['input_currency']
        output_currency = user_data[chat_id]['output_currency']
        if amount is not None:
            converted_amount = convert_currency(input_currency, output_currency, amount)
            if converted_amount:
                bot.send_message(chat_id, f"{amount} {input_currency} is {converted_amount:.2f} {output_currency}")
            else:
                bot.send_message(chat_id, "Error retrieving conversion rate. Please try again later.")

def convert_currency(input_currency, output_currency, amount):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/pair/{input_currency}/{output_currency}"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data['result'] == 'success':
        rate = data['conversion_rate']
        return amount * rate
    else:
        print("Error fetching conversion rate:", data.get("error-type", "Unknown error"))
        return None
