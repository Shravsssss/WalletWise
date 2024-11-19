# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 17:19:18 2022

@author: DELL
"""

# test cases

import os
import json
import datetime
import pandas as pd
from src import plots


def test_read_expense_json():
    """This is the test function for read expense json"""
    filename = "test_user_expenses.json"
    filepath = os.path.join("data", "testdata", filename)
    try:
        if os.stat(filepath).st_size != 0:
            with open(filepath) as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def test_read_transaction_json():
    """This is the test function for read transaction json"""
    filename = "test_group_expenses.json"
    filepath = os.path.join("data", "testdata", filename)
    try:
        if os.stat(filepath).st_size != 0:
            with open(filepath) as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def test_get_amount_df():
    """This is the test function for get amount"""
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    ret = plots.get_amount_df_with_other_handles(
        "4583959357",
        4,
        test_dict,
        trans_dict,
        amount_type="overall"
    )
    assert isinstance(ret, pd.core.frame.DataFrame)


def test_individual_present_shared_present():
    """This is the test function for individual present and shared present"""
    # test_dict = test_read_expense_json()
    test_dict = {
        '5718815807': {
            'personal_expenses': [
                '21-Aug-2022 17:37,Groceries,124.93'
            ],
            'group_expenses': [
                '26622027'
            ]
        }
    }
    # mocker.return_value =4
    ret_val = plots.check_data_present_with_other_handles(
        chat_id="5718815807",
        expense_dict_values=test_dict
    )
    assert ret_val == 4


def test_individual_present_shared_absent():
    """This is the test function for individual present and shared absent"""
    test_dict = {
        '5718815807': {
            'personal_expenses': ['21-Aug-2022 17:37,Groceries,124.93']
        }
    }
    # mocker.return_value =2
    ret_val = plots.check_data_present_with_other_handles(
        "5718815807",
        test_dict
    )
    assert ret_val == 2


def test_individual_absent_shared_present():
    """This is the test function for individual absent shared present"""
    test_dict = {
        '5718815807': {
            'personal_expenses': [],
            'group_expenses': ['26622027']
        }
    }
    ret_val = plots.check_data_present_with_other_handles(
        "5718815807",
        test_dict
    )
    assert ret_val == 3


def test_individual_absent_shared_absent():
    """This is the test function for individual absent and shared absent"""
    test_dict = {
        '5718815807': {
            'personal_expenses': [],
            'group_expenses': ['26622027']
        }
    }
    ret_val = plots.check_data_present("5555511111", test_dict)
    assert ret_val == 1


def test_categorical_plot_no_data_for_dates_and_cat():
    """This is the test function for categorical
    plot no data for dates and cat"""
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021, 12, 12)
    end_date = datetime.datetime(2022, 1, 12)
    ret_val = plots.categorical_plot_with_other_handles(
        "4583959357",
        start_date,
        end_date,
        "Food",
        test_dict,
        trans_dict
    )
    assert ret_val == 6


def test_categorical_plot_no_data():
    """This is the test function for categorical plot no data"""
    test_dict = test_read_expense_json()
    # trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021, 12, 12)
    end_date = datetime.datetime(2022, 1, 12)
    ret_val = plots.categorical_plot(
        "5555511111",
        start_date,
        end_date,
        "Food",
        test_dict
    )
    assert ret_val == 1


def test_owe_plot_no_data():
    """This is the test function for owe plot no data"""
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    ret_val = plots.owe("5555511111", test_dict, trans_dict)
    assert ret_val == 1


def test_owe_plot_no_shared_data():
    """This is the test function for owe plot no shared data"""
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    ret_val = plots.owe_with_other_handles("5457678456", test_dict, trans_dict)
    assert ret_val == 2


def test_overall_plot_no_data_for_dates():
    """This is the test function for overll plot no data for dates"""
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021, 12, 12)
    end_date = datetime.datetime(2022, 1, 12)
    ret_val = plots.overall_plot_with_other_handles(
        "4583959357",
        start_date,
        end_date,
        test_dict,
        trans_dict
    )
    assert ret_val == 5


def test_overall_plot_no_data():
    """This is the test function for overall plot no data"""
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021, 12, 12)
    end_date = datetime.datetime(2022, 1, 12)
    ret_val = plots.overall_plot(
        "5555511111",
        start_date,
        end_date,
        test_dict,
        trans_dict
    )
    assert ret_val == 1


def check_owe_plot_shared_data():
    """This is the test function for owe plot shared data"""
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    ret_val = plots.owe("4583959357", test_dict, trans_dict)
    os.remove('owe.png')
    assert ret_val == 7
