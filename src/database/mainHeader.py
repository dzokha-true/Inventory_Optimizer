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
from datetime import datetime

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)
  
# NEEDS TO BE DELETED AT THE END (USED FOR CORRECTING THE PROGRAM WHEN USERS DATA NEEDS TO BE RESETED)
def testing(username, password):
    URI = "mongodb+srv://" + "ReadWrite" + ":" + "ReadWrite" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
    client = MongoClient(URI, server_api=ServerApi('1'))
    DB = client['LoginSystem']
    users = DB['AccessDetails']
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    users.insert_one({'username': username, 'password': hashed_password, 'status': "Admin"})
    return True
# ABOVE NEEDS TO BE DELETED AT THE END (USED FOR CORRECTING THE PROGRAM WHEN USERS DATA NEEDS TO BE RESETED)

def passwordChecker():
    case = True
    while case:
        password = input("Enter password: ")
        capital = False
        special = False
        number = False
        
        if len(password) < 8:
            print("Password has to be atleast 8 characters long")
        for x in password:
            if x in str(numbers):
                number = True
            if x not in str(numbers) and x not in letters and x not in capitals:
                special = True
            if x in capitals:
                capital = True
        
        if capital == False:
            print("Your password has to contain capital letter")
        if special == False:
            print("Your password has to contain special character")
        if number == False:
            print("Your password has to contain a number")

        if capital == True and special == True and number == True and len(password) >= 8:
            case = False
            
        capital = False
        special = False
        number = False
    
    return password

def statuscheck():
        statusCheck = input("Write code according to your priveledges (should be given by the company): ")
        if statusCheck == "ReadWrite":
            return register(username, password, "RW")
        elif statusCheck == "Admin":
            return register(username, password, "Admin")
        elif statusCheck == "Read":
            return register(username, password, "R")
        else:
            print("You don't have any priveledges!")
            sys.exit(0)
            
def LoginSystem():
    
    URI = "mongodb+srv://" + "Read" + ":" + "Read" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
    client = MongoClient(URI, server_api=ServerApi('1'))
    DB = client['LoginSystem']
        
    choice = input("Do you have an account? (yes/no): ").lower()
        
    case = True
    capital = False
    special = False
    number = False
    if choice == "no":
        username = input("Enter username: ")
    
        username_check = True
        while username_check:
            user_check = DB.AccessDetails.find_one({'username': username})
            if user_check:
                print("Username already exists, try another username!")
                username = input("Enter username: ")
            else:
                username_check = False
                
        password = passwordChecker()
        return statuscheck()

    elif choice == "yes":
        username = input("Enter username: ")
        password = input("Enter password: ")
        return login(username, password)
    else:
        print("Please enter 'yes' or 'no'")
        return LoginSystem()
    return False
        
        
def register(username, password, status):
    URI = "mongodb+srv://" + "ReadWrite" + ":" + "ReadWrite" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
    client = MongoClient(URI, server_api=ServerApi('1'))
    DB = client['LoginSystem']
        
    users = DB['AccessDetails']
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    users.insert_one({'username': username, 'password': hashed_password, 'status': status})
    return status


def login(username, password):
    URI = "mongodb+srv://" + "Read" + ":" + "Read" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
    client = MongoClient(URI, server_api=ServerApi('1'))
    DB = client['LoginSystem']
        
    users = DB['AccessDetails']
    user_check = users.find_one({'username': username})
    if user_check:
        attempts = 0
        while attempts < 5:
            if bcrypt.checkpw(password.encode('utf8'), user_check['password']):
                    return user_check['status']
            else:
                attempts += 1
                print("Your password is incorrect. Please try again. You have " + str((5 - attempts)) + " attempts left.")
                password = input("Try the password again: ")
        if attempts == 5:
            print("You have exceeded the maximum number of attempts. Please try again later.")
            sys.exit(0)
    else:
        print("User does not exist. You need to register for an account.")
        
        username = input("Enter username: ")
        
        username_check = True
        while username_check:
            user_check = users.find_one({'username': username})
            if user_check:
                print("Username already exists, try another username!")
                username = input("Enter username: ")
            else:
                username_check = False
            
        passwordChecker()
        return statuscheck()


class Product():
    
# Admin --> Admin --> vug << Testing123!
# ReadWrite --> RW --> testing << Testing123!
# Read --> R --> checking  << Testing123!

    def __init__(self, statuses):
        self.status = statuses
        if self.status == "Admin":
            username = "Admin"
            password = "Admin"
        elif self.status == "RW":
            username = "ReadWrite"
            password = "ReadWrite"
        else:
            username = "Read"
            password = "Read"

        URI = "mongodb+srv://" + username + ":" + password + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        self.data_base = client['BusinessInverntoryChecker']
        client.admin.command('ping')


    def add_product(self, SKU, product_name, stock): 
        if self.status == "R":
            print("You dont have access to add any products")
            return None
        else:
            products = self.data_base['Product']
            product_check = products.find_one({'product_name': product_name})
            product_SKU_check = products.find_one({'SKU': SKU})
            if product_check:
                print("Product already exists. Please update the quantity instead.")
            elif product_SKU_check:
                print("A product with the SKU inputted already exists. Please upate the quantity instead.") 
            else:
                product = products.insert_one({'SKU': SKU, 'product_name': product_name, 'stock': int(stock)})
                print("You have successfully added the product!")

    def update_product_usingName(self, product_name, stock):
        if self.status == "R":
            print("You dont have access to add any products")
            return None
        else:
            products = self.data_base['Product']
            product_check = products.find_one({'product_name': product_name})
            if product_check:
                product = products.update_one({'product_name': product_name}, {'$set': {'stock': int(stock)}})
                print("The product has successfully been updated!")
            else:
                print("Product does not exist. Please add the product first.")

    def update_product_usingSKU(self, SKU, stock):
        if self.status == "R":
            print("You dont have access to add any items")
            return None
        else:
            products = self.data_base['Product']
            product_check = products.find_one({'SKU': SKU})
            if product_check:
                product = products.update_one({'SKU': SKU}, {'$set': {'stock': int(stock)}})
                print("The product has successfully been updated!")
            else:
                print("Product does not exist. Please add the product first.")

    def delete_product_usingName(self, product_name):
        if self.status == "R":
            print("You dont have access to add any items")
            return None
        else:
            products = self.data_base['Product']
            product_check = products.find_one({'product_name': product_name})
            if product_check:
                product = products.delete_one({'product_name': product_name})
                print("You have successfully deleted a product!")
            else:
                print("Product does not exist. Please add the Product first.")
            
    def delete_product_usingSKU(self, SKU):
        if self.status == "R":
            print("You dont have access to add any items")
            return None
        else:
            products = self.data_base['Product']
            product_check = products.find_one({'SKU': SKU})
            if product_check:
                product = products.delete_one({'SKU': SKU})
                print("You have successfully deleted a product!")
            else:
                print("Product does not exist. Please add the product first.")

    def get_product_everything(self):
        products = self.data_base['Product']
        cursor = products.find({}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'stock': 1})
        bold_start = "\033[1m"
        bold_end = "\033[0m"
        print('\n')
        for document in cursor:
            print(f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                  f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                  f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end}")
        print('\n')
        
    def get_product_name(self, name):
        products = self.data_base['Product']
        document = products.find_one({'product_name': name})
        bold_start = "\033[1m"
        bold_end = "\033[0m"
        if document:
            print(f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                  f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                  f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end}")
        else:
            print("No document found with product name: " + name)
                
    def get_product_SKU(self, SKU):
        products = self.data_base['Product']
        document = products.find_one({'SKU': SKU})
        bold_start = "\033[1m"
        bold_end = "\033[0m"
        if document:
            print(f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                  f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                  f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end}")
        else:
            print("No document found with SKU: " + SKU)




class Transaction():
    
    def __init__(self, statuses):
        self.status = statuses
        if self.status == "Admin":
            username = "Admin"
            password = "Admin"
        elif self.status == "RW":
            username = "ReadWrite"
            password = "ReadWrite"
        else:
            username = "Read"
            password = "Read"

        URI = "mongodb+srv://" + username + ":" + password + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        self.data_base = client['BusinessInverntoryChecker']
        client.admin.command('ping')

    def get_transaction_everything_day(self, date):
        transactions = self.data_base['Transaction']
        cursor = transactions.find({'date': date})
        results = list(cursor)
        if len(results) == 0:
            print("There are no transactions for the date inputted")
        else:
            bold_start = "\033[1m"
            bold_end = "\033[0m"
            print('\n')
            for document in results:  # Use 'results' instead of 'cursor'
                print(f"Date: {bold_start}{document.get('date', 'N/A')}{bold_end} -- "
                      f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                      f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                      f"Transaction Type: {bold_start}{document.get('transaction_type', 'N/A')}{bold_end} -- "
                      f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                      f"Price: {bold_start}{document.get('price', 'N/A')}{bold_end}")
            print('\n')
    
    def get_transaction_everything_name(self, product_name):
        transactions = self.data_base['Transaction']
        cursor = transactions.find({'product_name': product_name})
        results = list(cursor)
        if len(results) == 0:
            print("There are no transactions for the product name inputted")
        else:
            bold_start = "\033[1m"
            bold_end = "\033[0m"
            print('\n')
            for document in results:  # Use 'results' instead of 'cursor'
                print(f"Date: {bold_start}{document.get('date', 'N/A')}{bold_end} -- "
                      f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                      f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                      f"Transaction Type: {bold_start}{document.get('transaction_type', 'N/A')}{bold_end} -- "
                      f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                      f"Price: {bold_start}{document.get('price', 'N/A')}{bold_end}")
            print('\n')
    
    def get_transaction_everything_SKU(self, SKU):
        transactions = self.data_base['Transaction']
        cursor = transactions.find({'SKU': SKU})
        results = list(cursor)
        if len(results) == 0:
            print("There are no transactions for the SKU inputted")
        else:
            bold_start = "\033[1m"
            bold_end = "\033[0m"
            print('\n')
            for document in results:  # Use 'results' instead of 'cursor'
                print(f"Date: {bold_start}{document.get('date', 'N/A')}{bold_end} -- "
                      f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                      f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                      f"Transaction Type: {bold_start}{document.get('transaction_type', 'N/A')}{bold_end} -- "
                      f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                      f"Price: {bold_start}{document.get('price', 'N/A')}{bold_end}")
            print('\n')
        
    def get_transaction_everything_type(self, transaction_type):
        transactions = self.data_base['Transaction']
        cursor = transactions.find({'transaction_type': transaction_type})
        results = list(cursor)
        if len(results) == 0:
            print("There are no transactions for the transaction type inputted")
        else:
            bold_start = "\033[1m"
            bold_end = "\033[0m"
            print('\n')
            for document in results:  # Use 'results' instead of 'cursor'
                print(f"Date: {bold_start}{document.get('date', 'N/A')}{bold_end} -- "
                      f"SKU: {bold_start}{document.get('SKU', 'N/A')}{bold_end} -- "
                      f"Product Name: {bold_start}{document.get('product_name', 'N/A')}{bold_end} -- "
                      f"Transaction Type: {bold_start}{document.get('transaction_type', 'N/A')}{bold_end} -- "
                      f"Stock: {bold_start}{document.get('stock', 'N/A')}{bold_end} -- "
                      f"Price: {bold_start}{document.get('price', 'N/A')}{bold_end}")
            print('\n')
            
# FUNCTIONS BELOW NEEDS TO BE EDITTED
            
    def delete_transaction(self, date, SKU, product_name, transaction_type, stock, price, status):
        if self.status == "R":
            print("You dont have access to add any items")
            return None
        else:            
            transactions = self.data_base['Transaction']
            db = Product(status)
            products = db.data_base['Product']
            
            transaction_check = transactions.find_one({'date': date, 'SKU': SKU, 'product_name': product_name, 'transaction_type': transaction_type, 'stock': stock, 'price': price})
            if transaction_check:
                product_check = products.find_one({'SKU': SKU})
                if product_check:
                    new_stock = product_check['stock'] + stock
                    products.update_one({'SKU': SKU}, {'$set': {'stock': new_stock}})
                    transaction = transactions.delete_one({'date': date, 'SKU': SKU, 'product_name': product_name, 'transaction_type': transaction_type, 'stock': stock, 'price': price})
                    print("You have successfully deleted a transaction!")
                else:
                    print("Product doesn't exist. Please try adding it first!")
            else:
                print("Transaction does not exist. Please add the transaction first.")
    
    def add_transaction(self, date, SKU, product_name, transaction_type, stock, price, status):
        if self.status == "R":
            print("You dont have access to add any products")
            return None
        else:
            transactions = self.data_base['Transaction']
            db = Product(status)
            products = db.data_base['Product']
            
            product_check = products.find_one({'SKU': SKU})
            if product_check:
                new_stock = product_check['stock']  - stock
                if new_stock < 0:
                    print("Cant do this transaction as there is not enough in stock")
                    return None
                else:
                    products.update_one({'SKU': SKU}, {'$set': {'stock': new_stock}})
                    transaction = transactions.insert_one({'date': date, 'SKU': SKU, 'product_name': product_name, 'transaction_type': transaction_type, 'stock': int(stock), 'price': int(price)})
                    print("You have successfully added the transaction!")
            else:
                print("Product doesn't exist. Please try adding it first!")

    def update_transaction(self, date, SKU, product_name, transaction_type, stock, price):
        # make sure that stock changes in Product Database
        ...

    def get_transaction_all(self):
        ...
        
    def transaction_to_csv(self):
        # Every user
        with open('transaction.csv', 'w', newline='') as csvfile:
            fieldnames = ['date', 'SKU', 'product_name', 'transaction_type', 'stock', 'price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.data_base['Transaction'].find():
                date = row.get('date')
                SKU = row.get('SKU')
                product_name = row.get('product_name')
                transaction_type = row.get('transaction_type')
                stock = row.get('stock')
                price = row.get('price')

            writer.writerow({'date': date, 'SKU': SKU, 'product_name': product_name, 'transaction_type': transaction_type, 'stock': stock, 'price': price})

        csvfile.close()

        return None

    # this method is for inputting sample data into database or user inputting csv file instead of single transaction
    def csv_to_transaction(self,filename):
        # Only Admin
        if self.status == "R":
            print("You dont have access to this feature")
            return None
        else:
            with open(filename, newline='') as csvfile:
                myreader = csv.reader(csvfile)
            for row in myreader:
                self.add_transaction(row[0],row[1],row[2],row[3],row[4],row[5])
            filename.close()
            print("You have successfully added all the products!")
            return None
