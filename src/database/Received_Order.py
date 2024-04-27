import sys
import os
import bcrypt
import random
from urllib.parse import quote_plus
from time import ctime
import subprocess
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from datetime import date
import re
from Place_Order import Place_Order

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

class Received_Order(Place_Order):
    
    def __init__(self):
        super().__init__()
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.received_order_DB = self.data_base['OrdersReceived']
















    
    def expected_inventory(num, cost):
        # range of dates
        # add a date
        document = self.performance_DB.find_one({'num': 1})
        new_expected_inventory = document.get('expected_inventory', 0) + num * cost
        self.performance_DB.update_one({'num': 1}, {'$set': {'expected_inventory': new_expected_inventory}})
        
        
        
        
        
        
    def actual_inventory(num, cost):
        # range of dates
        #add a date
        document = self.performance_DB.find_one({'num': 1})
        new_actual_inventory = document.get('actual_inventory', 0) + num * cost
        self.performance_DB.update_one({'num': 1}, {'$set': {'actual_inventory': new_actual_inventory}})
        
        
        
        
        
        
    def shrinkage():
        # range of dates
        # add a date
        document = self.performance_DB.find_one({'num': 1})
        expected_inventory = document.get('expected_inventory', 0)
        actual_inventory = document.get('actual_inventory', 0)
        return expected_inventory - actual_inventory
        
        
        
        
        
        
    def shrinkage_percent():
        # range of dates
        # Add a date
        document = self.performance_DB.find_one({'num': 1})
        expected_inventory = document.get('expected_inventory', 0)
        actual_inventory = document.get('actual_inventory', 0)
        return ((expected_inventory - actual_inventory) / expected_inventory) * 100
        
        
        
        
        
        
    def writeoff(items, cost):
        # range of dates
        # Add a date
        document = self.performance_DB.find_one({'num': 1})
        new_writeoff = document.get('writeoff', 0) + num * cost
        self.performance_DB.update_one({'num': 1}, {'$set': {'writeoff': new_writeoff}})
        

   
        
        


