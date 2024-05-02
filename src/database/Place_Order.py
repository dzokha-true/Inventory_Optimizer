# Import modules
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Sales import Sales


# Place Order class which inherits from Sales class
class Place_Order(Sales):

    # Constructor which calls the parent class constructor and assigns a place_order_DB variable for a database access
    def __init__(self):
        super().__init__()
        URI = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority"
               "&appName=BusinessInventoryChecker&tlsInsecure=true")
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.place_order_DB = self.data_base['OrdersPlaced']

    # Function called place order which updated the database to add a new order which is in transit
    def place_order(self, date, sku, product_name, quantity, price):
        self.place_order_DB.insert_one({
            "date": date,
            "SKU": sku,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "isReceived": False
        })
        print("Success")
