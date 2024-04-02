import mainHeader
import re
        
def main():
    
    # NEEDS TO BE REMOVED (PURPOSE: DEBUGGING)
    #print(mainHeader.testing("vug", "Testing123!"))
    # NEEDS TO BE REMOVED (PURPOSE: DEBUGGING)
    
    status = mainHeader.LoginSystem()
    choice = input("What would you like to access?\n(1) transactions\n(2) product information\n(0) quit: ")
    while choice != "0":
        if choice == "2":
            db = mainHeader.Product(status)
            while choice != "0":
                choice = input("What would you like to do? Options are as follows (Input the number correspondent to the action):\n(1) add product\n(2) update product using name\n(3) update product using SKU\n(4) delete product using name\n(5) delete product using SKU\n(6) display all items\n(7) display a specific item using name\n(8) display a specific item using SKU\n(0) quit: ")

                if choice == "1":
                    
                    SKU = SKU_Checker()
                    product_name = input("Enter the product name: ")
                    stock = stock_Checker()
                    
                    db.add_product(SKU, product_name, stock)
                    
                elif choice == "2":
                    
                    name = input("Enter the name of the product: ")
                    stock = stock_Checker()
                    
                    db.update_product_usingName(name, stock)
                    
                elif choice == "3":
                    
                    SKU = SKU_Checker()
                    stock = stock_Checker()
                    
                    db.update_product_usingSKU(SKU, stock)
                    
                elif choice == "4":
                    
                    name = input("Enter the name of the product: ")
                    
                    db.delete_product_usingName(name)
                    
                elif choice == "5":
                    
                    SKU = SKU_Checker()
                    
                    db.delete_product_usingSKU(SKU)
                    
                elif choice == "6":
                    
                    db.get_product_everything()
                    
                elif choice == "7":
                    
                    name = input("Enter the name of the product: ")
                    
                    db.get_product_name(name)
                    
                elif choice == "8":
                    
                    SKU = SKU_Checker()

                    db.get_product_SKU(SKU)
                
                elif choice != 0:
                    print("Please enter the correct operation!")
                    
        
        # BELOW IS TRANSACTIONS WHICH STILL HAS TO BE DONE
        
        elif choice == "1":
            db = mainHeader.Transaction(status)

            while choice != "0":
                choice = input("What would you like to do? Options are as follows (Input the number correspondent to the action):\n(1) Add Transaction\n(2) Update Transaction\n(3) Delete Transaction\n(4) Show all transactions of a specific date\n(5) Show all transactions with product name\n(6) Show all transactions with SKU\n(7) Show all transactions of a specific type\n(8) Show all transactions\n(9) Change transaction to CSV file \n(10) Import CSV file to Transaction Database\n(0) quit: ")
                
                if choice == '1':
                    
                    date = date_checker()
                    SKU = SKU_Checker()
                    product_name = input("Enter the name of the product: ")
                    transaction_type = transaction_type_checker()
                    stock = stock_Checker()
                    price = price_Checker()
                    
                    db.add_transaction(date, SKU, product_name, transaction_type, stock, price, status)
                
                elif choice == '2':
                    
                    date = date_checker()
                    SKU = SKU_Checker()
                    product_name = input("Enter the name of the product: ")
                    transaction_type = transaction_type_checker()
                    stock = stock_Checker()
                    price = price_Checker()
                    
                    db.update_transaction(date, SKU, product_name, transaction_type, stock, price)
                    
                elif choice == '3':
                    
                    date = date_checker()
                    SKU = SKU_Checker()
                    product_name = input("Enter the name of the product: ")
                    transaction_type = transaction_type_checker()
                    stock = stock_Checker()
                    price = price_Checker()
                    
                    db.delete_transaction(date, SKU, product_name, transaction_type, stock, price, status)
                        
                elif choice == '4':
                    
                    date = date_checker()
                    
                    db.get_transaction_everything_day(date)
                        
                elif choice == '5':
                    
                    product_name = input("Enter the name of the product: ")

                    db.get_transaction_everything_name(product_name)
                    
                elif choice == '6':
                    
                    SKU = SKU_Checker()
                    
                    db.get_transaction_everything_SKU(SKU)
                        
                elif choice == '7':
                    
                    transaction_type = transaction_type_checker()

                    db.get_transaction_everything_type(transaction_type)
                    
                elif choice == '8':
                    
                    db.get_transaction_all()
                                    
                elif choice == '9':
                    
                    db.transaction_to_csv()
                                        
                elif choice == '10':
                    
                    db.csv_to_transaction()
                    
                elif choice != '0':
                    print("Please enter the correct operation!")
        
        else:
            choice = input("Please enter a proper command: ")
    print("Program is shutting down")

def date_checker():
    date = input("Please enter the date in the format (YYYY-MM-DD): ")
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date):
        return date
    else:
        print("Please enter the correct format!")
        return date_checker()
    
def transaction_type_checker():
    case = True
    while case:
        transaction_type = input("Please enter the transaction type (Sale or Order): ")
        if transaction_type == "Sale" or transaction_type == "Order":
            case = False
    return transaction_type
    
def price_Checker():
    case = True
    while case:
        try:
            price = int(input("Enter the cost: "))
            if price > 1:
                case = False
            else:
                print("Enter a number greater than zero!")
        except ValueError as ve:
            print("Please enter a number!")
            case = True      
    return price
    
def SKU_Checker():
    case = True
    while case:
        SKU = input("Enter the SKU in the format AAA-111-A-1: ")
        if re.match('^[A-Z]{3}-[0-9]{3}-[A-Z]{1}-[0-9]{1}$', SKU):
            case = False
        else:
            print("Please enter the SKU in the correct format")
    return SKU

def stock_Checker():
    case = True
    stock = 0
    while case:
        try:
            stock = int(input("Enter the stock number: "))
            if stock >= 0:
                case = False
            else:
                print("Enter a number greater than one!")
        except ValueError as ve:
            print("Please enter a number!")
            case = True      
    return stock


#Order_db = ....

# fill in the name of csv
# format: date, SKU, name, sale, quantity price
#with open('fridge.csv', newline='') as csvfile:
#    myreader = csv.reader(csvfile)
#    for row in myreader:
#        Stock_db.add_item(row[0],row[1],row[2],row[3],row[4],row[5])



# add information to second database TBD


#close file
#csvfile.close()

main()