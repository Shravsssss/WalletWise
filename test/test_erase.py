import os
import json
from mock import patch
from telebot import types
from src import erase


def test_read_json():
    """This is the test function for read json"""
    try:
        if not os.path.exists('./test/dummy_expense_record.json'):
            with open('./test/dummy_expense_record.json', 'w') as json_file:
                json_file.write('{}')
            return json.dumps('{}')
        elif os.stat('./test/dummy_expense_record.json').st_size != 0:
            with open('./test/dummy_expense_record.json') as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def create_message(text):
    """This is the create message function"""
    params = {'messagebody': text}
    chat = types.User("894127939", False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")
