#!/usr/bin/python
import pprint
import json
from pymongo import MongoClient
client = MongoClient('localhost:27017')
db = client.Webdb

def unnecessary_info(doc):
    db.linking_page.insert(doc)

def necessary_info(doc):
    db.info_page.insert(doc)
    
 
