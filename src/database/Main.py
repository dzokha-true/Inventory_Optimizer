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
from Mathematics import Mathematics
import json
import HelperFunctions 

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

if __name__ == "__main__":
    db = Mathematics()
            
    if len(sys.argv) == 2:
        if sys.argv[-1] == "get product":
            db.get_product_everything()
        
        if sys.argv[-1] == "get_report":
            cogs = db.COGS()
            gross = db.gross_margin()
            ITR = db.inventory_turnover_ratio()
            data = {"gross": gross,"cogs": cogs, "ITR": ITR}
            print(json.dump(data))

        if sys.argv[-1] == "generate_dashboard":
            # SHOW all orders database 
            db.pareto_chart()

        if sys.argv[-1] == "kpi_dash":
            cogs = db.COGS()
            gross = db.gross_margin()
            ITR = db.inventory_turnover_ratio()
            data = {"gross": gross,"cogs": cogs, "ITR": ITR}
            print(json.dump(data))
            
    elif len(sys.argv) == 3:
        if sys.argv[-1] == "get product by name":
            _, name, operation = sys.argv
            db.get_product_name(name)
        
        elif sys.argv[-1] == "get product by SKU":
            _, SKU, operation = sys.argv
            if HelperFunctions.SKU_Checker(SKU):
                db.get_product_SKU(SKU)
                
        elif sys.argv[-1] == "get product by SKU class":
            _, SKU_class, operation = sys.argv
            if SKU_class == 'A' or SKU_class == 'B' or SKU_class == 'C':
                db.get_product_SKU_class(SKU_class)
            else:
                print("Please enter a valid SKU class (e.i., 'A', 'B' or 'C'")
                
        elif sys.argv[-1] == "get total revenue":
            _, start_date, end_date = sys.argv
            revenue = db.total_revenue_calculator(start_date, end_date)
                
    elif len(sys.argv) == 4:
        if sys.argv[-1] == "login":
            _, username, password, operation = sys.argv
            db.login(username, password)
            
        elif sys.argv[-1] == "change fiscal year":
            _, date, username, operation = sys.argv
            status = HelperFunctions.status_check(db, username)
            new_date = db.check_fiscal_year(date)
            if new_date != False:
                db.change_fiscal_year(new_date, status)
                
        elif sys.argv[-1] == "change lifo_fifo":
            _, lifo_fifo, username, operation = sys.argv
            status = HelperFunctions.status_check(db, username)
            if lifo_fifo == 'lifo' or lifo_fifo == 'fifo':
                db.change_fiscal_year(lifo_fifo, status)
        
        elif sys.argv[-1] == "get SKU revenue":
            _, SKU, start_date, end_date = sys.argv
            revenue = db.SKU_revenue_calculator(SKU, start_date, end_date)
             
        elif sys.argv[-1] == "get name revenue":
            _, product_name, start_date, end_date = sys.argv
            revenue = db.name_revenue_calculator(product_name, start_date, end_date)
            
    elif len(sys.argv) == 5:
        if sys.argv[-1] == "register":
            _, username, password, status, operation = sys.argv
            db.register(username, password, status)
            
    else:
        print("Usage: LoginSystem.py <username> <password>")
        sys.exit(1)
        
        
s
        
        
        
        
        
        
        
        
        


