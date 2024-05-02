# Import modules
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Place_Order import Place_Order
from datetime import datetime


# Received Order class which inherits form Place Order
class Received_Order(Place_Order):

    # Constructor for Received order which calls parent constructor and assigns Orders Received Database to variable
    def __init__(self):
        super().__init__()
        URI = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/"
               "?retryWrites=true&w=majority&appName=BusinessInventoryChecker&tlsInsecure=true")
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.received_order_DB = self.data_base['OrdersReceived']

    # Function which updates the database and the table when an item is received by the company
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
            self.received_order_DB.insert_one({"date": new_date, "SKU": split_data[1],
                                               "product_name": split_data[2], "price": split_data[4]})
        if self.product_DB.find_one({'SKU': split_data[1]}):
            item = self.product_DB.find_one({'SKU': split_data[1]})
            quantity = int(item.get("quantity"))
            quantity += int(split_data[3])
            self.product_DB.update_one({'SKU': split_data[1]}, {"$set": {"quantity": str(quantity)}})
        else:
            self.product_DB.insert_one({"SKU": split_data[1], "product_name": split_data[2],
                                        "quantity": split_data[3], "price": split_data[4], })
        self.place_order_DB.update_one(
            {'date': split_data[0], 'SKU': split_data[1], "product_name": split_data[2], "quantity": split_data[3],
             "price": split_data[4]}, {'$set': {"isReceived": True}})
        print("Success")

    # Function for calculating and returning the expected inventory of a company
    def expected_inventory(self):
        fiscal_year_start_str, fiscal_year_end_str, admin_user = self.get_fiscal_year_admin()
        expected = 0
        cursor = self.place_order_DB.find({},
                                          {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
        for document in cursor:
            if fiscal_year_start_str <= document.get('date', 0) <= fiscal_year_end_str:
                expected += int(float(document.get('price', 0))) * int(float(document.get('quantity', 0)))
        return expected

    # Function for calculating and returning the actual inventory of a company
    def actual_inventory(self):
        fiscal_year_start_str, fiscal_year_end_str, admin_user = self.get_fiscal_year_admin()
        actual = 0
        cursor = self.received_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'price': 1})
        for document in cursor:
            if fiscal_year_start_str <= document.get('date', 0) <= fiscal_year_end_str:
                actual += int(float(document.get('price', 0)))
        return actual

    # Function for calculating and returning the shrinkage of a company
    def shrinkage(self):
        expected = self.expected_inventory()
        actual = self.actual_inventory()
        return expected - actual

    # Function for calculating and returning the shrinkage percent of a company
    def shrinkage_percent(self):
        expected = self.expected_inventory()
        actual = self.actual_inventory()
        return ((expected - actual) / expected) * 100
