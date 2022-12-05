from pymongo import MongoClient


def get_database():
    """This is the get database function"""
    connection_string = """mongodb+srv://shlokio:sLA3uByHAl844tQ5@cluster0.y9kiowx.mongodb.net/test"""
    client = MongoClient(connection_string)
    return client['telebot']


if __name__ == "__main__":  
    dbname = get_database()
