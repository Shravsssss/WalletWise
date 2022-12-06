# WalletBuddy2.0
> This is a requirement for NCSU's CSC510 Software Engineering Course project 2 for Group 10.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.572729933.svg)](https://doi.org/10.5281/zenodo.572729933)
![GitHub pull requests](https://img.shields.io/github/issues-pr/tusharkini/WalletBuddy)
[![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![GitHub repo size](https://img.shields.io/github/languages/code-size/tusharkini/WalletBuddy)](https://img.shields.io/github/languages/code-size/tusharkini/WalletBuddy)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/tusharkini/WalletBuddy?color=purple)
[![GitHub contributors](https://img.shields.io/github/contributors/tusharkini/WalletBuddy)](https://github.com/tusharkini/WalletBuddy/graphs/contributors/)
![GitHub issues](https://img.shields.io/github/issues/tusharkini/WalletBuddy?color=teal)
![GitHub closed issues](https://img.shields.io/github/issues-closed/tusharkini/WalletBuddy?color=aqua)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
[![GitHub forks](https://img.shields.io/github/forks/tusharkini/WalletBuddy?style=social)](https://github.com/tusharkini/WalletBuddy/network/members)
![example event parameter](https://github.com/tusharkini/WalletBuddy/actions/workflows/tests.yaml/badge.svg?event=push)
<hr>

## Delta from Project 1
- To make the system more scalable over time, we have migrated the earlier database system from a file based system to a distribute and scalable database- MongoDb.
- Analysis showed that for smaller database with relatively new users and less users, MongoDB would take more time due to access to the server than a small file system. In the long run when the number of records and also the number of users increases, MongoDB would be the clear winner. It would not matter if the data is 10X, 100X or 1000X, MondoDB can handle it due to its non relational and distributed design.
- Also the file system was not encrypted which made the data vulnerable to attacks, MongoDB eradicates this problem.
- 2 more types of plots namely box plot and pie chart is added to give a better understanding to the user about the expenses.
- An important functionality was missing in the Project 1 version of WalletBuddy, where the users did not have a way to look at what a user owes other or is owed by others. This has been taken care of in this version with command `/showOwings`.
- Also we have added another functionality where there is an option for the user to pay up/ settle up the expenses that are owed to other users. After paying them, a record can be kept to keep track of that transaction and the amount owed is reduced. The amount owed entry is deleted after the whole amount is payed back. The comman used is `/settleUp`.
- In project 1 our group had not used any code formatter. We have now used Pylint for the same.
- In project 1 our group had not used a style checker and in this project we have used pycodestyle as a style checker to conform with the PEP8 coding conventions.
- In project 1 our group had not used any automated documentation generator. This time we have used `pdoc3` to generate documentation using the docstrings written during development.
- For project 1 some important tests were failing in Github Actions, but this time we have got the tests to work on every push.

## Goal

> Design a dynamic application to assist a person in effectively managing and tracking his or her expenses on a regular basis using the popular Telegram API
---

## Motivation
> Manually trying to keep a track of the expenses and dividing the amount among a group (for group expenses) is a highly time-consuming task. Many standalone apps can be installed on the mobile but they take up additional space and need the user to open and enter the spendings in it. This application will aid the user to efficiently track and therefore manage all the expenses with help of simple commands in the popularily used Telegram App. No need to install any additional app, use what you are using already to track expenses.

## Features

WalletBuddy is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.
With simple commands, this bot allows you to:
- Add/Record a new spending 
- Add shared expenses with friends
- Show the sum of your expenditure for the current day/month
- Display your spendings plot : All expenses, Category expenses, Group Expenses
- Clear/Erase all your records
- Add/Manage Profile
- Show Owings/ Borrowings
- Settle up expenses


## Functionalities

### Add/Record A New Spending
The command to be entered is `/add`. This prompts the user to first select a category such as food, transport, shopping, etc, and then enter the amount spent on the selected category. After the successful data entry the bot replies with the data entered into the database.

### Add Shared Expenses With Friends
Upon entering the command `/addGroup`, the user will be able to add expenditures carried out in a group of people. First, the user will be prompted to select a category out of food, transport, etc, then a comma separated list of users is to be entered followed by the amount spent in the group expense.

### Display Spendings Plot
Here, the user will be prompted to enter the start and end date upon entering the command `/display`, and will be able to successfully view and analyze all the expenditures carried out in the mentioned dates. Apart from just the numbers, several plots will be shown consisting of bar graphs, pie charts, histograms and box plots.The user is then asked if he/she wants to view the expense charts with two choices "Yes" and "No".
### Show the sum of your expenditure for the current day/month
The command `/history` will show the user an extensive history of all the expenses he/she has carried out in the date range mentioned by the user. This includes both the individual and group expenses.

### Clear/Erase All Records
The command `/erase` will simply delete the complete history of the user.

### Add/Manage Profile
Here, the user will be asked for his/her email that will be validated by the application followed by a decision that the user is already existing or adding the new user to the database. The command used here is `/profile`. This step is essential so that other users can add shared expenses using the email as an identifier.

### Show Owings/ Borrowings
We can use  this added functionality to find what amount we own some other user or what other users owe me. The command for this functionality is `/showOwings`. This is an important functionality to keep track when group expenses are added and money exchange is to take place.

### Settle up expenses
We use this functionality where we can settle up the ammount what we owe to other users. By using this command `/settleUp` we can add a transaction that nullifies the amount that we owe any specific user. This is to be used when we actually pay the person and keep a record with this telegram bot.

---

## Previous version
This video is taken from the Project 1 of Group 18.
https://user-images.githubusercontent.com/21088141/194785646-d05f864c-af1e-42f3-b7a1-b68aef4c8fa9.mp4

## Updated version

OUR NEW VIDEO GOES HERE
https://user-images.githubusercontent.com/54414375/205833191-c314e58c-16da-4c61-94e0-0fe60888c595.mp4

Please follow this link for better quality audio: https://github.com/tusharkini/WalletBuddy/blob/main/project2-showcase.mp4


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
- Create working directory named `WalletBuddy` and go inside it
    ```bash
    $ mkdir WalletBuddy
    $ cd WalletBuddy
    ```
- Clone this repository from [here](https://github.com/tusharkini/WalletBuddy) or use the following in GitBash
    ```bash
    $ git clone https://github.com/tusharkini/WalletBuddy.git
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

[License Guidelines](https://github.com/tusharkini/WalletBuddy/blob/main/LICENSE)

---


## Contribute

Please have a look at the [guidelines](https://github.com/tusharkini/WalletBuddy/blob/main/CONTRIBUTING.md) before contributing.

---

## Authors

- Boscosylvester Chittilapilly [Github](https://github.com/boscosylvester-john)
- Prasad Kamath [Github](https://github.com/kamathprasad9)
- Shlok Naik [Github](https://github.com/shlokio)
- Tushar Kini [Github](https://github.com/tusharkini)
- Ankur Banerji [Github](https://github.com/ankurbanerji3)

---

## Technology Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)


-----
