# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

import logging
# Module providing helper functions
from . import helper
from .pymongo_run import get_database


def run(message, bot):
    """This is the run function"""
    try:
        chat_id = message.chat.id
        user_data = None
        dbname = get_database()
        collection_name = dbname["USER_EXPENSES"]
        item_details = collection_name.find()
        for i in item_details:
            if i['chatid'] == str(chat_id):
                user_data = i
        if user_data is None:
            raise Exception("Sorry! No spending records found!")

        spend_total_str = """Here is your spending history : \nDATE
        , CATEGORY, AMOUNT\n----------------------\n"""
        if len(user_data) == 0:
            spend_total_str = "Sorry! No spending records found!"
        else:
            for rec in user_data["personal_expenses"]:
                spend_total_str += str(rec) + "\n"

            transactions_list = helper.get_group_expenses_file()
            for transaction_id in user_data["group_expenses"]:
                if transaction_id not in transactions_list:
                    exception_message = """An unknown transaction was found
                    in your records, please try again later."""
                    raise Exception(exception_message)
                txn = transactions_list[transaction_id]
                rec = txn["created_at"] + "," + txn["category"]
                rec += "," + str(txn["members"][str(chat_id)])
                spend_total_str += str(rec) + "\n"

        bot.send_message(chat_id, spend_total_str)
    except Exception as exception_value:
        logging.exception(str(exception_value))
        bot.reply_to(message, "Oops!" + str(exception_value))
