# Import the needed modules
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from LoginSystem import LoginSystem
from plotly.graph_objects import Figure, Scatter, Bar
import pandas as pd
import numpy as np
from abc_classification.abc_classifier import ABCClassifier
from datetime import datetime


# Class for product which inherits from LoginSystem
class Product(LoginSystem):

    # Constructor for Product class which calls parent class constructor and assigns product database to variable
    def __init__(self):
        self.status = "Admin"
        super().__init__()
        URI = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority"
               "&appName=BusinessInventoryChecker&tlsInsecure=true")
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.product_DB = self.data_base['ProductInformation']

    # Function which returns the admin user, start of the fiscal year and end of the fiscal year in string format
    def get_fiscal_year_admin(self):
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year')
        now = datetime.now()
        current_year = now.year
        date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d')
        if date > now:
            start = datetime(current_year - 1, date.month, date.day)
            end = datetime(current_year, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')
        else:
            start = datetime(current_year, date.month, date.day)
            end = datetime(current_year + 1, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')
        return fiscal_year_start_str, fiscal_year_end_str, admin_user

    # Function which creates a pareto chart and downloads it so that html can display it for the user
    def pareto_chart(self):
        start_date, end_date, admin_user = self.get_fiscal_year_admin()
        revenue = 0
        cursor = self.sales_DB.find({}, {'_id': 1, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
        if start_date is not False and end_date is not False:
            if cursor:
                for document in cursor:
                    if (datetime.strptime(start_date, "%Y-%m-%d") <=
                            datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <=
                            datetime.strptime(end_date, "%Y-%m-%d")):
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue += num * cost
        df = pd.DataFrame(columns=['SKU', 'product_name', 'revenue', 'cum'])
        cursor = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
        total = revenue
        if cursor:
            for document in cursor:
                if (datetime.strptime(start_date, "%Y-%m-%d") <=
                        datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <=
                        datetime.strptime(end_date, "%Y-%m-%d")):
                    if document.get('SKU', 'N/A') not in df['SKU'].values:
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue = num * cost
                        cum = revenue / total * 100
                        new_row = {'SKU': document.get('SKU', 'N/A'),
                                   'product_name': document.get('product_name', 'N/A'), 'revenue': revenue, 'cum': cum}
                        df.loc[len(df)] = new_row
                    else:
                        row_index = df[df['SKU'] == document.get('SKU', 'N/A')].index
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue = num * cost
                        df.at[row_index[0], 'revenue'] += revenue
                        cum = df.at[row_index[0], 'revenue'] / total * 100
                        df.at[row_index[0], 'cum'] = cum
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
        data = [Bar(name="SKU Class", y=df['revenue'], x=df['SKU_class'],
                    marker={"color": list(np.repeat('rgb(71, 71, 135)', 5)) +
                            list(np.repeat('rgb(112, 111, 211)', len(df.index)))}),
                Scatter(line={"color": "rgb(192, 57, 43)", "width": 3}, name="Percentage of Total Revenue",
                        x=df['SKU_class'], y=100 - df['cum'], yaxis="y2", mode='lines+markers'), ]
        layout = {"title": {'text': "Pareto Chart", 'font': dict(size=30)},
                  "font": {"size": 14, "color": "rgb(44, 44, 84)", "family": "Times New Roman, monospace"},
                  "margin": {"b": 20, "l": 50, "r": 50, "t": 10, }, "height": 400, "plot_bgcolor": "rgb(255, 255, 255)",
                  "legend": {"x": 0.79, "y": 1.2, "font": {"size": 12, "color": "rgb(44, 44, 84)",
                                                           "family": "Courier New, monospace"}, 'orientation': 'h', },
                  "yaxis": {"title": "Total Revenue", "titlefont": {"size": 16, "color": "rgb(71, 71, 135)",
                                                                    "family": "Courier New, monospace"}, },
                  "yaxis2": {"side": "right", "range": [0, 100], "title": "Percentage of Total Revenue",
                             "titlefont": {"size": 16, "color": "rgb(71, 71, 135)", "family": "Courier New, monospace"},
                             "overlaying": "y", "ticksuffix": " %", }, }
        fig = Figure(data=data, layout=layout)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(current_dir, '..', 'source', 'public', 'images')
        fig.write_image(os.path.join(images_dir, 'pareto_chart.png'))
