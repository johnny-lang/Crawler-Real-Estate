#!/usr/bin/python
import pprint
import json
from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.Thangdb

def insert(doc):
    db.Coll.insert(doc)
 
def check():
    #for i in range(0,db.Coll.count()):
     #   pprint.pprint(db.Coll.find()[i])
    return    
# db.Coll.find() la 1 list cua dictionary

