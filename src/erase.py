from . import helper
from .pymongo_run import get_database
 
 
def run(message, bot):
    user_list = helper.read_json(helper.getUserExpensesFile())
    chat_id = message.chat.id
    user_data = None
    dbname = get_database()
    collection_name = dbname["USER_EXPENSES"]
    item_details = collection_name.find()
    for i in item_details:
            if i['chatid'] == str(chat_id):
                user_data = i
                myquery = { "chatid": str(chat_id)}
                collection_name.delete_one(myquery)
                delete_history_text = "History has been deleted!"
    if user_data is None:
        delete_history_text = "No records there to be deleted. Start adding your expenses to keep track of your " \
                              "spendings! "
 
    bot.send_message(chat_id, delete_history_text)
 
 
# function to delete a record
def deleteHistory(chat_id, user_list):
    if str(chat_id) in user_list:
        del user_list[str(chat_id)]
    return user_list
 
