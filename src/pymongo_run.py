import pymongo
from pymongo import MongoClient


def get_database():
    """This is the get database function"""
    connection_string = """mongodb+srv://Firasat:GooglePixel@walletbuddy.hkpji.mongodb.net/WalletBuddy"""
    client = MongoClient(connection_string)
    client = pymongo.MongoClient("mongodb+srv://<username>:<password>@walletbuddy.hkpji.mongodb.net/<dbname>?retryWrites=true&w=majority", ssl=True)

    return client['telebot']



if __name__ == "__main__":  
    dbname = get_database()
