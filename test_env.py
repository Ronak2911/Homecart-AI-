from pymongo import MongoClient
import certifi

uri = "mongodb+srv://admin:admin123@home-cluster.uyfw3kj.mongodb.net/home_db?tls=true"

client = MongoClient(uri, tlsCAFile=certifi.where())
print(client.list_database_names())
