# WalletWise: Installation and Running Guide

## Prerequisites

Before proceeding with the installation, ensure you have the following:

- **Python 3.8 or higher**: [Download Python](https://www.python.org/downloads/)
- **Pip**: Comes pre-installed with Python, but ensure it’s upgraded.
- **Git**: For cloning the repository. [Download Git](https://git-scm.com/downloads)
- **Telegram Desktop Application**: [Download Telegram](https://desktop.telegram.org/)

---

## Installation

### Step 1: Clone the Repository

1. Create a working directory:

    ```bash
    mkdir walletwise
    cd walletwise
    ```

2. Clone the WalletWise repository from GitHub:

    ```bash
    git clone https://github.com/Shravsssss/WalletWise.git
    ```

3. Navigate to the project directory:

    ```bash
    cd WalletWise
    ```

---

### Step 2: Install Python Dependencies

1. Upgrade pip:

    ```bash
    python -m pip install --upgrade pip
    ```

2. Install required dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

---

### Step 3: Set Up Your Telegram Bot

1. Open the Telegram application.
2. Search for `BotFather` and start a chat.
3. Use the command:

    ```bash
    /newbot
    ```

4. Follow the on-screen instructions to:
    - Set the name of your bot.
    - Get the bot's **API Token**.
5. Save the **API Token** provided by BotFather.

6. Update the `src/config.py` file with your bot token:
    - Open the file and locate the `ApiToken` variable.
    - Paste your token as the value.

---

### Step 4: Run the Application

1. Navigate to the `src` directory:

    ```bash
    cd src
    ```

2. Start the WalletWise bot:

    ```bash
    python -m main
    ```

3. Once started, you’ll see the message:

    ```plaintext
    TeleBot: Started polling.
    ```

4. Open Telegram, search for your bot (using the username you set with BotFather), and start interacting with it using the `/start` command.

---

## Publicly Hosted Bot (Optional)

If you don’t want to host the bot locally, you can use the publicly available bot:

1. Open Telegram and search for `walletwise_bot`.
2. Start interacting with the bot by sending `/start`.

---

## Testing the Application

1. To ensure the project is working correctly, run the test suite:

    ```bash
    pytest test/ -v
    ```

2. View the coverage report to confirm functionality.

---

## Common Commands for WalletWise

- `/start`: Start interacting with the bot.
- `/help`: View a list of available commands.
- `/add`: Add a new expense.
- `/setBudget`: Set a budget for a specific category.
- `/checkBudget`: Check remaining budget.
- `/crypto`: Record cryptocurrency transactions.
- `/addRecurringExpense`: Set a recurring expense.
- `/monthlyReport`: View a detailed monthly summary report.

For a complete list of commands, use `/help` in the bot.

---

## Notes

- Ensure your Python version is compatible (3.8 or higher).
- Keep your bot token secure and confidential.
- MongoDB is required for storing data when hosting locally. Ensure it’s set up if running WalletWise on your machine.

---

For more details, visit the [WalletWise GitHub Repository](https://github.com/Shravsssss/WalletWise).
