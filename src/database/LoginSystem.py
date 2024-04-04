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

class LoginSystem:
    
    # Initialiser for LoginSystem class
    def __init__(self):
        
        # Connects to the BusinessInventoryChecker database
        URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker"
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        # Assign the AccessDetails collection from LoginSystem database to variable called login_DB 
        self.data_base = client['LoginSystem']
        self.login_DB = self.data_base['AccessDetails']
        
        self.start_login()
    
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
    def login(self):
        
        # Ask the user for their username and checks if the username exists
        username = str(input("Please enter the username: "))
        user_check = self.login_DB.find_one({'username': username})
        
        # If user exists
        if user_check:
            
            # The user has 5 attempts to get the correct password for the inputted username
            attempts = 0
            while attempts < 5:
                
                password = input("Please enter the password: ")
                
                # if the password is correct, it returns True (i.e., managed to login)
                if bcrypt.checkpw(password.encode('utf8'), user_check['password']):
                    
                    self.username = username
                    self.status = user_check.get('status')
                    
                    return True
                
                # if the password is not correct then increment the attempt and print the password is not correct, the amount of attempts left and ask user for the password again
                else:
                    attempts += 1
                    print("Your password is incorrect. Please try again. You have " + str((5 - attempts)) + " attempts left.")
                    
            # If the user did not manage to get the password correct after 5 attempts, print that no attempts left and return False (i.e., not managed to login)
            if attempts == 5:
                print("You have exceeded the maximum number of attempts. Please try again later.")
                return False
                
        # If user doesn't exist
        else:
            # print that the user doesnt exist and ask the user if they want to login or register
            print("User does not exist. You need to register for an account.")
            choice = str(input("Would you like to register or login: "))
            
            # keeping asking for either register or login as user inputs
            while choice != "register" and choice != "login":
                choice = str(input("Please input either register or login: "))
            
            # if user inputted register, then call the register function. If user inputted login, then call the login function
            if choice == "register":
                return self.register()
            else:
                return self.login()
    
    def register(self):
        
        # Ask the user for a username and check if it already exists
        username = str(input("Please enter a username for the account: "))
        user_check = self.login_DB.find_one({'username': username})
        
        # Keep asking for a username until the user enters a username which doesn't exist
        while user_check:
            username = str(input("Username already exists! Please enter another username: "))
            user_check = self.login_DB.find_one({'username': username})
        
        # Call password_checker function to get a secure password to assign to the account
        password = HelperFunctions.password_checker()
        
        # Assign the user status
        status = HelperFunctions.status_check(self)
        
        # Find an admin in the database
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        
        self.username = username
        self.status = status
        fiscal_year = admin_user.get('fiscal_year')
        lifo_fifo = admin_user.get('lifo_fifo')
        
        # hash the password and insert it onto the database
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.login_DB.insert_one({'username': username, 'password': hashed_password, 'status': status, 'fiscal_year': fiscal_year, 'lifo_fifo': lifo_fifo})
        
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
        
    
        
        
        
        
        
        
        
        
