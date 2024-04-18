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
#import matplotlib.pyplot as plt
#from matplotlib.ticker import PercentFormatter
import HelperFunctions
from LoginSystem import LoginSystem
import numpy as np

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

class Product(LoginSystem):
    
    # initilse a constructor
    def __init__(self):
        self.status = "Admin"
        super().__init__()
        # Connects to the BusinessInventoryChecker database
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        # Assign the AccessDetails collection from LoginSystem database to variable called login_DB 
        self.data_base = client['CompanyDetails']
        self.product_DB = self.data_base['ProductInformation']
    
    def get_product_everything(self):
        cursor = self.product_DB.find({}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'stock': 1, 'cost': 1, 'inventory_value': 1, 'expected_sales': 1, 'SKU_class': 1})
        bold_start = "\033[1m"
        bold_end = "\033[0m"
        if cursor:
            print('\n')
            for document in cursor:
                print(f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                      f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                      f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                      f"Cost: {bold_start}{document.get('cost', 'N/A')}{bold_end} -- "
                      f"Inventory value: {bold_start}{document.get('inventory_value', 'N/A')}{bold_end} -- "
                      f"Expected sales: {bold_start}{document.get('expected_sales', 'N/A')}{bold_end} -- "
                      f"SKU class: {bold_start}{document.get('SKU_class', 'N/A')}{bold_end}")
            print('\n')
        else:
            print("There are no products! Try adding first.")
        
    def get_product_name(self):
        name = input("Please enter the name of the item you are searching for: ")
        document = self.product_DB.find_one({'product_name': name})
        bold_start = "\033[1m"
        bold_end = "\033[0m"
        print('\n')
        if document:
            print(f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                  f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                  f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                  f"Cost: {bold_start}{document.get('cost', 'N/A')}{bold_end} -- "
                  f"Inventory value: {bold_start}{document.get('inventory_value', 'N/A')}{bold_end} -- "
                  f"Expected sales: {bold_start}{document.get('expected_sales', 'N/A')}{bold_end} -- "
                  f"SKU class: {bold_start}{document.get('SKU_class', 'N/A')}{bold_end}")
            print('\n')
        else:
            print("No document found with product name: " + name)
                
    def get_product_SKU(self):
        SKU = HelperFunctions.SKU_Checker()
        document = self.product_DB.find_one({'SKU': SKU})
        bold_start = "\033[1m"
        bold_end = "\033[0m"
        print('\n')
        if document:
            print(f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                  f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                  f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                  f"Cost: {bold_start}{document.get('cost', 'N/A')}{bold_end} -- "
                  f"Inventory value: {bold_start}{document.get('inventory_value', 'N/A')}{bold_end} -- "
                  f"Expected sales: {bold_start}{document.get('expected_sales', 'N/A')}{bold_end} -- "
                  f"SKU class: {bold_start}{document.get('SKU_class', 'N/A')}{bold_end}")
            print('\n')
        else:
            print("No document found with SKU: " + SKU)
            
    def get_product_SKU_class(self):
        case = True
        while case:
            choice = input("Please enter the SKU class you want to display (A, B or C): ")
            if choice == 'A' or choice == 'B' or choice == 'C':
                case = False
            else:
                print("Please enter the correct letter!")
                
        cursor = self.product_DB.find({'SKU_class': choice}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'stock': 1, 'cost': 1, 'inventory_value': 1, 'expected_sales': 1, 'SKU_class': 1})
        bold_start = "\033[1m"
        bold_end = "\033[0m"
        if cursor:
            print('\n')
            for document in cursor:
                print(f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                      f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                      f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                      f"Cost: {bold_start}{document.get('cost', 'N/A')}{bold_end} -- "
                      f"Inventory value: {bold_start}{document.get('inventory_value', 'N/A')}{bold_end} -- "
                      f"Expected sales: {bold_start}{document.get('expected_sales', 'N/A')}{bold_end} -- "
                      f"SKU class: {bold_start}{document.get('SKU_class', 'N/A')}{bold_end}")
            print('\n')
        else:
            print("There is no product with the SKU class provided!")
        
    ###############################################################
            
    def pareto_chart(self): # FINISH THIS FUNCTION
        # Fetch the data from the MongoDB database
        cursor = self.product_DB.find({}, {'_id': 0, 'SKU': 1, 'inventory_value': 1})

        # Convert the cursor to a list for easier manipulation
        data_list = list(cursor)

        # Sort the data in descending order by inventory_value
        sorted_data = sorted(data_list, key=lambda x: x['inventory_value'], reverse=True)

        # Extract the SKUs and inventory_values into separate lists
        SKUs = [item['SKU'] for item in sorted_data]
        inventory_values = [item['inventory_value'] for item in sorted_data]

        # Calculate the cumulative percentage
        cum_percent = np.cumsum(inventory_values) / np.sum(inventory_values) * 100

        # Create the Pareto chart
        fig, ax1 = plt.subplots()

        # Create the bars representing individual values
        ax1.bar(SKUs, inventory_values, color='blue')
        ax1.set_ylabel('Inventory Value')

        # Create the line representing the cumulative total
        ax2 = ax1.twinx()
        ax2.plot(SKUs, cum_percent, color='red', marker='o')
        ax2.set_ylabel('Cumulative Percentage')

        # Set the x-axis labels to be the SKUs, rotated 90 degrees for readability
        plt.xticks(SKUs, rotation=90)

        # Save the plot to a file
        plt.savefig('pareto_chart.png', bbox_inches='tight')

        print("Pareto chart has been saved as 'pareto_chart.png'")

        # # range of dates
        # # define aesthetics for plot
        # color1 = 'steelblue'
        # color2 = 'red'
        # line_size = 4
        #
        # # create basic bar plot
        # fig, ax = plt.subplots()
        # ax.bar(df.index, df['count'], color=color1)
        #
        # # add cumulative percentage line to plot
        # ax2 = ax.twinx()
        # ax2.plot(df.index, df['cumperc'], color=color2, marker="D", ms=line_size)
        # ax2.yaxis.set_major_formatter(PercentFormatter())
        #
        # # specify axis colors
        # ax.tick_params(axis='y', colors=color1)
        # ax2.tick_params(axis='y', colors=color2)
        #
        # # display Pareto chart
        # plt.show()
        
    ###############################################################
        
    def product_to_csv(self):
        with open('product.csv', 'w', newline='') as csvfile:
            fieldnames = ['SKU', 'product_name', 'stock', 'cost', 'inventory_value', 'expected_sales', 'SKU_class']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.product_DB.find():
                SKU = row.get('SKU')
                product_name = row.get('product_name')
                stock = row.get('stock')
                cost = row.get('cost')
                inventory_value = row.get('inventory_value')
                expected_sales = row.get('expected_sales')
                SKU_class = row.get('SKU_class')

            writer.writerow({'SKU': SKU, 'product_name': product_name, 'stock': stock, 'cost': cost, 'inventory_value': inventory_value, 'expected_sales': expected_sales, 'SKU_class': SKU_class})
        csvfile.close()

    def csv_to_product(self):
        if self.status != "Admin":
            print("You dont have access to this feature")
        else:
            with open('product.csv', newline='') as csvfile:
                myreader = csv.reader(csvfile)
            for row in myreader:
                SKU_check = self.product_DB.find_one({'SKU': row[0]})
                if SKU_check:
                    self.product_DB.update_one({'SKU': row[0]}, {'$set': {'SKU': row[0], 'product_name': row[1], 'stock': row[2], 'cost': row[3], 'inventory_value': row[4], 'expected_sales': row[5], 'SKU_class': row[6]}})
                else:
                    self.product_DB.insert_one({'SKU': row[0], 'product_name': row[1], 'stock': row[2], 'cost': row[3], 'inventory_value': row[4], 'expected_sales': row[5], 'SKU_class': row[6]})
            filename.close()
        
    def add_product(self): # NEED TO CHANGE IT
        if self.status == 'Read':
            print("You dont have access to this feature")
        else:
            SKU = HelperFunctions.SKU_Checker()
            product_name = input("Please input the name of the product")
            stock = HelperFunctions.stock_Checker()
            order = HelperFunctions.check_order_number()
            cost = HelperFunctions.price_Checker()
            #inventory_value = # NEEDS TO BE ADDED
            #expected_sales = # NEEDS TO BE ADDED
            #SKU_class = # NEEDS TO BE ADDED
            SKU_check = self.product_DB.find_one({'SKU': SKU})
            if SKU_check:
                print("The product already exists! Try updating it instead")
            else:
                self.product_DB.insert_one({'SKU': SKU, 'product_name': product_name, 'stock': stock, 'order': order, 'cost': cost, 'inventory_value': inventory_value, 'expected_sales': expected_sales, 'SKU_class': SKU_class})
            
    def update_product(self): # NEED TO CHANGE IT
        if self.status == 'Read':
            print("You dont have access to this feature")
        else:
            SKU = HelperFunctions.SKU_Checker()
            product_name = input("Please input the name of the product")
            stock = HelperFunctions.stock_Checker()
            order = HelperFunctions.check_order_number()
            cost = HelperFunctions.price_Checker()
            #inventory_value = # NEEDS TO BE ADDED
            #expected_sales = # NEEDS TO BE ADDED
            #SKU_class = # NEEDS TO BE ADDED
            SKU_check = self.product_DB.find_one({'SKU': SKU})
            if SKU_check:
                self.product_DB.update_one({'SKU': SKU}, {'$set': {'SKU': SKU, 'product_name': product_name, 'stock': stock, 'order': order, 'cost': cost, 'inventory_value': inventory_value, 'expected_sales': expected_sales, 'SKU_class': SKU_class}})
            else:
                print("Product does not exist! Try adding the product first.")        
        
    def delete_product(self): # NEED TO CHANGE IT
        if self.status == "Read":
            print("You dont have access to this feature")
        else:
            SKU = HelperFunctions.SKU_Checker()
            product_name = input("Please input the name of the product")
            stock = HelperFunctions.stock_Checker()
            order = HelperFunctions.check_order_number()
            cost = HelperFunctions.price_Checker()
            #inventory_value = # NEEDS TO BE ADDED
            #expected_sales = # NEEDS TO BE ADDED
            #SKU_class = # NEEDS TO BE ADDED
            SKU_check = self.product_DB.find_one({'SKU': SKU})
            
            product_check = self.product_DB.find_one({'SKU': SKU, 'product_name': product_name, 'stock': stock, 'order': order, 'cost': cost, 'inventory_value': inventory_value, 'expected_sales': expected_sales, 'SKU_class': SKU_class})
            
            if product_check:
                production = self.product_DB.delete_one({'SKU': SKU, 'product_name': product_name, 'stock': stock, 'order': order, 'cost': cost, 'inventory_value': inventory_value, 'expected_sales': expected_sales, 'SKU_class': SKU_class})
            else:
                print("Transaction does not exist. Please add the transaction first.")
        
        
# adding a product
#input SKU, product_name
#stock = 0
#price = 0
#inventory_value = 0
#expected sales = ...
#SKU_class = 'C'
#check if already exists, return None # Later Error
#if it doesnt, add it

# editting later when GUI is done

# deleting
#check if none zero stock, and if none zero then return None
#else delete the data field

        
        

    
