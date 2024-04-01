import sys
import os
import bcrypt
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
from time import ctime


MONGO_PASSWORD = quote_plus(os.getenv("PASSWORD"))
URI = (f"mongodb+srv://zmamayev:{MONGO_PASSWORD}@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w"
       f"=majority&appName=BusinessInventoryChecker")
server_api = ServerApi('1')

client = MongoClient(URI, server_api=server_api, tlsAllowInvalidCertificates=True)


class DataBaseManager:
    def __init__(self):
        self.data_base = client['BusinessInverntoryChecker']
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            sys.exit()  # End program if failed.

    def register(self, username, password, codeword):
        users = self.['users']
        codeword = bcrypt.hashpw(codeword.encode(), bcrypt.gensalt())
        codeword_check = users.find_one({'codeword': codeword})
        if codeword_check:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            users_check = users.insert_one({'username': username, 'password': hashed_password})
            return users_check

    def login(self, username, password):
        users = self.data_base['users']
        user_check = users.find_one({'username': username})
        if user_check:
            attempts = 0
            while attempts < 5:
                if bcrypt.checkpw(password.encode(), user_check['password']):
                    return True
                    break
                else:
                    attempts += 1
                    print(f"your password was incorrect. Please try again. You have {5 - attempts} attempts left.")
            if attempts == 5:
                print("You have exceeded the maximum number of attempts. Please try again later.")
                sys.exit(0)
        else:
            print("User does not exist. Please register for an account.")
            return False

    def add_item(self, item_name, item_quantity, item_price): #TODO ID FOR EACH ITEM ADDED
        items = self.data_base['items']
        item_check = items.find_one({'item_name': item_name})
        if item_check:
            print("Item already exists. Please update the quantity instead.")
        else:
            item = items.insert_one({'item_name': item_name, 'item_quantity': item_quantity, 'item_price': item_price})
            return item

    def update_item(self, item_name, item_quantity):
        items = self.data_base['items']
        item_check = items.find_one({'item_name': item_name})
        if item_check:
            item = items.update_one({'item_name': item_name}, {'$set': {'item_quantity': item_quantity}})
            return item
        else:
            print("Item does not exist. Please add the item first.")

    def delete_item(self, item_name):
        items = self.data_base['items']
        item_check = items.find_one({'item_name': item_name})
        if item_check:
            item = items.delete_one({'item_name': item_name})
            return item
        else:
            print("Item does not exist. Please add the item first.")

    def sell_items(self, items_sold: dict):
        """
            :param: item_sold: expects a dictionary with the item name as a key and the quantity sold as a value.
            :return: None
            """
        #TODO ADD PROFIT FROM SALE
        items = self.data_base['items']
        for item in items_sold:
            item_check = items.find_one({'item_name': item})
            if item_check:
                item_quantity = item_check['item_quantity']
                if item_quantity >= items_sold[item]:
                    item = items.update_one({'item_name': item},
                                            {'$set': {'item_quantity': item_quantity - items_sold[item]}})
                    self.data_base['sales'].insert_one({'item_name': item, 'quantity_sold': items_sold[item], 'time': ctime()})
                else:
                    print(f"Item {item} does not have enough quantity to sell.")
            else:
                print(f"Item {item} does not exist. Please add the item first.")


DB = DataBaseManager()
DB.add_item("Hi", 10,500)