from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Place_Order import Place_Order
from datetime import datetime


class Received_Order(Place_Order):

    def __init__(self):
        super().__init__()
        URI = "mongodb+srv://" + self.status + ":" + self.status + "@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true"
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.received_order_DB = self.data_base['OrdersReceived']

    def received(self, data):
        split_data = data.split(',')
        quantity = int(split_data[3])
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
                "SKU": split_data[1],
                "product_name": split_data[2],
                "price": split_data[4]
            })
        if self.product_DB.find_one({'SKU': split_data[1]}):
            item = self.product_DB.find_one({'SKU': split_data[1]})
            quantity = int(item.get("quantity"))
            quantity += int(split_data[3])
            self.product_DB.update_one({'SKU': split_data[1]}, {"$set": {"quantity": str(quantity)}})
        else:
            self.product_DB.insert_one({
                "SKU": split_data[1],
                "product_name": split_data[2],
                "quantity": split_data[3],
                "price": split_data[4],
            })
        self.place_order_DB.update_one(
            {'date': split_data[0], 'SKU': split_data[1], "product_name": split_data[2], "quantity": split_data[3],
             "price": split_data[4]}, {'$set': {"isReceived": True}})
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
        cursor = self.place_order_DB.find({},
                                          {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
        for document in cursor:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                expected += int(float(document.get('price', 0))) * int(float(document.get('quantity', 0)))
        return expected

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
                actual += int(float(document.get('price', 0)))
        return actual

    def shrinkage(self):
        expected = self.expected_inventory()
        actual = self.actual_inventory()
        return expected - actual

    def shrinkage_percent(self):
        expected = self.expected_inventory()
        actual = self.actual_inventory()
        return ((expected - actual) / expected) * 100