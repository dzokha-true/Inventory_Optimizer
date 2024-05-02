from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Sales import Sales

letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
'y', 'z')
capitals = (
'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
'Y', 'Z')
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)


class Place_Order(Sales):

    def __init__(self):
        super().__init__()
        URI = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority"
               "&appName=BusinessInventoryChecker&tlsInsecure=true")
        client = MongoClient(URI, server_api=ServerApi('1'))
        self.data_base = client['CompanyDetails']
        self.place_order_DB = self.data_base['OrdersPlaced']

    def place_order(self, date, SKU, product_name, quantity, price):
        self.place_order_DB.insert_one({
            "date": date,
            "SKU": SKU,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "isReceived": False
        })
        print("Success")
