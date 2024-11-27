# WalletWise
> This is a requirement for NCSU's CSC510 Software Engineering Course project 3 for Group 54.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![DOI](https://zenodo.org/badge/880744201.svg)](https://doi.org/10.5281/zenodo.14027332) ![GitHub open issues](https://img.shields.io/github/issues-raw/Shravsssss/WalletWise) ![GitHub closed issues](https://img.shields.io/github/issues-closed/Shravsssss/WalletWise) [![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/) [![codecov](https://img.shields.io/badge/codecov-83%25-brightgreen.svg)](https://codecov.io/gh/Shravsssss/WalletWise) [![Build repo](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/Shravsssss/WalletWise/actions) [![Python Style Checker](https://img.shields.io/badge/style%20checker-passing-brightgreen.svg)](https://github.com/Shravsssss/WalletWise/actions) [![Lint Python](https://img.shields.io/badge/lint-passing-brightgreen.svg)](https://github.com/Shravsssss/WalletWise/actions) [![CodeQL](https://img.shields.io/badge/CodeQL-passing-brightgreen.svg)](https://github.com/Shravsssss/WalletWise/security/code-scanning) [![Run Tests On Push](https://img.shields.io/badge/tests-passing-brightgreen.svg)](https://github.com/Shravsssss/WalletWise/actions) [![Code Style](https://img.shields.io/badge/code%20style-pep8-orange.svg)]() ![Repo Size](https://img.shields.io/badge/repo%20size-41.3%20MB-blue.svg)  

<hr>

## Delta from Project 1
**Advanced Predictive Analytics for Spending Patterns**: In the current project, "WalletWise," we have introduced advanced predictive analytics to implement category-specific expenditure forecasting and anomaly detection. This functionality provides users with precise, real-time spending insights, allowing them to make data-driven financial decisions effortlessly.

**Budget Setting and Alerts**: Users can now set monthly or weekly budgets for specific categories (e.g., Food, Transport) and receive alerts as they approach their budget limit. This proactive budgeting feature, available through commands like /setBudget [category] [amount] and /checkBudget, empowers users to stay on top of their spending and avoid overspending.

**Recurring Expense Reminders**: We've added the ability for users to set recurring expenses (e.g., rent, utility bills) and receive reminders before their due dates. Using commands like /addRecurringExpense [category] [amount] [interval] and /listRecurringExpenses, users can manage recurring payments efficiently and stay on track with their obligations.

**Goal Setting and Progress Tracking**: Users can now set financial goals (e.g., saving $500 for a trip) and track their progress based on spending habits. This feature, accessible via commands like /setGoal [goal_name] [target_amount] and /checkGoals, helps users stay motivated and on track to meet their financial targets.

**Income Tracking and Net Savings Calculation**: We've introduced support for tracking income and calculating net savings (income minus expenses). Using commands like /addIncome [amount] [description] and /netSavings, users can gain a clear view of their financial health.

**Export Expenses as CSV or PDF**: Users can now export their expenses for a specific date range in CSV or PDF format, making it easier to analyze spending offline or share reports. The feature is accessible through the /exportExpenses [format] [start_date] [end_date] command, and the generated files are delivered via Telegram.

**Monthly or Weekly Summary Reports**: A summary report feature has been added, allowing users to receive detailed insights into their expenses for the past week or month. The reports include total spending, top categories, and any anomalies detected, and are generated using the /monthlyReport command.

These newly added features significantly enhance the functionality of WalletWise, transforming it into a comprehensive, user-friendly financial management tool.


## Goal

> Develop a dynamic Telegram-based application to help users manage, track, and forecast expenses effortlessly. Features include budget setting, savings goals, predictive analytics, recurring reminders, cryptocurrency tracking, currency conversion, and detailed reports for comprehensive financial management.
---

## Motivation
> Managing personal and group finances manually can be tedious and time-consuming, especially when it involves tasks like tracking expenses, forecasting spending patterns, and managing recurring payments. While standalone mobile apps exist, they often require additional storage, frequent updates, and manual input from users. With the updated "WalletWise" project, we aim to simplify financial management by integrating these features directly into the popular Telegram app. Users can efficiently track expenses, set budgets, receive reminders, monitor financial goals, and even analyze spending patterns with the help of simple Telegram commands. By eliminating the need for additional apps, WalletWise ensures seamless, real-time financial management within a familiar platform, making it an ideal solution for modern, busy lifestyles.

## Features

WalletWise is an easy-to-use Telegram Bot that assists you in managing and recording your daily expenses seamlessly within a familiar platform. With simple commands, this bot allows you to:

- Add/Record a new spending.
- Add shared expenses with friends.
- Show the sum of your expenditure for the current day or month.
- Display your spending history and trends over time.
- Clear/Erase all your records.
- Add/Manage your profile.
- Show owings/borrowings and settle up pending dues with ease.
- Set monthly or weekly budgets for specific categories and receive alerts as you approach your limits.
- Record and track cryptocurrency transactions.
- Set and track financial goals, including savings progress for trips, purchases, or other milestones.
- Add savings towards specific goals and monitor your progress.
- Receive reminders for recurring expenses such as rent or utility bills.
- Export your expenses for a specific date range in CSV or PDF format.
- View detailed weekly or monthly summary reports of your expenses, including total spending, top categories, and anomalies.
- Predict future spending patterns using advanced machine learning models for the next 30 days.
- Convert expenses between currencies, including cryptocurrencies, for seamless international tracking.
WalletWise transforms financial management into a convenient, intuitive, and efficient experience directly on Telegram!


## Functionalities

### Add/Record A New Spending
Use the /add command to log new spending. Choose a category (e.g., food, transport, shopping) and enter the amount. The bot confirms by saving and displaying the entered data.

### Add Shared Expenses With Friends
The /addGroup command allows you to record expenses shared with friends. Select a category, enter a comma-separated list of users along with the amount, and the bot updates the group's record.

### Display Spending Plots
Using /display, specify the start and end dates to view your expenses. The bot generates visualizations like bar graphs, pie charts, histograms, and box plots, offering insights into your spending patterns.

### Show Daily/Monthly Expenditure Summary
The /history command provides a detailed view of your spending history over a specified period, including personal and group expenses, helping you analyze past expenditures.

#### Clear All Records
Use /erase to delete all recorded spending data from your profile, effectively resetting your financial history when needed.

### Add/Manage Profile
The /profile command is used for profile management. Enter your email for verification, enabling you to update an existing profile or create a new one for accurate user identification.

### Show Owings/Borrowings
The /showOwings command tracks outstanding debts, both owed and owing. This feature simplifies managing finances when group expenses are involved.

### Settle Up Expenses
Use /settleUp to record payments made to others, clearing debts and updating owed amounts. This feature ensures transparency in group finances.

### Track Crypto Spendings
With /crypto, users can log and monitor cryptocurrency transactions. This feature integrates digital financial activities into your expense tracking.

### Set Budgets and Alerts
The /setBudget command allows you to set monthly or weekly budgets for specific categories, while /checkBudget helps track your remaining budget. Alerts are sent when you approach or exceed your limit.

### Predict Spendings Using ML Models
Use /predict to forecast future spending patterns using advanced machine learning models. This feature provides insights to help users manage their finances proactively.

### Set and Track Savings Goals
The /setGoal command enables users to define financial goals (e.g., saving for a trip), while /checkGoals monitors progress. Use /addSavings to add funds toward specific goals.

### Receive Recurring Expense Reminders
With /addRecurringExpense, users can set recurring expenses like rent or utility bills. The bot sends reminders before due dates, ensuring timely payments.

### Export Expenses as CSV or PDF
The /exportExpenses command lets users export their expense history for a specific date range in CSV or PDF format, providing flexibility for offline analysis or sharing reports.

### View Weekly/Monthly Summary Reports
The /weeklyReport and /monthlyReport commands generate detailed reports, including total spending, top categories, and anomalies, helping users stay informed about their financial habits.

### View Spending Trends
Use /trend to visualize your expense trends over time, offering insights into long-term financial behavior.

#### Currency Exchange
The /currencyConvert command provides real-time currency conversion rates, enabling users to manage international transactions or travel expenses easily.

These functionalities make WalletWise a comprehensive, intuitive, and efficient financial management tool, catering to diverse user needs.


---

## Previous version
This video is taken from the Project 2 of Group 93.
https://drive.google.com/drive/folders/1UH4dTulGGdwuYMUsUZozWx3M2cx7KV-c?usp=drive_link

## Updated version

OUR NEW VIDEO GOES HERE:
add here



## Getting Started
### Installation guide

The below instructions below can be followed to set-up a Telegram bot in a span of few minutes! This is your personal bot that replies when you chat with it. It would interact with the MongoDb database setup by us to store the data. No data will be stored on your local system.
- Install Python3 from [here](https://www.python.org/downloads/) and finish the required setup in the executable file.
- Install pip package manager for future downloads-
    ```bash
    $ python -m ensurepip --upgrade
    ```
- Upgrade the version of pip-
    ```
    $ python -m pip install --upgrade pip
    ```
- Create working directory named `walletwise` and go inside it
    ```bash
    $ mkdir walletwise
    $ cd walletwise
    ```
- Clone this repository from [here](https://github.com/firasat/walletwise) or use the following in GitBash
    ```bash
    $ git clone https://github.com/firasat/walletwise.git
    ```
- Install the required dependencies using the following-
	```bash
	pip3 install -r requirements.txt
	```
- Download and install the Telegram desktop application for your system from the following [site](https://desktop.telegram.org/)
- Once you login to your Telegram account, search for `BotFather` in Telegram. Click on `Start` and enter the following command to create a new bot:
	```bash
	/newbot
	```
- Follow the instructions on screen and choose a name for your bot. Post this, select a username for your bot that ends with `bot` (as per the instructions on your Telegram screen)

- BotFather will now confirm the creation of your bot and provide a TOKEN to access the Telegram API - copy this token for future use and keep it safe. 
- Paste the token copied in the above step in the config.py file under the `src` folder under ApiToken variable.
- In the Telegram app, search for your newly created bot by entering the username and open the same.

### Running the Algorithm Code
- Run the algorithm code in `src/main.py` using- 
    ```bash
    $ cd src
    $ python -m src.main
    ```
- A successful run will generate a message on your terminal that says `TeleBot: Started polling.`
- Post this, navigate to your bot on Telegram, enter the` /start` command and a menu will be displayed to help you with further acceptable commands.
- You can always use ` /help` to get the comman menu again. Enjoy tracking your expenses.

### Running publicly available bot:

If you want to run publicly hosted bot instead of creating and managing your own bot then got to :
```
http://t.me/tushar_wallet_bot
```
send message to the bot named `tushar_wallet_bot` and start managing your expanses using different functionalities.
(Note for Evaluator) If it is not running please ping a member of our team so that they can run it for you while you test it.

## Coverage Reports
<table class="index" data-sortable>
        <thead>
            <tr class="tablehead" title="Click to sort">
                <th class="name left" aria-sort="none" data-shortcut="n">Module</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="s">statements</th>
                <th aria-sort="none" data-default-sort-order="descending" data-shortcut="m">missing</th>
                <th class="right" aria-sort="none" data-shortcut="c">coverage</th>
            </tr>
        </thead>
        <tbody>
            <tr class="file">
                <td class="name left">src\add.py</td>
                <td>74</td>
                <td>5</td>
                <td class="right" data-ratio="69 74">93%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\add_group.py</td>
                <td>263</td>
                <td>116</td>
                <td class="right" data-ratio="147 263">56%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\config.py</td>
                <td>4</td>
                <td>4</td>
                <td class="right" data-ratio="0 4">0%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\display.py</td>
                <td>117</td>
                <td>94</td>
                <td class="right" data-ratio="23 117">20%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\display_calendar.py</td>
                <td>10</td>
                <td>10</td>
                <td class="right" data-ratio="0 10">0%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\erase.py</td>
                <td>20</td>
                <td>17</td>
                <td class="right" data-ratio="3 20">15%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\helper.py</td>
                <td>102</td>
                <td>42</td>
                <td class="right" data-ratio="60 102">59%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\history.py</td>
                <td>33</td>
                <td>12</td>
                <td class="right" data-ratio="21 33">64%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\main.py</td>
                <td>73</td>
                <td>73</td>
                <td class="right" data-ratio="0 73">0%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\plots.py</td>
                <td>322</td>
                <td>237</td>
                <td class="right" data-ratio="85 322">26%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\profile.py</td>
                <td>29</td>
                <td>1</td>
                <td class="right" data-ratio="28 29">97%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\pymongo_run.py</td>
                <td>7</td>
                <td>1</td>
                <td class="right" data-ratio="6 7">86%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\settle_up.py</td>
                <td>74</td>
                <td>74</td>
                <td class="right" data-ratio="0 74">0%</td>
            </tr>
            <tr class="file">
                <td class="name left">src\show_owings.py</td>
                <td>32</td>
                <td>32</td>
                <td class="right" data-ratio="0 32">0%</td>
            </tr>
        </tbody>
        <tfoot>
            <tr class="total">
                <td class="name left">Total</td>
                <td>1160</td>
                <td>718</td>
                <td class="right" data-ratio="442 1160">38%</td>
            </tr>
        </tfoot>
    </table>

---


## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[License Guidelines](https://github.com/firasat/walletwise/blob/main/LICENSE)

---


## Contribute

Please have a look at the [guidelines](https://github.com/firasat/walletwise/blob/main/CONTRIBUTING.md) before contributing.

---

## Authors
Current Authours
- Sravya Yepuri [Github](https://github.com/Shravsssss)
- Chirag Hegde [Github](https://github.com/Chirag-Hegde)
- Melika Ahmadi Ranjbar [Github](https://github.com/meliiwamd)
  
Previous Authors
- Boscosylvester Chittilapilly [Github](https://github.com/boscosylvester-john)
- Prasad Kamath [Github](https://github.com/kamathprasad9)
- Shlok Naik [Github](https://github.com/shlokio)
- Tushar Kini [Github](https://github.com/firasat)
- Ankur Banerji [Github](https://github.com/ankurbanerji3)

---

## Technology Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)


-----
