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
            choice = input("What would you like to do? Options are as follows (Input the number correspondent to the action):\n(1) add product\n(2) update product using name\n(3) update product using SKU\n(4) delete product using name\n(5) delete product using SKU\n(6) display all items\n(7) display a specific item using name\n(8) display a specific item using SKU\n(0) quit: ")
            while choice != "0":
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
                    
                choice = input("What would you like to do? Options are as follows (Input the number correspondent to the action):\n(1) add product\n(2) update product using name\n(3) update product using SKU\n(4) delete product using name\n(5) delete product using SKU\n(6) display all items\n(7) display a specific item using name\n(8) display a specific item using SKU\n(0) quit: ")
        
        # BELOW IS TRANSACTIONS WHICH STILL HAS TO BE DONE
        
        elif choice == "1":
            db = mainHeader.Transaction(status)
            choice = print("What would you like to do? Options are as follows (Input the number correspondent to the action):\n(1)")
            while choice != "0":
                db.add_transaction("11-18-2004","AAA-111-A-1","LG Fridge", "Sale", 500, 25.50)
                choice = print("What would you like to do? Options are as follows (Input the number correspondent to the action):\n(1)")
        else:
            choice = input("Please enter a proper command: ")
    print("Program is shutting down")
    
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
            stock = int(input("Enter the new amount in stock: "))
            if stock > 1:
                case = False
            else:
                print("Enter a number greater than one!")
        except ValueError as ve:
            print("Please enter a number")
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