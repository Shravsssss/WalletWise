from pymongo import MongoClient


def get_database():
    """This is the get database function"""
    connection_string = """mongodb+srv://syepuri:syepuri@se-project3.0htqg.mongodb.net/?retryWrites=true&w=majority&appName=SE-Project3"""
    client = MongoClient(connection_string)
    return client['telebot']


if __name__ == "__main__":  
    dbname = get_database()
