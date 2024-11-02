# WalletWise
> This is a requirement for NCSU's CSC510 Software Engineering Course project 2 for Group 93.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/880744201.svg)](https://doi.org/10.5281/zenodo.14027332)
![GitHub open issues](https://img.shields.io/github/issues-raw/MFirasatHussain/WalletWise)
![GitHub closed issues](https://img.shields.io/github/issues-closed/MFirasatHussain/WalletWise)
<hr>

## Delta from Project 1
- **Tracking Crypto Spendings:** In our current project, "WalletWise," we have introduced a feature to track cryptocurrency transactions and spending. This new functionality enhances the application's ability to manage and analyze digital financial activities, catering to the growing popularity of cryptocurrencies.

- **Predicting Spendings Using ML Models:** We've leveraged machine learning algorithms to predict future spending patterns. This predictive functionality helps users better manage their finances by providing insights based on historical data, allowing for more informed financial planning.

- **Currency Exchange:** The addition of a currency exchange feature provides users with the ability to convert between different currencies including cryptocurrencies. This is especially useful for users who engage in international transactions or travel, ensuring they can manage and track their expenses in multiple currencies seamlessly.

These new features significantly enhance the functionality of WalletWise, making it a more comprehensive financial management tool compared to the first version of the project.


## Goal

> Design a dynamic application to assist a person in effectively managing and tracking his or her expenses on a regular basis using the popular Telegram API
---

## Motivation
> Manually trying to keep a track of the expenses and dividing the amount among a group (for group expenses) is a highly time-consuming task. Many standalone apps can be installed on the mobile but they take up additional space and need the user to open and enter the spendings in it. This application will aid the user to efficiently track and therefore manage all the expenses with help of simple commands in the popularily used Telegram App. No need to install any additional app, use what you are using already to track expenses.

## Features

walletwise is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.
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
Use the `/add` command to log new spending. You will choose a category such as food, transport, or shopping, and then enter the amount. The bot confirms by saving and displaying the entered data.

### Add Shared Expenses With Friends
The `/addGroup` command allows you to record expenses shared with friends. After selecting a category and entering a comma-separated list of users along with the amount, the expense is added to the group's record.

### Display Spending Plots
Using `/display`, specify the start and end dates to view your expenses. The bot shows various visualizations such as bar graphs, pie charts, histograms, and box plots. You will then choose whether to view these charts with options "Yes" and "No".

### Show Daily/Monthly Expenditure Summary
The `/history` command provides a detailed view of your spending history over a specified period, including both personal and group expenses.

### Clear All Records
Use `/erase` to delete all recorded spending data from your profile, effectively resetting your financial history.

### Add/Manage Profile
The `/profile` command is used for profile management. You will enter your email, which the application verifies, to either update your existing profile or add a new one to the database. This step is crucial for identifying users in shared expenses.

### Show Owings/Borrowings
The `/showOwings` command helps track outstanding debts—both owed and owing. This function is vital for managing finances when group expenses are involved.

### Settle Up Expenses
With `/settleUp`, you can record payments made to others, clearing debts recorded in the bot. This function is used to keep track of repayments and update the owed amounts accordingly.

### Track Crypto Spendings
The `/trackCrypto` command enables users to log and monitor their cryptocurrency transactions. This feature helps manage and analyze digital financial activities seamlessly.

### Predict Spendings Using ML Models
Use `/predictSpendings` to forecast future spending patterns using sophisticated machine learning models. This feature provides insights based on historical data to help with financial planning.

### Currency Exchange
The `/exchange` command offers real-time currency conversion rates, allowing users to manage expenses in different currencies. This tool is particularly useful for international transactions or travel.


---

## Previous version
This video is taken from the Project 1 of Group 10.
https://user-images.githubusercontent.com/54414375/205833191-c314e58c-16da-4c61-94e0-0fe60888c595.mp4

## Updated version

OUR NEW VIDEO GOES HERE



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
