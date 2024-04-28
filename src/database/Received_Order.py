from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Place_Order import Place_Order
from datetime import datetime

letters = ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z')
capitals = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
numbers = (1,2,3,4,5,6,7,8,9,0)

class Received_Order(Place_Order):
    
    def __init__(self):
        super().__init__()
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.received_order_DB = self.data_base['OrdersReceived']

    def received(self, data):
        split_data = data.split(',')
        quantity = int(data[3])
        now = datetime.now()
        date = datetime.strptime(f'{now.year}-{now.month}-{now.day}', '%Y-%m-%d')
        new_date = (str(date.year))
        if len(str(date.month)) == 1:
            new_date = "-0" + str(date.month)
        else:
            new_date = "-" + str(date.month)
        if len(str(date.day)) == 1:
            new_date = "-0" + str(date.day)
        else:
            new_date = "-" + str(date.day)
        for x in range(quantity):
            self.received_order_DB.insert_one({
                "date": new_date,
                "SKU": data[1],
                "product_name": data[2],
                "price": data[4]
            })
        if self.product_DB.find_one({'SKU': data[1]}):
            item = self.product_DB.find_one({'SKU': data[1]})
            quantity = int(item.get("quantity"))
            quantity += int(data[3])
            self.product_DB.update_one({'SKU': data[1]}, {"quanity": str(quantity)})
        else:
            self.product_DB.insert_one({
                "SKU": data[1],
                "product_name": data[2],
                "quantity": data[3],
                "price": data[4],
                "SKU_class": 'C'
            })
        result = self.place_order_DB.update_one({'date': data[0], 'SKU': data[1], "product_name": data[2], "quantity": data[3], "price": data[4]}, {'$set': {"isReceived": True}})
        self.SKU_class()
        print("Success")

    def expected_inventory(self):
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
        expected = 0
        cursor = self.place_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
        for document in cursor:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                expected += document.get('price', 0) * document.get('quantity', 0)
        print(expected)

    def actual_inventory(self):
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
        actual = 0
        cursor = self.received_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'price': 1})
        for document in cursor:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                expected += document.get('price', 0)
        print(actual)

    def shrinkage(self):
        print(self.expected_inventory() - self.actual_inventory())

    def shrinkage_percent(self):
        print((self.expected_inventory() - self.actual_inventory()) / self.expected_inventory()) * 100
