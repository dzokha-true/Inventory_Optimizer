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
from Received_Order import Received_Order
from LoginSystem import LoginSystem
import json

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

class Mathematics(Received_Order):
    
    def __init__(self):
        super().__init__()
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.performance_DB = self.data_base['Performance']









    def gross_profit(self):
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year')
        now = datetime.now()
        current_year = now.year
        date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d') 
        if date > now:
            start = datetime(current_year-1, date.month, date.day)
            end = datetime(current_year, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')
        else:
            start = datetime(current_year, date.month, date.day)
            end = datetime(current_year+1, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')

        start_date = fiscal_year_start_str
        end_date = fiscal_year_end_str
        cursor = sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 0, 'product_name': 0, 'num': 1, 'cost': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('num', 0))
                        cost = float(document.get('cost', 0))
                        revenue += num * cost

        
        COGS = self.COGS(product)
        return revenue - COGS
       
       
       
       
       
       
       
       
    #calculate gross margin
    def gross_margin(self):
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year')
        now = datetime.now()
        current_year = now.year
        date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d') 
        if date > now:
            start = datetime(current_year-1, date.month, date.day)
            end = datetime(current_year, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')
        else:
            start = datetime(current_year, date.month, date.day)
            end = datetime(current_year+1, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')

        return self.gross_profit() / self.revenue_calculator() * 100

    #calculate average inventory
    def average_inventory(self):
        # range of dates
        # Tie to a date, per SKU
        start = self.received_order_DB.cost.find().sort({"cost": -1}).limit(1) 
        end = self.received_order_DB.cost.find().sort({"cost": 1}).limit(1) 
        return (start + end)/2
        
    # Turnover Ratio
    def inventory_turnover_ratio(self):
        # range of dates
        # Tie to a date, per SKU
        return self.COGS(product)/self.average_inventory() 
        
    #COGS
    def COGS(self, product):
        # range of dates
        # Tie to a date, per SKU
        number_stock = self.received_order_DB.find({},{"product":product}).count()
        COGS = 0
        all_product = self.sales_DB.find({},{"product":product}).pretty()
        number_sales = self.sales_DB.count()
        if self.login_DB.find({"lifo_fifo":"fifo"}):
            for i in [0,number_sales-1]:
                COGS += all_product[i].price
        elif self.login_DB.find({"lifo_fifo":"lifo"}):
            for i in [number_stock,number_stock-number_sales+1]:
                COGS += all_product[i].price
                



