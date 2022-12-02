from pymongo import MongoClient
 
 
def get_database():
    CONNECTION_STRING = "mongodb+srv://shlokio:sLA3uByHAl844tQ5@cluster0.y9kiowx.mongodb.net/test"
    client = MongoClient(CONNECTION_STRING)
    return client['telebot']
 
if __name__ == "__main__":  
   dbname = get_database()
