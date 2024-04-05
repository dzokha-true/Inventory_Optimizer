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
from datetime import datetime
import re

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

# checking if the password is correct
def password_checker():
        
    # Assigning variables to check for capital letters, special characters and numbers
    capital = False
    special = False
    number = False
    password = ''
    
    # keep asking the user until the password has 8 characters, 1 upper case letter, 1 number and 1 special character
    while capital == False or special == False or number == False or len(password) < 8:
        password = str(input("Please enter the password: "))
        number = False
        capital = False
        special = False
        
        # prints according message if the password has less than 8 characters
        if len(password) < 8:
            print("Password has to be atleast 8 characters long!")
            
        # checks if the password has a number, a capital letter and a special character
        for letter in password:
            if letter in str(numbers):
                    number = True
            if letter not in str(numbers) and letter not in letters and letter not in capitals:
                special = True
            if letter in capitals:
                capital = True
        
        if number == False:
            print("Your paswword has to contain a number!")
        if special == False:
            print("Your password has to contain a special character!")
        if capital == False:
            print("Your password has to contain a capital letter")
                
    return password

# Check the user access level
def status_check(object):
    
    # Asks the user for their access level code given by the company
    status = input("Write code according to your priveledges (should be given by the company): ")
    
    # returns a string depending on their access level. If the user didnt enter it correct, the user is sent back to the intial login
    if status == "ReadWrite":
        return "ReadWrite"
    elif status == "Admin":
        return "Admin"
    elif status == "Read":
        return "Read"
    else:
        print("You don't have any priveledges!")
        return False
        
# Check if the date has been entered in correct format
def normal_date_checker():
    
    # assign a pattern to check the user input
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    
    # ask the user for the date unitl the format is correct
    loop = True
    while loop:
        date_input = input("Please enter the date in the format (YYYY-MM-DD): ")
        
        # checks if the user input is in correct format
        check = re.match(pattern, date_input)
        if not check:
            print("Please enter the correct format!")
        else:
            
            # checks if the input is an actual date
            loop = False
            try:
                my_date = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
            except ValueError as ve:
                print("Please make sure that the Month is between 1-12 and Day is between 1-31 depending on the Month")
                loop = True
    return my_date
    
# checks if the price is correct
def price_Checker():
    
    # asks the user for the cost until a value is correct
    case = True
    while case:
        try:
            price = float(input("Enter the cost: "))
            
            # checks if the price is graeter than zero and if not, gives an appropriate message
            if price > 0:
                case = False
            else:
                print("Enter a number greater than zero!")
        
        # catches an exception where the user enters a letter instead of a number
        except ValueError as ve:
            print("Please enter a number!")     
    return price

# checks if the SKU is correct
def SKU_Checker():
    
    # asks the user for SKU until the user enters it in a correct format
    case = True
    while case:
        SKU = input("Enter the SKU in the format AAA-111-A-1: ")
        
        # checks if the SKU is in correct format and if not, it prints an appropriate message
        if re.match('^[A-Z]{3}-[0-9]{3}-[A-Z]{1}-[0-9]{1}$', SKU):
            case = False
        else:
            print("Please enter the SKU in the correct format")
    return SKU

# checks if the stock number is correct
def stock_Checker():
    
    # asks the user for the number until the user enters it in a correct format
    case = True
    while case:
        try:
            stock = int(input("Enter the stock number: "))
            
            # checks if the number is equal or above zero
            if stock >= 0:
                case = False
            else:
                print("Enter a number greater than one!")
        
        # catches the exception if the user enters a letter and prints an appropriate message
        except ValueError as ve:
            print("Please enter a number!")
            case = True      
    return stock

# Check if the fiscal year format is correct
def check_fiscal_year():
    
    # sets the format for the fiscal date and the loop case
    date_format = "%m-%d"
    valid_date = False
    
    # Asks the user for input until a valid date is inputted
    while not valid_date:
        user_input = input("Please enter the fiscal date in MM-DD format: ")
        
        # Tries to make it into daytime object and if it cant, it will ask for user input again
        try:
            valid_date = datetime.strptime(user_input, date_format)
        except ValueError:
            print("Invalid format. Please ensure the date is in MM-DD format.")
    return user_input

# Checks if the user wants lifo or fifo
def check_lifo_fifo():
    choice = input("Would you like COGS to calculate using lifo or fifo: ")
    while choice != "lifo" and choice != "fifo":
        choice = input("Please input either lifo or fifo: ")
    return choice

def check_order_number():
    
    # asks the user for the number until the user enters it in a correct format
    case = True
    while case:
        try:
            choice = int(input("Enter the order number: "))
            
            # checks if the number is equal or above zero
            if choice >= 0:
                case = False
            else:
                print("Order value has to greater than zero!")
        
        # catches the exception if the user enters a letter and prints an appropriate message
        except ValueError as ve:
            print("Please enter a number!")
            case = True      
    return choice
