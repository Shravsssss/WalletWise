import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from . import helper
from sklearn.linear_model import LinearRegression
from .pymongo_run import get_database
import os
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
import logging
if not os.path.exists('temp'):
    os.makedirs('temp')

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
    """This is the function for get amount"""
    # plot overall expenses
    print('get_amount_df')
    individual_expenses, shared_expenses = [], []
    expense_dict_values = helper.get_user_history(chat_id)
    if amount_type not in ["shared"]:
        if data_code in [2, 4]:
            if expense_dict_values['personal_expenses']:
                for i in expense_dict_values['personal_expenses']:
                    individual_expenses.append(i.split(','))
    # print("get amount expense dict run")
    if data_code in [3, 4]:
        for j in expense_dict['group_expenses']:
            print('jnjnknknkjjjjjjj', j)
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
    print(total_expenses_df)
    return total_expenses_df


def check_data_present(chat_id, expense_dict_values):
    """This is the check data present function"""
    # checking if chat id has any data
    print('check_data_rpresnt')

    #  1 : data not present in both individual data and shared transactions
    #  2 : data present in individual data but not in shared transactions
    #  3 : data present in shared transaction but not in individual data
    #  4 : data present in both individual data and shared transactions

    history = helper.get_user_history(chat_id)
    if history is None:
        return 1
    if history['personal_expenses'] and history['group_expenses']:
        return 4
    elif history['personal_expenses']:
        return 2
    else:
        return 3
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


def pie_plot(
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
            # plt.ylabel('Amount ($)')
            # plt.xlabel('Category')
            # plt.xticks(rotation=45)
            # label_amount(sum_df['Amount'])
            plt.pie(
                sum_df.Amount,
                labels=sum_df.Category,
                autopct='%.1f%%',
                explode=[0.1] * len(sum_df.index)
            )
            plt.legend(
                bbox_to_anchor=(1.0, 0.1),
                loc='upper left',
                borderaxespad=0
            )
            plt.savefig("pie.png", dpi=200)
            return 7


def box_plot(
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
            # plt.title("Total Expenses (for the Dates Selected)")
            # plt.ylabel('Amount ($)')
            # plt.xlabel('Category')
            # plt.xticks(rotation=45)
            # label_amount(sum_df['Amount'])
            plt.boxplot(sum_df["Amount"], showmeans=True)
            plt.ylabel("Amount($)")
            plt.title(
                "Complete Statistics of Expenses between the chosen Dates"
            )
            plt.savefig('box.png')
            return 7


def categorical_plot(
    chat_id,
    start_date,
    end_date,
    selected_cat,
    expense_dict_values
):
    """This is the categorical plot function"""
    check_data_val = check_data_present(chat_id, expense_dict_values)
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df(
            chat_id,
            check_data_val,
            expense_dict,
            transaction_dict,
            amount_type="overall"
        )
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] >= start_date
        ]
        print(total_expenses_df)
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] <= end_date
        ]
        print(total_expenses_df)
        print(selected_cat)
        print(total_expenses_df['Category'])
        # Error in next line
        total_expenses_df = total_expenses_df[
            total_expenses_df[
                'Category'
            ].isin(
                [selected_cat]
            )
        ]
        print(total_expenses_df)
        total_expenses_df['Month'] = total_expenses_df[
            'Date'
        ].apply(
            lambda x: month_dict[x.month]
        )
        print(total_expenses_df)
        sum_df = total_expenses_df[
            ['Month', 'Amount']
        ].groupby(
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


def hist_categorical_plot(
    chat_id,
    start_date,
    end_date,
    selected_cat,
    expense_dict_values
):
    """This is the categorical plot function"""
    check_data_val = check_data_present(chat_id, expense_dict_values)
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df(
            chat_id,
            check_data_val,
            expense_dict,
            transaction_dict,
            amount_type="overall"
        )
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] >= start_date
        ]
        print(total_expenses_df)
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] <= end_date
        ]
        print(total_expenses_df)
        print(selected_cat)
        print(total_expenses_df['Category'])
        # Error in next line
        total_expenses_df = total_expenses_df[
            total_expenses_df[
                'Category'
            ].isin(
                [selected_cat]
            )
        ]
        print(total_expenses_df)
        total_expenses_df['Month'] = total_expenses_df[
            'Date'
        ].apply(
            lambda x: month_dict[x.month]
        )
        print(total_expenses_df)
        sum_df = total_expenses_df[
            ['Month', 'Amount']
        ].groupby(
            ['Month'],
            as_index=False
        ).sum()
        if sum_df.shape[0] == 0:
            # 6 means "No expense data for selected dates and Category"
            return 6
        else:
            rand_val = np.random.randint(5001, 10000)
            plt.figure(rand_val)
            # plt.title("Expenses (for the Dates Selected)")
            # plt.ylabel('Amount ($)')
            # plt.xlabel('Month')
            # plt.xticks(rotation=45)
            # label_amount(sum_df['Amount'])
            plt.hist(
                total_expenses_df['Amount'],
                bins=10,
                density=True,
                alpha=0.6,
                color='b'
            )
            plt.title("Statistics for " + selected_cat)
            plt.savefig('hist.png', bbox_inches='tight')
            helper.date_range = []
            return 7


def box_categorical_plot(
    chat_id,
    start_date,
    end_date,
    selected_cat,
    expense_dict_values
):
    """This is the categorical plot function"""
    check_data_val = check_data_present(chat_id, expense_dict_values)
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df(
            chat_id,
            check_data_val,
            expense_dict,
            transaction_dict,
            amount_type="overall"
        )
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] >= start_date
        ]
        print(total_expenses_df)
        total_expenses_df = total_expenses_df[
            total_expenses_df['Date'] <= end_date
        ]
        print(total_expenses_df)
        print(selected_cat)
        print(total_expenses_df['Category'])
        # Error in next line
        total_expenses_df = total_expenses_df[
            total_expenses_df['Category'].isin(
                [selected_cat]
            )
        ]
        print(total_expenses_df)
        total_expenses_df['Month'] = total_expenses_df[
            'Date'
        ].apply(
            lambda x: month_dict[x.month]
        )
        print(total_expenses_df)
        sum_df = total_expenses_df[
            ['Month', 'Amount']
        ].groupby(
            ['Month'],
            as_index=False
        ).sum()
        if sum_df.shape[0] == 0:
            # 6 means "No expense data for selected dates and Category"
            return 6
        else:
            rand_val = np.random.randint(5001, 10000)
            plt.figure(rand_val)
            # plt.title("Expenses (for the Dates Selected)")
            # plt.ylabel('Amount ($)')
            # plt.xlabel('Month')
            # # plt.xticks(rotation=45)
            # label_amount(sum_df['Amount'])
            plt.boxplot(total_expenses_df["Amount"])
            plt.ylabel("Amount($)")
            plt.title("Statistics for " + selected_cat)
            plt.savefig('box_cat.png')
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


def get_amount_df_with_other_handles(
    chat_id,
    data_code,
    expense_dict_values,
    transaction_dict_values,
    amount_type="overall"
):
    """This is the get amount df with other handles function"""
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


def check_data_present_with_other_handles(chat_id, expense_dict_values):
    """This is the check data present with other handles function"""
    # checking if chat id has any data

    #  1 : data not present in both individual data and shared transactions
    #  2 : data present in individual data but not in shared transactions
    #  3 : data present in shared transaction but not in individual data
    #  4 : data present in both individual data and shared transactions

    # data_present, transaction_present = 99 , 99
    if chat_id not in expense_dict_values.keys():
        # chat_id is not present in expense_dict_values
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


def categorical_plot_with_other_handles(
    chat_id,
    start_date,
    end_date,
    selected_cat,
    expense_dict_values,
    transaction_dict_values
):
    """This is the categorical plot with other handles function"""
    check_data_val = check_data_present_with_other_handles(
        chat_id,
        expense_dict_values
    )
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df_with_other_handles(
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
        total_expenses_df['Month'] = total_expenses_df[
            'Date'
        ].apply(
            lambda x: month_dict[x.month]
        )
        sum_df = total_expenses_df[
            ['Month', 'Amount']
        ].groupby(
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


def owe_with_other_handles(
    chat_id,
    expense_dict_values,
    transaction_dict_values
):
    """This is the owe with other handles function"""
    check_data_val = check_data_present_with_other_handles(
        chat_id,
        expense_dict_values
    )
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
        for m in all_ids:
            owe_dict[m] = []
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
        for k, val in owe_dict.items():
            if val != []:
                x.append(user_key[k])
                # what I owe will be positive on plot
                y.append(sum(val) * -1)

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


def overall_plot_with_other_handles(
    chat_id,
    start_date,
    end_date,
    expense_dict_values,
    transaction_dict_values
):
    """This is the overall plot with other handles function"""
    check_data_val = check_data_present_with_other_handles(
        chat_id,
        expense_dict_values
    )
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df_with_other_handles(
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


def create_time_series_plot(chat_id):
    try:
        db = get_database()
        collection = db["USER_EXPENSES"]

        user_doc = collection.find_one({"chatid": chat_id})

        if not user_doc or not user_doc.get('personal_expenses'):
            raise Exception(
                "No expense data found. Please add some expenses first.")

        # Parse the expenses
        expenses = []
        for exp_str in user_doc['personal_expenses']:
            try:
                date_str, category, amount_str = exp_str.split(', ')
                # Handle different date formats
                try:
                    # Try the standard format first
                    date = pd.to_datetime(date_str, format='%d %b %Y %H:%M')
                except BaseException:
                    try:
                        # Try with hyphens
                        date = pd.to_datetime(date_str.replace(
                            '-', ' '), format='%d %b %Y %H:%M')
                    except BaseException:
                        # If all else fails, try flexible parsing
                        date = pd.to_datetime(
                            date_str, format='mixed', dayfirst=True)

                expenses.append({
                    'date': date,
                    'category': category,
                    'amount': float(amount_str)
                })
            except Exception as e:
                print(f"Error parsing expense: {exp_str}, Error: {str(e)}")
                continue

        if not expenses:
            raise Exception("No valid expenses found after parsing")

        # Convert to DataFrame and sort
        df = pd.DataFrame(expenses)
        df = df.sort_values('date')

        # Create figure with larger size
        plt.figure(figsize=(15, 10))

        # Time series plot
        plt.subplot(2, 1, 1)
        plt.plot(
            df['date'],
            df['amount'],
            marker='o',
            linestyle='-',
            markersize=4)
        plt.title('Your Daily Expenses Over Time')
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.grid(True)
        plt.xticks(rotation=45)

        # Category plot
        plt.subplot(2, 1, 2)
        category_totals = df.groupby('category')['amount'].sum()
        category_totals.plot(kind='bar')
        plt.title('Expenses by Category')
        plt.xlabel('Category')
        plt.ylabel('Total Amount ($)')
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save plot
        if not os.path.exists('temp'):
            os.makedirs('temp')
        plot_path = f"temp/{chat_id}_trend.png"
        plt.savefig(plot_path)
        plt.close()

        return plot_path

    except Exception as e:
        # logging.error(f"Error in create_time_series_plot: {str(e)}")
        raise Exception(f"Could not create trend plot: {str(e)}")


def predict_expenses(chat_id, prediction_days=30):
    """Predict future expenses with anomaly detection and generate visual insights."""
    try:
        # Load data from the database
        db = get_database()
        collection = db["USER_EXPENSES"]
        user_doc = collection.find_one({"chatid": chat_id})

        if not user_doc or not user_doc.get('personal_expenses'):
            raise Exception(
                "No expense data found for prediction. Please add some expenses first.")

        # Parse and preprocess expense data
        expenses = []
        for exp_str in user_doc['personal_expenses']:
            try:
                date_str, category, amount_str = exp_str.split(', ')
                date_str = date_str.replace(
                    'Sept', 'Sep')  # Handle month abbreviation
                date = pd.to_datetime(date_str, dayfirst=True)  # Parse date
                expenses.append(
                    {'date': date, 'category': category, 'amount': float(amount_str)})
            except Exception as e:
                print(f"Error parsing expense: {exp_str}, Error: {str(e)}")
                continue

        if not expenses:
            raise Exception("No valid expenses found after parsing")

        # Convert to DataFrame and sort by date
        df = pd.DataFrame(expenses).sort_values('date')
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['week_of_month'] = (df['date'].dt.day - 1) // 7 + 1
        df['month'] = df['date'].dt.month

        categories = df['category'].unique()
        predictions = {}

        plt.figure(figsize=(15, 5 * len(categories)))

        for idx, category in enumerate(categories, 1):
            category_data = df[df['category'] == category].copy()

            if len(category_data) < 2:
                continue

            # Anomaly Detection
            iso_forest = IsolationForest(contamination=0.05, random_state=42)
            category_data['anomaly'] = iso_forest.fit_predict(
                category_data[['amount']])
            anomalies = category_data[category_data['anomaly'] == -1]

            # Calculate rolling averages for feature engineering
            category_data['rolling_7day_avg'] = category_data['amount'].rolling(
                window=7, min_periods=1).mean()
            category_data['rolling_30day_avg'] = category_data['amount'].rolling(
                window=30, min_periods=1).mean()

            # Prepare features for prediction
            feature_columns = [
                'day_of_week',
                'day_of_month',
                'week_of_month',
                'month',
                'rolling_7day_avg',
                'rolling_30day_avg']
            X = category_data[feature_columns]
            y = category_data['amount']

            # Train the model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X, y)

            # Generate future dates for prediction
            last_date = category_data['date'].max()
            future_dates = pd.date_range(
                start=last_date,
                periods=prediction_days + 1,
                freq='D')[
                1:]

            # Create future features
            future_data = pd.DataFrame({
                'date': future_dates,
                'day_of_week': future_dates.dayofweek,
                'day_of_month': future_dates.day,
                'week_of_month': ((future_dates.day - 1) // 7 + 1),
                'month': future_dates.month,
                'rolling_7day_avg': [category_data['rolling_7day_avg'].iloc[-1]] * len(future_dates),
                'rolling_30day_avg': [category_data['rolling_30day_avg'].iloc[-1]] * len(future_dates)
            })

            # Predict future expenses
            future_amounts = model.predict(future_data[feature_columns])

            # Store predictions
            predictions[category] = {
                'dates': future_dates,
                'amounts': future_amounts,
                'current_avg': y.mean(),
                'predicted_avg': future_amounts.mean(),
                'importance': dict(zip(feature_columns, model.feature_importances_)),
                'anomalies': anomalies[['date', 'amount']]
            }

            # Plot actual, predicted, and anomalies
            plt.subplot(len(categories), 1, idx)
            plt.plot(
                category_data['date'],
                category_data['amount'],
                'o-',
                label='Actual',
                alpha=0.5,
                markersize=4)
            plt.plot(
                future_dates,
                future_amounts,
                'r--',
                label='Predicted',
                linewidth=2)
            plt.scatter(
                anomalies['date'],
                anomalies['amount'],
                color='red',
                label='Anomaly',
                marker='x')

            # Confidence intervals
            std_dev = y.std()
            plt.fill_between(
                future_dates,
                future_amounts - std_dev,
                future_amounts + std_dev,
                color='red',
                alpha=0.2,
                label='Confidence Interval')

            plt.title(f'{category} Expenses - Actual, Predicted & Anomalies')
            plt.xlabel('Date')
            plt.ylabel('Amount ($)')
            plt.legend()
            plt.grid(True)
            plt.xticks(rotation=45)

        plt.tight_layout()

        # Save prediction plot
        if not os.path.exists('temp'):
            os.makedirs('temp')
        plot_path = f"temp/{chat_id}_prediction_anomalies.png"
        plt.savefig(plot_path)
        plt.close()

        # Prepare prediction summary
        summary = "📊 Expense Predictions & Anomaly Detection Summary:\n\n"
        for category, pred in predictions.items():
            percent_change = (
                (pred['predicted_avg'] - pred['current_avg']) / pred['current_avg']) * 100

            summary += f"💰 {category}:\n"
            summary += f"   • Current average: ${pred['current_avg']:.2f}\n"
            summary += f"   • Predicted average: ${
                pred['predicted_avg']:.2f}\n"
            summary += f"   • Expected change: {percent_change:+.1f}%\n"

            # Include anomalies if any
            if not pred['anomalies'].empty:
                summary += f"   • Anomalies Detected:\n"
                for _, row in pred['anomalies'].iterrows():
                    summary += f"      - {
                        row['date'].strftime('%d-%b-%Y')}: ${
                        row['amount']:.2f}\n"

            # Add top factors for prediction
            top_factors = sorted(
                pred['importance'].items(),
                key=lambda x: x[1],
                reverse=True)[
                :3]
            summary += f"   • Key factors: {
                ', '.join(
                    f[0] for f in top_factors)}\n\n"

        return plot_path, summary

    except Exception as e:
        raise Exception(
            f"Could not create prediction and anomaly detection: {
                str(e)}")
