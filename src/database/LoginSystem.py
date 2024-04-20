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
import HelperFunctions

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

# TALK TO PREE ABOUT THE USER ACCESS LEVEL
# TALK TO PREE ABOUT THE RETURNS AND PRINTS




class LoginSystem:
    
    # Initialiser for LoginSystem class
    def __init__(self):
        
        # Connects to the BusinessInventoryChecker database
        URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        # Assign the AccessDetails collection from LoginSystem database to variable called login_DB 
        self.data_base = client['LoginSystem']
        self.login_DB = self.data_base['AccessDetails']
      
      
      
      
      
    # First stage of login asking the user for either creating an account or logging in
    def start_login(self):
        
        # Ask the user if they have an account
        choice = input("Do you have an account (yes or no): ")
        
        # Keep asking the same question until the user inputs yes or no
        while choice != "yes" and choice != "no":
            choice = input("Please enter either yes or no: ")
            
        # if user has account, then the functions called the login function, else it calls the register function
        if choice == "yes":
            return self.login()
        else:
            return self.register()
    
    
    
    
    
    # logging in the user
    def login(self, username, password):
        user_check = self.login_DB.find_one({'username': username})
        if user_check:    
            if bcrypt.checkpw(password.encode('utf8'), user_check['password']):
                self.username = username
                self.status = user_check.get('status')
                self.fiscal_year = user_check.get('fiscal_year')
                self.lifo_fifo = user_check.get('lifo_fifo')
                print("Success")
                return True
            else:
                print("Wrong Password")
                return False
        else:
            print("Wrong Password")
            return False
            
            
            
    
    def register(self, username, password, status):
        user_check = self.login_DB.find_one({'username': username})
        if user_check:
            print("User exists")
            return False
        capital = False
        special = False
        number = False
        if capital == False or special == False or number == False or len(password) < 8:
            if len(password) < 8:
                print("Length is wrong")
                return False
            for letter in password:
                if letter in str(numbers):
                        number = True
                if letter not in str(numbers) and letter not in letters and letter not in capitals:
                    special = True
                if letter in capitals:
                    capital = True
            if number == False:
                print("No numbers")
                return False
            if special == False:
                print("No special characters")
                return False
            if capital == False:
                print("No capitals")
                return False                  
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        if status == "ReadWrite":
            self.status = "RW"
        elif status == "Admin":
            self.status = "Admin"
        elif status == "Read":
            self.status ="R"
        else:
            print(status+"Wrong status")
            return False
        self.username = username
        self.status = status
        self.fiscal_year = admin_user.get('fiscal_year')
        self.lifo_fifo = admin_user.get('lifo_fifo')
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.login_DB.insert_one({'username': username, 'password': hashed_password, 'status': status, 'fiscal_year': self.fiscal_year, 'lifo_fifo': self.lifo_fifo})
        print("Success")
        return True
    
    
    
    
    
    # change the fiscal year for everyone, only admins can do it
    def change_fiscal_year(self):
        
        # Checks if the user is admin and if not, prints the correct message
        if self.status != "Admin":
            print("You can not change the fiscal year")
            return False
        
        # gets a new fiscal year date and changes the database for all the users accordingly
        new_fiscal_year = HelperFunctions.check_fiscal_year()
        result = self.login_DB.update_many({}, {"$set": {"fiscal_year": new_fiscal_year}})
        return True
    
    # change the lifo fifo computation for everyone, only admin can do it
    def change_lifo_fifo(self):
        
        # Checks if the user is admin and if not, prints the correct message
        if self.status != "Admin":
            print("You can not change the life or fifo computation")
            return False
        
        # gets a new fifo or lifo computation and changes the database for all the users accordingly
        new_lifo_fifo = HelperFunctions.check_lifo_fifo()
        result = self.login_DB.update_many({}, {"$set": {"lifo_fifo": new_lifo_fifo}})
        return True

        
        
        
        
        
        