from datetime import datetime
from datetime import date
import re
import statistics
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

def check_fiscal_year(date):
    date_format = "%Y-%m-%d"
    try:
        temp = datetime.strptime(date, date_format)
        return temp
    except ValueError:
        print("Invalid format. Please ensure the date is in YYYY-MM-DD format!")
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

def stock(SKU):
    URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    product_DB = data_base['ProductInformation']
    cursor = product_DB.find({'SKU': SKU}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    for document in cursor:
        return int(float(document.get("quantity")))

def mean_daily(SKU):
    now = datetime.now()
    end = datetime(now.year, now.month, now.day)
    start = datetime(now.year - 1, now.month, now.day)
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    sales_DB = data_base['SalesDone']
    total = 0
    cursor = sales_DB.find({'SKU': SKU},{'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    for document in cursor:
        if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'),"%Y-%m-%d") <= datetime.strptime(end_date,"%Y-%m-%d"):
            total += int(float(document.get("quantity")))
    return total / 730

def mean_weekly(SKU):
    now = datetime.now()
    end = datetime(now.year, now.month, now.day)
    start = datetime(now.year - 1, now.month, now.day)
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    sales_DB = data_base['SalesDone']
    total = 0
    cursor = sales_DB.find({'SKU': SKU},{'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    for document in cursor:
        if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'),"%Y-%m-%d") <= datetime.strptime(end_date,"%Y-%m-%d"):
            total += int(float(document.get("quantity")))
    return total / 104

def sd_daily(SKU):
    now = datetime.now()
    end = datetime(now.year, now.month, now.day)
    start = datetime(now.year - 1, now.month, now.day)
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    sales_DB = data_base['SalesDone']
    data = []
    cursor = sales_DB.find({'SKU': SKU, 'date': {'$gte': start_date, '$lte': end_date}},{'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    df = pd.DataFrame(list(cursor))
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    daily_sums = df.groupby('date')['quantity'].sum()
    return statistics.stdev(daily_sums)

def sd_weekly(SKU):
    now = datetime.now()
    end = datetime(now.year, now.month, now.day)
    start = datetime(now.year -1, now.month, now.day)
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    sales_DB = data_base['SalesDone']
    data = []
    cursor = sales_DB.find({'SKU': SKU,'date': {'$gte': start_date, '$lte': end_date}}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    df = pd.DataFrame(list(cursor))
    df['date'] = pd.to_datetime(df['date'])
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    weekly_sums = df.resample('W-SUN', on='date')['quantity'].sum()
    return statistics.stdev(weekly_sums)

def total_demand(SKU):
    now = datetime.now()
    end = datetime(now.year, now.month, now.day)
    start = datetime(now.year -1, now.month, now.day)
    start_date = start.strftime('%Y-%m-%d')
    end_date = end.strftime('%Y-%m-%d')
    URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    sales_DB = data_base['SalesDone']
    total = 0
    cursor = sales_DB.find({'SKU': SKU}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
    for document in cursor:
        if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date,"%Y-%m-%d"):
            total += int(float(document.get("quantity")))
    return total

def sku_on_order(SKU):
    URI = "mongodb+srv://" + "Admin" + ":" + "Admin" + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
    client = MongoClient(URI, server_api=ServerApi('1'))
    data_base = client['CompanyDetails']
    orders_DB = data_base['OrdersPlaced']
    total = 0
    cursor = orders_DB.find({'SKU': SKU}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1, 'isReceived': 1})
    for document in cursor:
        if document.get("isReceived") == False:
            total += int(document.get("quantity"))
    return total