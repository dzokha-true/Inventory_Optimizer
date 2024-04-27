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
from Product import Product
import pandas as pd
from abc_analysis import abc_analysis, abc_plot
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from abc_classification.abc_classifier import ABCClassifier
from abc_classification.abc_visualiser import pareto_chart
import csv
import bcrypt
import json
from datetime import datetime

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

# ==================================
# NEEDS ADDING REMOVING AND UPDATING
# ==================================

class Sales(Product):
    
    def __init__(self):
        super().__init__()
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.sales_DB = self.data_base['SalesDone']
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def total_revenue_calculator(self, start_date, end_date):
        start_date = normal_date_checker(start_date)
        end_date = normal_date_checker(end_date)
        cursor = sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 0, 'product_name': 0, 'num': 1, 'cost': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('num', 0))
                        cost = float(document.get('cost', 0))
                        revenue += num * cost
                print(revenue)
        else:
            return False
                    
    def SKU_revenue_calculator(self, SKU, start_date, end_date):
        start_date = normal_date_checker(start_date)
        end_date = normal_date_checker(end_date)
        cursor = sales_DB.find({'SKU': SKU}, {'_id': 0, 'date': 1, 'SKU': 0, 'product_name': 0, 'num': 1, 'cost': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('num', 0))
                        cost = float(document.get('cost', 0))
                        revenue += num * cost
                print(revenue)
        else:
            return False
        
    def name_revenue_calculator(self, product_name, start_date, end_date):
        start_date = normal_date_checker(start_date)
        end_date = normal_date_checker(end_date)
        cursor = sales_DB.find({'product_name': product_name}, {'_id': 0, 'date': 1, 'SKU': 0, 'product_name': 0, 'num': 1, 'cost': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('num', 0))
                        cost = float(document.get('cost', 0))
                        revenue += num * cost
                print(revenue)
        else:
            return False    
        
    def SKU_class(self):
        start_date = '2019-11-01'
        end_date = '2023-01-10'
        revenue = 0
        cursor = self.sales_DB.find({}, {'_id': 1, 'date': 1, 'SKU': 1, 'product_name': 1, 'num': 1, 'cost': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('num', 0))
                        cost = float(document.get('cost', 0))
                        revenue += num * cost
        df = pd.DataFrame(columns=['SKU', 'product_name', 'revenue', 'cum'])
        cursor = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'num': 1, 'cost': 1})
        total = revenue
        if cursor:
            for document in cursor:
                if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                    if document.get('SKU', 'N/A') not in df['SKU'].values:
                        num = float(document.get('num', 0))
                        cost = float(document.get('cost', 0))
                        revenue = num * cost
                        cum = revenue / total * 100
                        new_row = {'SKU': document.get('SKU', 'N/A'), 'product_name': document.get('product_name', 'N/A'), 'revenue': revenue, 'cum': cum}
                        df.loc[len(df)] = new_row
                    else:
                        row_index = df[df['SKU'] == document.get('SKU', 'N/A')].index
                        num = float(document.get('num', 0))
                        cost = float(document.get('cost', 0))
                        revenue = num * cost
                        df.at[row_index[0], 'revenue'] += revenue
                        cum = df.at[row_index[0], 'revenue'] / total * 100
                        df.at[row_index[0], 'cum'] = cum
        df = df.sort_values('cum', ascending=False)
        abc_clf = ABCClassifier(df)
        abc_df = abc_clf.classify('SKU', 'cum')
        for index, row in abc_df.iterrows():
            self.product_DB.update_one({'SKU': row['SKU']}, {'$set': {'SKU_class': row['class']}})
        


        


        
        
        
        
        

