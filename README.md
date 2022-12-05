# WalletBuddy
> This is a requirement for NCSU's CSC510 Software Engineering Course project 2 for Group 10.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7179471.svg)](https://doi.org/10.5281/zenodo.7179471)
![GitHub pull requests](https://img.shields.io/github/issues-pr/tusharkini/WalletBuddy)
[![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![GitHub repo size](https://img.shields.io/github/repo-size/smanishs175/WalletBuddy)](https://github.com/smanishs175/WalletBuddy/)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/tusharkini/WalletBuddy?color=purple)
[![GitHub contributors](https://img.shields.io/github/contributors/tusharkini/WalletBuddy)](https://github.com/tusharkini/WalletBuddy/graphs/contributors/)
![GitHub issues](https://img.shields.io/github/issues/tusharkini/WalletBuddy?color=teal)
![GitHub closed issues](https://img.shields.io/github/issues-closed/tusharkini/WalletBuddy?color=aqua)
[![Platform](https://img.shields.io/badge/Platform-Telegram-blue)](https://desktop.telegram.org/)
[![GitHub forks](https://img.shields.io/github/forks/tusharkini/WalletBuddy?style=social)](https://github.com/tusharkini/WalletBuddy/network/members)
[![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/tusharkini/WalletBuddy/Node.js%20CI?event=push)](https://github.com/tusharkini/WalletBuddy/actions)

<hr>

## Goal

> Design a dynamic application to assist a person in effectively managing and tracking his or her expenses on a regular basis.
---

## Motivation
> Manually trying to keep a track of the expenses and dividing the amount among a group (for group expenses) is a highly time-consuming task. This application will aid the user to efficiently track and therefore manage all the expenses, along with planning any expenditure in the future.

## Features

WalletBuddy is an easy-to-use Telegram Bot that assists you in recording your daily expenses on a local system without any hassle.
With simple commands, this bot allows you to:
- Add/Record a new spending 
- Add shared expenses with friends
- Show the sum of your expenditure for the current day/month
- Display your spendings plot : All expenses, Category expenses, Group Expenses
- Clear/Erase all your records

### Components
The components for the system are-
- Frontend- It is made using python and telebot to import the functionalities on the telegram applicaton.

- Backend- JSON objects and MongoDb to maintain the data for implementing this project.

## Previous version
https://user-images.githubusercontent.com/21088141/194785646-d05f864c-af1e-42f3-b7a1-b68aef4c8fa9.mp4

## Updated version

Our new video will come here

## Installation guide

The below instructions can be followed in order to set-up this bot at your end in a span of few minutes! Let's get started:

1. Set up your own server for deployment.

2. This installation guide assumes that you have already installed Python (Python3 would be preferred) and setup your own server.

3. Install git and add your account details using terminal.

4. Clone this repository to your local system at a suitable directory/location of your choice

5. Start a terminal session, and navigate to the directory where the repo has been cloned

6. Run the following command to install the required dependencies:
```
  pip3 install -r requirements.txt
```
7. Download and install the Telegram desktop application for your system from the following site: https://desktop.telegram.org/

8. Once you login to your Telegram account, search for "BotFather" in Telegram. Click on "Start" --> enter the following command:
```
  /newbot
```
9. Follow the instructions on screen and choose a name for your bot. Post this, select a username for your bot that ends with "bot" (as per the instructions on your Telegram screen)

10. BotFather will now confirm the creation of your bot and provide a TOKEN to access the HTTP API - copy this token for future use.

11. Paste the token copied in step 8 in the config.ini file under settings in ApiToken variable.

12. In the Telegram app, search for your newly created bot by entering the username and open the same. Once this is done, go back to the terminal session. Navigate to the directory containing the "main" folder inside your application code:
```
  run python3 main/main py
```
13. A successful run will generate a message on your terminal that says "TeleBot: Started polling." 

14. Post this, navigate to your bot on Telegram, enter the "/start" or "/menu" command, and you are all set to track your expenses!

## Running publicly available bot:

If you want to run publicly hosted bot then got to :
```
  <!-- https://t.me/niharrao_bot -->
  Public link goes here
```
send message to the bot named "sebot" and start managing your expanses using different functionalities.


## Coverage Reports
<table class="coverage-summary">
<thead>
<tr>
   <th data-col="file" data-fmt="html" data-html="true" class="file">File</th>
   <th data-col="pic" data-type="number" data-fmt="html" data-html="true" class="pic"></th>
   <th data-col="statements" data-type="number" data-fmt="pct" class="pct">Statements</th>
   <th data-col="statements_raw" data-type="number" data-fmt="html" class="abs"></th>
   <th data-col="lines" data-type="number" data-fmt="pct" class="pct">Lines</th>
   <th data-col="lines_raw" data-type="number" data-fmt="html" class="abs"></th>
</tr>
</thead>
<tbody><tr>
	<td class="file low" data-value="middleware">middleware</td>
	<td data-value="29.54" class="pic low">
	<div class="chart"><div class="cover-fill" style="width: 29%"></div><div class="cover-empty" style="width: 71%"></div></div>
	</td>
	<td data-value="--" class="pct low">--</td>
	<td data-value="--" class="abs low">--</td>
	<td data-value="--" class="pct low">--</td>
	<td data-value="--" class="abs low">--</td>
	</tr>

<tr>
	<td class="file medium" data-value="models">models</td>
	<td data-value="--" class="pic medium">
	<div class="chart"><div class="cover-fill" style="width: 71%"></div><div class="cover-empty" style="width: 29%"></div></div>
	</td>
	<td data-value="--" class="pct medium">--</td>
	<td data-value="--" class="abs medium">--</td>
	<td data-value="--" class="pct medium">--</td>
	<td data-value="--" class="abs medium">--</td>
	</tr>

<tr>
	<td class="file low" data-value="routes">routes</td>
	<td data-value="--" class="pic low">
	<div class="chart"><div class="cover-fill" style="width: 30%"></div><div class="cover-empty" style="width: 70%"></div></div>
	</td>
	<td data-value="--" class="pct low">--</td>
	<td data-value="--" class="abs low">--</td>
	<td data-value="--" class="pct low">--</td>
	<td data-value="--" class="abs low">--</td>
	</tr>

</tbody>
</table>

---


## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[License Guidelines](https://github.com/boscosylvester-john/parttimeScheduler/blob/main/LICENSE.md)

---


## Contribute

Please have a look at the [guidelines](https://github.com/boscosylvester-john/se_hw_LuaToPython/blob/main/CONTRIBUTING.md) before contributing.

---

## Authors

- Boscosylvester Chittilapilly [Github](https://github.com/boscosylvester-john)
- Prasad Kamath [Github](https://github.com/kamathprasad9)
- Shlok Naik [Github](https://github.com/shlokio)
- Tushar Kini [Github](https://github.com/tusharkini)
- Ankur Banerji [Github](https://github.com/ankurbanerji3)

---