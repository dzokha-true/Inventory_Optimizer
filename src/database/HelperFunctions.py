# Imports for the code
from datetime import datetime
from datetime import date
import re
import statistics
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd


# Function to check the fiscal year and returns the fiscal year if it is in the correct format
def check_fiscal_year(date_input):
    date_format = "%Y-%m-%d"
    try:
        temp = datetime.strptime(date_input, date_format)
        return temp
    except ValueError:
        print("Invalid format. Please ensure the date is in YYYY-MM-DD format!")
        return False


# Function to check the status of the user and return the status of the user
def status_check(object_status, username):
    user = object_status.login_DB.find_one({'username': username})
    status = user.get('status')
    if status == "ReadWrite":
        return "ReadWrite"
    elif status == "Admin":
        return "Admin"
    else:
        return "Read"


# Function to validate the date format which returns the date if it is in the correct format
def normal_date_checker(date_input):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_input):
        print("Invalid format. Please ensure the date is in YYYY-MM-DD format.")
        return False
    else:
        try:
            year, month, day = map(int, date_input.split('-'))
            date(year, month, day)
            return date_input
        except ValueError:
            print("Invalid date. Please make sure the date is correct format (YYYY-MM-DD).")
            return False


# Function to check the current stock for a given SKU
def stock(sku):
    # Establish connection to the product database within MongoDB
    uri = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName"
           "=BusinessInventoryChecker&tlsInsecure=true")
    client = MongoClient(uri, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    product_db = data_base['ProductInformation']
    cursor = product_db.find({'SKU': sku}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    for document in cursor:
        return int(float(document.get("quantity")))


# Function to calculate and return mean daily sales for a given SKU
def mean_daily(sku):
    return find_total_quantity(sku) / 730


# Function to calculate and return mean weekly sales for a given SKU
def mean_weekly(sku):
    return find_total_quantity(sku) / 104


# Function to calculate and return standard deviation of weekly sales for a given SKU
def sd_weekly(sku):
    df = create_pd_information(sku)
    df['date'] = pd.to_datetime(df['date'])
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    weekly_sums = df.resample('W-SUN', on='date')['quantity'].sum()
    return statistics.stdev(weekly_sums)


# Function to create and return a pandas DataFrame from the sales database within MongoDB for a given SKU
def create_pd_information(sku):
    start_date = get_start_date()
    end_date = get_end_date()
    sales_db = get_sales_database()
    cursor = sales_db.find({'SKU': sku, 'date': {'$gte': start_date, '$lte': end_date}},
                           {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    df = pd.DataFrame(list(cursor))
    return df


# Function to calculate and return total demand for a given SKU
def total_demand(sku):
    return find_total_quantity(sku)


# Function to find and return total quantity on order for a given SKU
def sku_on_order(sku):
    # Establish connection to the orders database within MongoDB
    uri = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName"
           "=BusinessInventoryChecker&tlsInsecure=true")
    client = MongoClient(uri, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    orders_db = data_base['OrdersPlaced']
    total = 0
    cursor = orders_db.find({'SKU': sku}, {'_id': 0, 'date': 1, 'SKU': 1,
                                           'product_name': 1, 'quantity': 1, 'price': 1, 'isReceived': 1})
    for document in cursor:
        if not document.get("isReceived"):
            total += int(document.get("quantity"))
    return total


# Function to calculate and return total quantity sold for a given SKU
def find_total_quantity(sku):
    start_date = get_start_date()
    end_date = get_end_date()
    sales_db = get_sales_database()
    total = 0
    cursor = sales_db.find({'SKU': sku}, {'_id': 0, 'date': 1, 'SKU': 1,
                                          'product_name': 1, 'quantity': 1, 'price': 1})
    for document in cursor:
        if (datetime.strptime(start_date, "%Y-%m-%d") <=
                datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <=
                datetime.strptime(end_date, "%Y-%m-%d")):
            total += int(float(document.get("quantity")))
    return total


# Function to connect and return the sales database within MongoDB
def get_sales_database():
    # Establish connection to sales database within MongoDB
    uri = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName"
           "=BusinessInventoryChecker&tlsInsecure=true")
    client = MongoClient(uri, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    sales_db = data_base['SalesDone']
    return sales_db


# Function to get the end date of the fiscal year for calculation
def get_end_date():
    now = datetime.now()
    end = datetime(now.year, now.month, now.day)
    end_date = end.strftime('%Y-%m-%d')
    return end_date


# Function to get the start date of the fiscal year for sales analysis
def get_start_date():
    now = datetime.now()
    start = datetime(now.year - 1, now.month, now.day)
    start_date = start.strftime('%Y-%m-%d')
    return start_date
