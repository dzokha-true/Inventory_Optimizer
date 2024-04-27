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
import re

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

def check_fiscal_year(date):
    date_format = "%m-%d"
    try:
        temp = datetime.strptime(date, date_format)
        return temp
    except ValueError:
        print("Invalid format. Please ensure the date is in MM-DD format!")
        return False

def status_check(object, username):
    user = object.login_DB.find_one({'username': username})
    status = user.get('status')
    if status == "ReadWrite":
        return "ReadWrite"
    elif status == "Admin":
        return "Admin"
    else:
        return "Read"

def SKU_Checker(SKU):
    if re.match('^[A-Z]{3}-[0-9]{3}-[A-Z]{1}-[0-9]{1}$', SKU):
        print("Invalid format. Please ensure the SKU is in AAA-111-A-1 format!")
        return False
    else:
        return True
    
def normal_date_checker(date_input):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_input):
        print("Invalid format. Please ensure the date is in YYYY-MM-DD format.")
        return False
    else:
        try:
            year, month, day = map(int, date_input.split('-'))
            my_date = date(year, month, day)
            return date_input  
        except ValueError:
            print("Invalid date. Please make sure the date is correct format (YYYY-MM-DD).")
            return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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


