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
from Sales import Sales

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

class Place_Order(Sales):
    
    # Initilise the object
    def __init__(self):
        super().__init__()
        # Connects to the BusinessInventoryChecker database
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        # Assign the AccessDetails collection from LoginSystem database to variable called login_DB 
        self.data_base = client['CompanyDetails']
        self.place_order_DB = self.data_base['OrdersPlaced']
        
    def place_order(self):

        date_str = HelperFunctions.normal_date_checker()
        SKU = HelperFunctions.SKU_Checker()
        product_name = input("Please enter the product name: ")
        number_of_items = HelperFunctions.stock_Checker()
        cost = HelperFunctions.price_Checker()

        latest_order = self.place_order_DB.find_one(sort=[("order_number", -1)])
        if latest_order:
            new_order_number = latest_order['order_number'] + 1
        else:
            new_order_number = 1

        self.place_order_DB.insert_one({
            "date": order_date,
            "SKU": SKU,
            "product_name": product_name,
            "number_of_items": number_of_items,
            "cost": cost,
            "order_number": new_order_number
        })
        
        self.expected_inventory(number_of_items, cost)
        
    def update_order(self):

        date_str = HelperFunctions.normal_date_checker()
        SKU = HelperFunctions.SKU_Checker()
        product_name = input("Please enter the current product name: ")
        number_of_items = HelperFunctions.stock_Checker()
        cost = HelperFunctions.price_Checker()

        query = {
            "date": date_str,
            "SKU": SKU,
            "product_name": product_name,
            "number_of_items": number_of_items,
            "cost": cost
        }

        if self.place_order_DB.find_one(query) is None:
            print("Order not found.")
            return None

        print("Please enter the new details for the order:")
        new_date_str = HelperFunctions.normal_date_checker()
        new_SKU = HelperFunctions.SKU_Checker()
        new_product_name = input("Please enter the new product name: ")
        new_number_of_items = HelperFunctions.stock_Checker()
        new_cost = HelperFunctions.price_Checker()

        self.expected_inventory(new_number_of_items, new_cost)

        # Update the document.
        new_values = {
            "$set": {
                "date": new_date_str,
                "SKU": new_SKU,
                "product_name": new_product_name,
                "number_of_items": new_number_of_items,
                "cost": new_cost
            }
        }

        self.place_order_DB.update_one(query, new_values)
        
    def delete_order():
        
        date_str = HelperFunctions.normal_date_checker()
        SKU = HelperFunctions.SKU_Checker()
        product_name = input("Please enter the product name: ")
        number_of_items = HelperFunctions.stock_Checker()
        cost = HelperFunctions.price_Checker()
        
        query = {
            "date": date_str,
            "SKU": SKU,
            "product_name": product_name,
            "number_of_items": number_of_items,
            "cost": cost
        }
        self.place_order_DB.delete_one(query)
        self.expected_inventory(number_of_items, cost)
        
    def place_order_to_csv():
        with open('place_order.csv', 'w', newline='') as csvfile:
            fieldnames = ['date', 'SKU', 'product_name', 'number_of_items', 'cost', 'order_number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.place_order_DB.find():
                date = row.get('date')
                SKU = row.get('SKU')
                product_name = row.get('product_name')
                number_of_items = row.get('number_of_items')
                cost = row.get('cost')
                order_number = row.get('order_number')

            writer.writerow({'date': date, 'SKU': SKU, 'product_name': product_name, 'number_of_items': number_of_items, 'cost': cost, 'order_number': order_number})
        csvfile.close()

    def csv_to_place_order():
        if self.status != "Admin":
            print("You dont have access to this feature")
        else:
            with open('place_order.csv', newline='') as csvfile:
                myreader = csv.reader(csvfile)
            for row in myreader:
                
                latest_order = self.place_order_DB.find_one(sort=[("order_number", -1)])
                if latest_order:
                    new_order_number = latest_order['order_number'] + 1
                else:
                    new_order_number = 1
                
                self.place_order_DB.insert_one({'date': row[0], 'SKU': row[1], 'product_name': row[2], 'number_of_items': row[3], 'cost': row[4], 'order_number': new_order_number})
            filename.close()