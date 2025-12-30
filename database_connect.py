#database_connect.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client['Student_Management']

user_collection = db['user']
student_collection = db['student']
