from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_crypto_options():
    cryptos = {
        "1": "Bitcoin",
        "2": "Ethereum",
        "3": "Litecoin",
        "4": "Ripple"
    }
    return cryptos

def create_crypto_keyboard():
    """Create an inline keyboard with cryptocurrency options."""
    cryptos = get_crypto_options()
    keyboard = InlineKeyboardMarkup()
    for key, name in cryptos.items():
        keyboard.add(InlineKeyboardButton(text=name, callback_data=f"crypto_{key}"))
    return keyboard
