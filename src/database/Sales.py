from pymongo import MongoClient
from pymongo.server_api import ServerApi
import HelperFunctions
from Product import Product
import pandas as pd
from abc_classification.abc_classifier import ABCClassifier
from datetime import datetime

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

class Sales(Product):
    
    def __init__(self):
        super().__init__()
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.sales_DB = self.data_base['SalesDone']

    def add_sale(self, date, SKU, product_name, quantity, price):
        self.sales_DB.insert_one({
            "date": date,
            "SKU": SKU,
            "product_name": product_name,
            "quantity": quantity,
            "price": price
        })
        item = self.product_DB.find_one({'SKU': 'SKU'})
        if item.get("quantity") == 0:
            print("Unsuccessful")
        else:
            temp = int(item.get("quantity")) - 1
            self.product_DB.update_one({'SKU': SKU}, {'$set': {"quantity": str(temp)}})
            print("Success")
    
    def total_revenue_calculator(self):
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year', '01-01')  # Assume 'MM-DD' format if not specified
        now = datetime.now()
        current_year = now.year
        date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d')

        if date > now:
            start = datetime(current_year - 1, date.month, date.day)
            end = datetime(current_year, date.month, date.day)
        else:
            start = datetime(current_year, date.month, date.day)
            end = datetime(current_year + 1, date.month, date.day)

        fiscal_year_start_str = start.strftime('%Y-%m-%d')
        fiscal_year_end_str = end.strftime('%Y-%m-%d')

        # Fetch sales within the fiscal year
        cursor = self.sales_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}},
                                    {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})

        revenue = 0  # Initialize revenue
        for document in cursor:
            num = float(document.get('quantity', 0))
            cost = float(document.get('price', 0))
            revenue += num * cost

        if revenue > 0:
            return revenue
        else:
            return 0
    
    """
    def total_revenue_calculator(self):
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
        start_date = fiscal_year_start_str
        end_date = fiscal_year_end_str
        cursor = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 0, 'product_name': 0, 'quantity': 1, 'price': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue += num * cost
                print(revenue)
                return True
        else:
            return False
    """
        
    def SKU_class(self):
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
        start_date = fiscal_year_start_str
        end_date = fiscal_year_end_str
        revenue = 0
        cursor = self.sales_DB.find({}, {'_id': 1, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue += num * cost
        df = pd.DataFrame(columns=['SKU', 'product_name', 'revenue', 'cum'])
        cursor = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
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
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue = num * cost
                        df.at[row_index[0], 'revenue'] += revenue
                        cum = df.at[row_index[0], 'revenue'] / total * 100
                        df.at[row_index[0], 'cum'] = cum
        df = df.sort_values('cum', ascending=False)
        abc_clf = ABCClassifier(df)
        abc_df = abc_clf.classify('SKU', 'cum')
        for index, row in abc_df.iterrows():
            self.product_DB.update_one({'SKU': row['SKU']}, {'$set': {'SKU_class': row['class']}})
