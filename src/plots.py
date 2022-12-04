import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from . import helper

month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar',
              4: 'Mar', 5: 'Apr', 6: 'Jun',
              7: 'Jul', 8: 'Aug', 9: 'Sep',
              10: 'Oct', 11: 'Nov', 12: 'Dec'}

DATE_FORMAT = '%d-%b-%Y'
TIME_FORMAT = '%H:%M'
MONTH_FORMAT = '%b-%Y'

helper.load_config()

# getting json files
# user_key_filename = helper.get_user_profile_file()
user_key = helper.get_user_profile_file()

# expenseFile = helper.get_user_expenses_file()
expense_dict = helper.get_user_expenses_file()

# transactionFile = helper.get_group_expenses_file()
transaction_dict = helper.get_group_expenses_file()


def label_amount(y):
    """This is the label amount function"""
    for ind, val in enumerate(y):
        plt.text(ind, val, str(round(val, 2)), ha='center', va='bottom')


def get_amount_df(
    chat_id,
    data_code,
    expense_dict_values,
    transaction_dict_values,
    amount_type="overall"
):
    """This is the get amount df function"""
    # plot overall expenses
    individual_expenses, shared_expenses = [], []
    if amount_type not in ["shared"]:
        if data_code in [2, 4]:
            for i in expense_dict_values[chat_id]['personal_expenses']:
                individual_expenses.append(i.split(','))
    # print("get amount expense dict run")
    if data_code in [3, 4]:
        for j in expense_dict_values[chat_id]['group_expenses']:
            temp_dict = transaction_dict_values[j]
            shared_expenses.append([
                temp_dict['created_at'],
                temp_dict['category'],
                temp_dict['members'][chat_id]
            ])
    total_expenses = individual_expenses + shared_expenses
    total_expenses_df = pd.DataFrame(
        total_expenses,
        columns=['Date', 'Category', 'Amount']
    )
    total_expenses_df['Amount'] = total_expenses_df['Amount'].astype(float)
    total_expenses_df['Date'] = pd.to_datetime(
        total_expenses_df['Date'],
        format=DATE_FORMAT + ' ' + TIME_FORMAT
    )
    return total_expenses_df


def check_data_present(chat_id, expense_dict_values):
    """This is the check data present function"""
    # checking if chat id has any data

    # 1 : data not present in both individual data and shared transactions
    # 2 : data present in individual data but not in shared transactions
    # 3 : data present in shared transaction but not in individual data
    # 4 : data present in both individual data and shared transactions

    # data_present, transaction_present = 99 , 99
    if chat_id not in expense_dict.keys():
        # chat_id is not present in expense_dict
        return 1
    elif expense_dict_values[chat_id]['personal_expenses'] == []:
        # data_present = 0
        if 'group_expenses' not in expense_dict_values[chat_id].keys():
            # transaction_present = 0
            return 1
        elif expense_dict_values[chat_id]['group_expenses'] == []:
            # transaction_present = 0
            return 1
        else:
            # transaction_present = 1
            return 3
    else:
        # data_present = 1
        if 'group_expenses' not in expense_dict_values[chat_id].keys():
            # transaction_present = 0
            return 2
        elif expense_dict_values[chat_id]['group_expenses'] == []:
            # transaction_present = 0
            return 2
        else:
            # transaction_present = 1
            return 4


def overall_plot(
    chat_id,
    start_date,
    end_date,
    expense_dict_values,
    transaction_dict_values
):
    """This is the overall plot function"""
    check_data_val = check_data_present(chat_id, expense_dict_values)
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df(
            chat_id,
            check_data_val,
            expense_dict_values,
            transaction_dict_values,
            amount_type="overall"
        )
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] >= start_date
        ]
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] <= end_date
        ]
        sum_df = total_expenses_df[
            ['Category', 'Amount']
        ].groupby(
            ['Category'],
            as_index=False
        ).sum()
        # check if df is blank
        if sum_df.shape[0] == 0:
            # 5 means "No expense data for selected dates"
            return 5
        else:
            rand_val = np.random.randint(1, 5000)
            plt.figure(rand_val)
            plt.title("Total Expenses (for the Dates Selected)")
            plt.ylabel('Amount ($)')
            plt.xlabel('Category')
            plt.xticks(rotation=45)
            label_amount(sum_df['Amount'])
            plt.bar(
                sum_df['Category'],
                sum_df['Amount'],
                color=['r', 'g', 'b', 'y', 'm', 'c', 'k']
            )
            plt.savefig('overall_expenses.png', bbox_inches='tight')
            return 7


def categorical_plot(
    chat_id,
    start_date,
    end_date,
    selected_cat,
    expense_dict_values,
    transaction_dict_values
):
    """This is the categorical plot function"""
    check_data_val = check_data_present(chat_id, expense_dict_values)
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df(
            chat_id,
            check_data_val,
            expense_dict_values,
            transaction_dict_values,
            amount_type="overall"
        )
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] >= start_date
        ]
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] <= end_date
        ]
        total_expenses_df = total_expenses_df[
            total_expenses_df['Category'].isin([selected_cat])
        ]
        total_expenses_df['Month'] = total_expenses_df['Date'].apply(
            lambda x: month_dict[x.month]
        )
        sum_df = total_expenses_df[['Month', 'Amount']].groupby(
            ['Month'],
            as_index=False
        ).sum()
        if sum_df.shape[0] == 0:
            # 6 means "No expense data for selected dates and Category"
            return 6
        else:
            rand_val = np.random.randint(5001, 10000)
            plt.figure(rand_val)
            plt.title("Expenses (for the Dates Selected)")
            plt.ylabel('Amount ($)')
            plt.xlabel('Month')
            # plt.xticks(rotation=45)
            label_amount(sum_df['Amount'])
            plt.bar(
                sum_df['Month'],
                sum_df['Amount'],
                color=['r', 'g', 'b', 'y', 'm', 'c', 'k']
            )
            plt.savefig('categorical_expenses.png', bbox_inches='tight')
            helper.date_range = []
            return 7


def owe(chat_id, expense_dict_values, transaction_dict_values):
    """This is the owe function"""
    check_data_val = check_data_present(chat_id, expense_dict_values)
    if check_data_val == 1:
        return 1
    elif check_data_val == 2:
        return 2
    else:
        all_ids = []
        for j in expense_dict_values[chat_id]['group_expenses']:
            all_ids += transaction_dict_values[j]['members'].keys()
            all_ids = list(set(all_ids))
            all_ids.remove(chat_id)

        owe_dict = {}
        for id_value in all_ids:
            owe_dict[id_value] = []
        for j in expense_dict_values[chat_id]['group_expenses']:
            temp_dict = transaction_dict_values[j]
            creator_id = temp_dict['created_by']
            if chat_id == creator_id:
                for c_id in temp_dict['members'].keys():
                    if c_id != chat_id:
                        owe_dict[c_id] += [temp_dict['members'][c_id]]
            else:
                owe_dict[creator_id] += [-1 * (temp_dict['members'][chat_id])]

        x, y = [], []
        for key in owe_dict.items():
            val = owe_dict[key]
            if val != []:
                x.append(user_key[key])
                y.append(sum(val) * -1)  # what I owe will be positive on plot

        rand_val = np.random.randint(10001, 15000)
        plt.figure(rand_val)
        plt.title("What I owe")
        plt.ylabel('Amount ($)')
        plt.xlabel('User')
        # plt.xticks(rotation=45)
        label_amount(y)
        plt.bar(x, y, color=['r', 'g', 'b', 'y', 'm', 'c', 'k'])
        plt.savefig('owe.png', bbox_inches='tight')
        return 7
