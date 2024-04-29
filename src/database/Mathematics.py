from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from Received_Order import Received_Order

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
        revenue = 0
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
        cursor = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'), "%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue += num * cost
        if admin_user.get("lifo_fifo") == "fifo":
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}})
        else:
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_end_str, '$lte': fiscal_year_start_str}})
        cursor2 = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})
        cogs = 0
        for document in cursor2:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                num = document.get("quantity", 0)
                for entry in cursor:
                    if entry.get("SKU", 0) == document.get("SKU", 0):
                        cogs += entry.get("price", 0)
        return revenue - cogs

    def gross_margin(self):
        revenue = 0
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
        cursor = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})
        if start_date != False and end_date != False:
            if cursor:
                for document in cursor:
                    if datetime.strptime(start_date, "%Y-%m-%d") <= datetime.strptime(document.get('date', 'N/A'),"%Y-%m-%d") <= datetime.strptime(end_date, "%Y-%m-%d"):
                        num = float(document.get('quantity', 0))
                        cost = float(document.get('price', 0))
                        revenue += num * cost
        if admin_user.get("lifo_fifo") == "fifo":
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}})
        else:
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_end_str, '$lte': fiscal_year_start_str}})
        cursor2 = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})
        cogs = 0
        for document in cursor2:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                num = document.get("quantity", 0)
                for entry in cursor:
                    if entry.get("SKU", 0) == document.get("SKU", 0):
                        cogs += entry.get("price", 0)
        gross_profit = revenue - cogs
        return gross_profit / revenue * 100

    def average_inventory(self):
        revenue = 0
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year')
        now = datetime.now()
        current_year = now.year
        date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d')
        current_date = datetime.strptime(f'{current_year}-{now.month}-{now.day}', '%Y-%m-%d')
        if date > now:
            start = datetime(current_year - 1, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
        else:
            start = datetime(current_year, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
        cursor = self.product_DB.find({'date': fiscal_year_start_str})
        cursor2 = self.product_DB.find({'date': current_date})
        initial = 0
        final = 0
        for document in cursor:
            initial += document.get("quantity", 0) * document.get("price", 0)
        for document in cursor2:
            final += document.get("quantity", 0) * document.get("price", 0)
        return (initial + final)/2

    """    
    def inventory_turnover_ratio(self):
        revenue = 0
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
        if admin_user.get("lifo_fifo") == "fifo":
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}})
        else:
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_end_str, '$lte': fiscal_year_start_str}})
        cursor2 = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})
        cogs = 0
        for document in cursor2:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                num = document.get("quantity", 0)
                for entry in cursor:
                    if entry.get("SKU", 0) == document.get("SKU", 0):
                        cogs += entry.get("price", 0)
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year')
        now = datetime.now()
        current_year = now.year
        date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d')
        current_date = datetime.strptime(f'{current_year}-{now.month}-{now.day}', '%Y-%m-%d')
        if len(now.month) == 1:
            if len(now.day) == 1:
                fin = current_year + "-0" + now.month + "-0" + now.day 
            else:
                fin = current_year + "-0" + now.month + "-" + now.day 
        else:
            fin = current_year + "-" + now.month + "-" + now.day 
        if date > now:
            start = datetime(current_year - 1, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
        else:
            start = datetime(current_year, date.month, date.day)
            if len(date.month) == 1:
                if len(date.day) == 1:
                    fiscal_year_start_str = current_year + "-0" + date.month + "-0" + date.day 
                else:
                    fiscal_year_start_str = current_year + "-0" + date.month + "-" + date.day 
            else:
                fiscal_year_start_str = current_year + "-" + date.month + "-" + date.day 
        cursor = self.sales_DB.find({'date': fiscal_year_start_str})
        cursor2 = self.sales_DB.find({'date': fin})
        initial = 0
        final = 0
        for document in cursor:
            initial += document.get("quantity", 0) * document.get("price", 0)
        for document in cursor2:
            final += document.get("quantity", 0) * document.get("price", 0)
        average = (initial + final)/2
        return cogs/average
    """
    def inventory_turnover_ratio(self):
        # Retrieve the admin user data
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        fiscal_year_start_date = admin_user.get('fiscal_year', '01-01')  # Defaulting to January 1 if not set
        current_year = datetime.now().year
        date = datetime.strptime(f'{current_year}-{fiscal_year_start_date}', '%Y-%m-%d')
        now = datetime.now()

    # Determine the fiscal year start and end dates
        if date > now:
            start = datetime(current_year - 1, date.month, date.day)
            end = datetime(current_year, date.month, date.day)
        else:
            start = datetime(current_year, date.month, date.day)
            end = datetime(current_year + 1, date.month, date.day)
        fiscal_year_start_str = start.strftime('%Y-%m-%d')
        fiscal_year_end_str = end.strftime('%Y-%m-%d')

    # Fetch data from the database
        if admin_user.get("lifo_fifo") == "fifo":
            received_orders = self.received_order_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}})
        else:
            received_orders = self.received_order_DB.find({'date': {'$gte': fiscal_year_end_str, '$lte': fiscal_year_start_str}})

        sales = self.sales_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}}, {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})

    # Calculate COGS
        cogs = sum(int(float(doc['quantity'])) * int(float(doc.get('price', 0))) for doc in sales if 'quantity' in doc and 'price' in doc)

    # Calculate inventory at start and end of period (simplified example)
        inventory_initial = sum(doc['quantity'] * doc.get('price', 0) for doc in received_orders)
        inventory_final = inventory_initial  # Assuming no inventory change for simplification

        average_inventory = (inventory_initial + inventory_final) / 2
        return cogs / average_inventory if average_inventory else 0

    def COGS(self):
        revenue = 0
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
        if admin_user.get("lifo_fifo") == "fifo":
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_start_str, '$lte': fiscal_year_end_str}})
        else:
            cursor = self.received_order_DB.find({'date': {'$gte': fiscal_year_end_str, '$lte': fiscal_year_start_str}})
        cursor2 = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'quantity': 1, 'price': 1})
        cogs = 0
        for document in cursor2:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                num = document.get("quantity", 0)
                for entry in cursor:
                    if entry.get("SKU", 0) == document.get("SKU", 0):
                        cogs += entry.get("price", 0)
        return cogs
                




