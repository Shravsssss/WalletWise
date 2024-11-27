# WalletWise

# Version: 1.0.0
# Date Released: 2024-11-26 
# Authors: Sravya Yepuri, Chirag Hegde, Melika Ahmadi Ranjbar

# Licensed under the MIT License.
# You may obtain a copy of the License at

#     https://opensource.org/licenses/MIT

from pymongo import MongoClient


def get_database():
    """This is the get database function"""
    cs = "mongodb+srv://syepuri:syepuri@se-project3.0htqg.mongodb.net/?retryWrites=true&w=majority&appName=SE-Project3"
    client = MongoClient(cs)
    return client['telebot']


if __name__ == "__main__":
    dbname = get_database()
