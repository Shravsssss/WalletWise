from pymongo import MongoClient


def get_database():
    """This is the get database function"""
    connection_string = """mongodb+srv://Firasat:GooglePixel@walletbuddy.hkpji.mongodb.net/WalletBuddy"""
    client = MongoClient(connection_string)
    return client['telebot']


if __name__ == "__main__":  
    dbname = get_database()
