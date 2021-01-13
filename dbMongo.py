from pymongo import MongoClient
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient['TodoList']
mycol = db['test']









