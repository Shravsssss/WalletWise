# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

# Module providing display of owings
from .pymongo_run import get_database


def run(message, bot):
    """This is the run function"""
    # msg = bot.reply_to(message, 'Please enter your email')
    chat_id = str(message.chat.id)
    print(chat_id)
    db = get_database()["OWING_DETAILS"]
    user_details = db.find_one({"payer_chatid": chat_id})
    display_text = ""
    user_owing_details = []
    if bool(user_details):
        for doc in user_details["borrowers"]:
            user_owing_details.append(doc)

        for borrower in user_owing_details:
            borrower_chat_id = borrower["borrower_chatid"]
            borrower_amount = borrower["amount"]
            db_borrower = get_database()["USER_EMAILS"].find()
            borrower_email = ""
            for doc in db_borrower:
                for key in doc:
                    if str(key) == str(borrower_chat_id):
                        borrower_email = doc[key]
                        break
            if borrower_amount < 0:
                display_text += "You owe " + borrower_email
                display_text += str(abs(borrower_amount)) + "\n"
            else:
                display_text += borrower_email + " owes you "
                display_text += str(abs(borrower_amount)) + "\n"
    else:
        display_text = "You have no shared spendings yet."
    bot.send_message(chat_id, display_text)
    # bot.register_next_step_handler(msg, post_email_input, bot)
    return user_owing_details, user_details
