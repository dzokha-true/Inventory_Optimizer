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
    
    # Initilise the object
    def __init__(self):
        super().__init__()
        # Connects to the BusinessInventoryChecker database
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        # Assign the AccessDetails collection from LoginSystem database to variable called login_DB 
        self.data_base = client['CompanyDetails']
        self.received_order_DB = self.data_base['OrdersReceived']
        self.performance_DB = self.data_base['Performance']

    def order_received():
        
    
    def expected_inventory(num, cost):
        document = self.performance_DB.find_one({'num': 1})
        new_expected_inventory = document.get('expected_inventory', 0) + num * cost
        self.performance_DB.update_one({'num': 1}, {'$set': {'expected_inventory': new_expected_inventory}})
        
    def actual_inventory(num, cost):
        document = self.performance_DB.find_one({'num': 1})
        new_actual_inventory = document.get('actual_inventory', 0) + num * cost
        self.performance_DB.update_one({'num': 1}, {'$set': {'actual_inventory': new_actual_inventory}})
        
    def shrinkage():
        document = self.performance_DB.find_one({'num': 1})
        expected_inventory = document.get('expected_inventory', 0)
        actual_inventory = document.get('actual_inventory', 0)
        return expected_inventory - actual_inventory
        
    def shrinkage_percent():
        document = self.performance_DB.find_one({'num': 1})
        expected_inventory = document.get('expected_inventory', 0)
        actual_inventory = document.get('actual_inventory', 0)
        return ((expected_inventory - actual_inventory) / expected_inventory) * 100
        
    def writeoff(items, cost):
        document = self.performance_DB.find_one({'num': 1})
        new_writeoff = document.get('writeoff', 0) + num * cost
        self.performance_DB.update_one({'num': 1}, {'$set': {'writeoff': new_writeoff}})
        
    def reset_expected_inventory():
        document = self.performance_DB.find_one({'num': 1})
        self.performance_DB.update_one({'num': 1}, {'$set': {'expected_inventory': 0}})
    
    def reset_actual_inventory():
        document = self.performance_DB.find_one({'num': 1})
        self.performance_DB.update_one({'num': 1}, {'$set': {'actual_inventory': 0}})
        
    def reset_writeoff():
        document = self.performance_DB.find_one({'num': 1})
        self.performance_DB.update_one({'num': 1}, {'$set': {'writeoff': 0}})
        
    def place_order_to_csv():
        with open('received_order.csv', 'w', newline='') as csvfile:
            fieldnames = ['date', 'SKU', 'product_name', 'serial_id', 'cost', 'order_number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.place_order_DB.find():
                date = row.get('date')
                SKU = row.get('SKU')
                product_name = row.get('product_name')
                serial_id = row.get('serial_id')
                cost = row.get('cost')
                order_number = row.get('order_number')

            writer.writerow({'date': date, 'SKU': SKU, 'product_name': product_name, 'serial_id': serial_id, 'cost': cost, 'order_number': order_number})
        csvfile.close()

    def csv_to_place_order():
        if self.status != "Admin":
            print("You dont have access to this feature")
        else:
            with open('received_order.csv', newline='') as csvfile:
                myreader = csv.reader(csvfile)
            for row in myreader:  
                self.place_order_DB.insert_one({'date': row[0], 'SKU': row[1], 'product_name': row[2], 'serial_id': row[3], 'cost': row[4], 'order_number': row[5]})
            filename.close()
        
        
        
        
        
        