import helper
import logging
from telebot import types
from datetime import datetime
from pymongo_run import get_database
 
 
option = {}
 
 
def run(message, bot):
    helper.read_json(helper.getUserExpensesFile())
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.getSpendCategories():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, post_category_selection, bot)
 
 
def post_category_selection(message, bot):
    try:
        chat_id = message.chat.id
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this category \"{}\"!".format(selected_category))
 
        option[chat_id] = selected_category
        message = bot.send_message(chat_id, 'How much did you spend on {}? \n(Enter numeric values only)'.format(str(option[chat_id])))
        bot.register_next_step_handler(message, post_amount_input, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = ""
        commands = helper.getCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)
 
 
def post_amount_input(message, bot, selected_category):
    try:
        chat_id = message.chat.id
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")
        print("----SUCCESS!----")
 
        date_of_entry = datetime.today().strftime(helper.getDateFormat() + ' ' + helper.getTimeFormat())
        date_str, category_str, amount_str = str(date_of_entry), str(option[chat_id]), str(amount_value)
        text_string = date_str+", "+category_str+", "+amount_str
 
 
        dbname = get_database()
        collection_name = dbname["USER_EXPENSES"]
        item_details = collection_name.find()
        flag = 0
        for i in item_details:
             if i['chatid'] == str(chat_id):
                    flag+=1
                    k = i['group_expenses']+[text_string]
                    collection_name.update_one({"chatid":str(chat_id)},{'$set':{"personal_expenses":k}})
             else:
                    flag+=1
                    item = {"chatid":str(chat_id),"personal_expenses":[text_string], "group_expenses":[]}
                    collection_name.insert_one(item)
        if flag==0:
                item = {"chatid":str(chat_id),"personal_expenses":[text_string], "group_expenses":[]}
                collection_name.insert_one(item)            
       
           
        bot.send_message(chat_id, 'The following expenditure has been recorded: You have spent ${} for {} on {}'.format(amount_str, category_str, date_str))
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))
 
