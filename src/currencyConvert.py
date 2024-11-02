import requests
from telebot import types
from src import helper

# Insert your ExchangeRate-API key here
EXCHANGE_RATE_API_KEY = "333481fb3782ac0721ff6bfc"

# User data to track selection
user_data = {}

def create_currency_menu(bot, chat_id, prompt="Select the output currency:"):
    # Inline keyboard for output currency selection
    markup = types.InlineKeyboardMarkup()
    currencies = helper.get_currency_options()  # Replace with relevant currency list if needed
    buttons = [types.InlineKeyboardButton(c, callback_data=f"currency_{c}") for c in currencies]
    markup.add(*buttons)
    bot.send_message(chat_id, prompt, reply_markup=markup)

def start_currency_convert(bot, message):
    chat_id = message.chat.id
    # Set USD as the default input currency
    user_data[chat_id] = {'input_currency': 'USD', 'output_currency': None, 'amount': None}
    bot.send_message(chat_id, "The input currency is set to USD by default.")
    create_currency_menu(bot, chat_id)

def handle_currency_selection(bot, call):
    chat_id = call.message.chat.id
    currency = call.data.split('_')[1]

    # Set the output currency as the selected currency
    user_data[chat_id]['output_currency'] = currency
    bot.send_message(chat_id, f"Output currency set to {currency}. Now, please enter the amount in USD to convert:")

def handle_amount_input(bot, message):
    chat_id = message.chat.id
    amount = helper.validate_entered_amount(message.text)
    
    if chat_id in user_data and user_data[chat_id].get('output_currency'):
        if amount:
            user_data[chat_id]['amount'] = float(amount)
            input_currency = user_data[chat_id]['input_currency']  # Defaults to 'USD'
            output_currency = user_data[chat_id]['output_currency']
            # Call convert_currency here
            converted_amount = convert_currency(input_currency, output_currency, user_data[chat_id]['amount'])
            
            if converted_amount:
                bot.send_message(chat_id, f"{amount} {input_currency} is {converted_amount:.2f} {output_currency}")
            else:
                bot.send_message(chat_id, "Error retrieving conversion rate. Please try again later.")
        else:
            bot.send_message(chat_id, "Invalid amount. Please enter a valid number.")
    else:
        bot.send_message(chat_id, "Please select the output currency first.")

import requests

def convert_currency(input_currency, output_currency, amount):
    output_currency = output_currency.strip()
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{input_currency}"
    
    try:
        response = requests.get(url)
        
        # Check if the response is empty or invalid
        if response.status_code != 200:
            print("Error fetching conversion rate:", response.status_code, response.text)
            return None
        
        # Try parsing the response as JSON
        data = response.json()
        
        if data.get('result') == 'success':
            rate = data["conversion_rates"][output_currency]
            
            
            return amount * rate
        else:
            print("Error in conversion response:", data.get("error-type", "Unknown error"))
            return None
    
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None
    except ValueError as e:
        print("Failed to decode JSON response:", e)
        print("Response text:", response.text)  # Print the raw response for debugging
        return None

