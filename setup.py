from setuptools import setup, find_packages

setup(
    name='WalletBuddy',
    version='1.0',
    description="""An easy to use Telegram Bot to track 
        | everyday expenses with your friends""",
    author='Boscosylvester, Tushar, Shlok, Prasad, Ankur',
    scripts=['src/main.py'],
    packages=find_packages()
)
