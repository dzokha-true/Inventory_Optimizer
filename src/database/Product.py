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
import json
import HelperFunctions
from LoginSystem import LoginSystem
from plotly.graph_objects import Figure, Scatter, Bar
import pandas as pd
from abc_analysis import abc_analysis, abc_plot
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from abc_classification.abc_classifier import ABCClassifier
from abc_classification.abc_visualiser import pareto_chart
import csv
from datetime import datetime

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

# =====================================
# ADDING, UPDATING AND REMOVING IS LEFT
# =====================================

class Product(LoginSystem):
    
    def __init__(self):
        self.status = "Admin"
        super().__init__()
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.product_DB = self.data_base['ProductInformation']
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def get_product_everything(self):
        cursor = self.product_DB.find({}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'stock': 1, 'cost': 1, 'inventory_value': 1, 'expected_sales': 1, 'SKU_class': 1})
        data = []
        if cursor:
            for document in cursor:
                data.append(document)
            print(json.dumps(data))
        else:
            print("There are no products")
         
    def get_product_name(self, name):
        cursor = self.product_DB.find({'product_name': name}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'stock': 1, 'cost': 1, 'inventory_value': 1, 'expected_sales': 1, 'SKU_class': 1})
        data = []
        if cursor:
            for document in cursor:
                data.append(document)
            print(json.dumps(data))
        else:
            print("There is no such product with the specified name")
      
    def get_product_SKU(self, SKU):
        cursor = self.product_DB.find({'SKU': SKU}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'stock': 1, 'cost': 1, 'inventory_value': 1, 'expected_sales': 1, 'SKU_class': 1})
        if cursor:
            for document in cursor:
                data.append(document)
            print(json.dumps(data))
        else:
            print("There is no such product with the specified SKU")
            
    def get_product_SKU_class(self, SKU_class):                
        cursor = self.product_DB.find({'SKU_class': choice}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'stock': 1, 'cost': 1, 'inventory_value': 1, 'expected_sales': 1, 'SKU_class': 1})
        if cursor:
            for document in cursor:
                data.append(document)
            print(json.dumps(data))
        else:
            print("There is no product with the specified SKU class!")
        
    def pareto_chart(self):
        revenue = 0
        start_date = '2017-11-01'
        end_date = '2023-01-10'
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
        #df = df.sort_values('cum', ascending=False)
        abc_clf = ABCClassifier(df)
        abc_df = abc_clf.classify('SKU', 'cum')
        pareto_df = pd.DataFrame(columns=['SKU_class', 'cum', 'revenue'])
        for index, row in abc_df.iterrows():
            if any(pareto_df.SKU_class == row['class']):
                for index2, row2 in df.iterrows():
                    if row2['SKU'] == row['SKU']:
                        pareto_df.loc[pareto_df.SKU_class == row['class'], 'revenue'] += row2['revenue']
                        pareto_df.loc[pareto_df.SKU_class == row['class'], 'cum'] += row['cum']
            else:
                for index2, row2 in df.iterrows():
                    if row2['SKU'] == row['SKU']:
                        pareto_df.loc[len(pareto_df.index)] = [row['class'], row['cum'], row2['revenue']]
        df = pareto_df.copy()
        data = [
            Bar(
                name = "SKU Class",
                y= df['revenue'],
                x= df['SKU_class'],
                marker= {"color": list(np.repeat('rgb(71, 71, 135)', 5)) + list(np.repeat('rgb(112, 111, 211)', len(df.index)))}
                ),
            Scatter(
                line= {
                    "color": "rgb(192, 57, 43)",
                    "width": 3
                    },
                name= "Percentage of Total Revenue",
                x=  df['SKU_class'],
                y= 100 - df['cum'],
                yaxis= "y2",
                mode='lines+markers'
                ),
            ]
        layout = {
            "title": {
                'text': "Pareto Chart",
                'font': dict(size=30)
                },
            "font": {
                "size": 14,
                "color": "rgb(44, 44, 84)",
                "family": "Times New Roman, monospace"
                },
            "margin": {
                "b": 20,
                "l": 50,
                "r": 50,
                "t": 10,
                },
            "height": 400,
            "plot_bgcolor": "rgb(255, 255, 255)",
            "legend": {
                "x": 0.79,
                "y": 1.2,
                "font": {
                    "size": 12,
                    "color": "rgb(44, 44, 84)",
                    "family": "Courier New, monospace"
                    },
                'orientation': 'h',
                },
            "yaxis": {
                "title": "Total Revenue",
                "titlefont": {
                    "size": 16,
                    "color": "rgb(71, 71, 135)",
                    "family": "Courier New, monospace"
                    },
                },
            "yaxis2": {
                "side": "right",
                "range": [0, 100],
                "title": "Percentage of Total Revenue",
                "titlefont": {
                    "size": 16,
                    "color": "rgb(71, 71, 135)",
                    "family": "Courier New, monospace"
                    },
                "overlaying": "y",
                "ticksuffix": " %",
                },
            }
        fig = Figure(data=data, layout=layout)
        if not os.path.exists("Downloads"):
            os.mkdir("Downloads")
        fig.write_image("fig2.png")
        



    

