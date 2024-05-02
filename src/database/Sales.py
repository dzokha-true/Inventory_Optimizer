# Import modules
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Product import Product
from datetime import datetime


# Class for Sales which inherits from Product class
class Sales(Product):

    # Constructor for Sales which calls the parent constructor, and it also assigns Sales Database to a variable
    def __init__(self):
        super().__init__()
        URI = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?"
               "retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true")
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.sales_DB = self.data_base['SalesDone']

    # Function for adding a successful sale by a company to the database
    def add_sale(self, date, sku, product_name, quantity, price):
        self.sales_DB.insert_one({"date": date, "SKU": sku, "product_name": product_name,
                                  "quantity": quantity, "price": price})
        item = self.product_DB.find_one({'SKU': sku})
        if int(float(item.get("quantity"))) == 0:
            print("Unsuccessful")
        else:
            temp = int(float(int(item.get("quantity")))) - int(float(quantity))
            self.product_DB.update_one({'SKU': sku}, {'$set': {"quantity": str(temp)}})
            print("Success")

    # Function which calculates and returns the total revenue of the company within the fiscal year period
    def total_revenue_calculator(self):
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year', '01-01')
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
        cursor = self.sales_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}},
                                    {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})
        revenue = 0
        for document in cursor:
            num = float(document.get('quantity', 0))
            cost = float(document.get('price', 0))
            revenue += num * cost
        return revenue
