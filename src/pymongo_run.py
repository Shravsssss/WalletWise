import pymongo
from pymongo import MongoClient


def get_database():
    """This is the get database function"""
    connection_string = """mongodb+srv://meliiw_amd:Shaghayegh_69@cluster0.kmhof.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"""
    client = MongoClient(connection_string)

    return client['telebot']


if __name__ == "__main__":
    dbname = get_database()
