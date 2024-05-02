# Import modules needed
import bcrypt
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Initialize constants for input validation
capitals = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
           'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)


class LoginSystem:

    # Initialize connection to the access details database
    def __init__(self):
        self.username = None
        self.status = None
        self.fiscal_year = None
        self.lifo_fifo = None
        uri = ("mongodb+srv://Admin:Admin@businessinventorychecke.hnarzhd.mongodb.net/?retryWrites=true&w=majority"
               "&appName=BusinessInventoryChecker&tlsInsecure=true")
        client = MongoClient(uri, server_api=ServerApi('1'))
        self.data_base = client['LoginSystem']
        self.login_DB = self.data_base['AccessDetails']

    # Function for logging in
    def login(self, username, password):
        user_check = self.login_DB.find_one({'username': username})
        if user_check:
            if bcrypt.checkpw(password.encode('utf8'), user_check['password']):
                self.username = username
                self.status = user_check.get('status')
                self.fiscal_year = user_check.get('fiscal_year')
                self.lifo_fifo = user_check.get('lifo_fifo')
                print("Success")
                return True
        print("Wrong Password")

    # Function for registering
    def register(self, username, password, status):
        user_check = self.login_DB.find_one({'username': username})
        case = False
        if user_check:
            print("User Exists!")
            case = True
        capital = False
        special = False
        number = False
        if capital is False or special is False or number is False or len(password) < 8:
            if len(password) < 8:
                print("Minimum 8 Characters!")
                case = True
            for letter in password:
                if letter in str(numbers):
                    number = True
                if letter not in str(numbers) and letter not in letters and letter not in capitals:
                    special = True
                if letter in capitals:
                    capital = True
            if number is False:
                print("Need Numbers!")
                case = True
            if special is False:
                print("Need Special Characters!")
                case = True
            if capital is False:
                print("Need Capitals!")
                case = True
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        if status == "ReadWrite":
            self.status = "ReadWrite"
        elif status == "Admin":
            self.status = "Admin"
        elif status == "Read":
            self.status = "Read"
        else:
            print("Wrong Status!")
            case = True
        if case:
            return False
        else:
            self.username = username
            self.status = status
            self.fiscal_year = admin_user.get('fiscal_year')
            self.lifo_fifo = admin_user.get('lifo_fifo')
            hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
            self.login_DB.insert_one(
                {'username': username, 'password': hashed_password, 'status': status, 'fiscal_year': self.fiscal_year,
                 'lifo_fifo': self.lifo_fifo})
            print("Success")
            return True

    # Function for only admin being able to change the fiscal year
    def change_fiscal_year(self, date, status):
        if status != "Admin":
            print("You can not change the fiscal year!")
            return False
        self.login_DB.update_many({}, {"$set": {"fiscal_year": date}})
        return True

    # Function for only the admin to change LIFO/FIFO computation
    def change_lifo_fifo(self, lifo_fifo, status):
        if status != "Admin":
            print("You can not change the life or fifo computation!")
            return False
        self.login_DB.update_many({}, {"$set": {"lifo_fifo": lifo_fifo}})
        return True
