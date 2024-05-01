import sys
from datetime import date
from Mathematics import Mathematics
import json
import HelperFunctions
from bson.json_util import dumps
import random
import numpy as np
import updated_checkForReorder



if __name__ == "__main__":
    db = Mathematics()

    if len(sys.argv) == 2:
        if sys.argv[-1] == "get_report":
            _, operation = sys.argv
            cogs = db.COGS()
            gross = db.gross_margin()
            average_inventory = db.average_inventory()
            gross_profit = db.gross_profit()
            ITR = db.inventory_turnover_ratio()
            expected_inv = db.expected_inventory()
            actual_inv = db.actual_inventory()
            shrinkage = db.shrinkage()
            revenue = db.total_revenue_calculator()
            shrinkage_perc = db.shrinkage_percent()

            # Assemble data into a dictionary
            data = {
                'revenue': revenue, 
                "gross": gross,
                "cogs": cogs, 
                "ITR": ITR, 
                "gross_profit": gross_profit, 
                "average_inventory": average_inventory, 
                "expected_inventory": expected_inv, 
                "actual_inventory": actual_inv, 
                "shrinkage": shrinkage, 
                "shrinkage_percent": shrinkage_perc
            }
            
            db.pareto_chart()
            # Print JSON string
            print(json.dumps(data))

        elif sys.argv[-1] == "generate_dashboard":
            _, operation = sys.argv
            page_number = 1
            cursor = list(db.place_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1,'price': 1, 'isReceived': 1}).sort("date", -1))
            length = len(cursor)
            data = []
            start = 0
            for x in range(50):
                if start >= length:
                    break
                else:
                    data.append(cursor[start])
                    start += 1
            db.pareto_chart()
            print(json.dumps(data))

        elif sys.argv[-1] == "kpi_dash":
            _, operation = sys.argv
            cogs = db.COGS()
            gross = db.gross_margin()
            average_inventory = db.average_inventory()
            gross_profit = db.gross_profit()
            ITR = db.inventory_turnover_ratio()
            expected_inv = db.expected_inventory()
            actual_inv = db.actual_inventory()
            shrinkage = db.shrinkage()
            revenue = db.total_revenue_calculator()
            shrinkage_perc = db.shrinkage_percent()

            # Assemble data into a dictionary
            data = {
                'revenue': revenue, 
                "gross": gross,
                "cogs": cogs, 
                "ITR": ITR, 
                "gross_profit": gross_profit, 
                "average_inventory": average_inventory, 
                "expected_inventory": expected_inv, 
                "actual_inventory": actual_inv, 
                "shrinkage": shrinkage, 
                "shrinkage_percent": shrinkage_perc
            }

            # Print JSON string
            print(json.dumps(data))

        elif sys.argv[-1] == "noti":
            _, operation = sys.argv
            cursor = db.product_DB.find({}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
            for document in cursor:
                SKU = document.get("SKU")
                updated_checkForReorder.predictDemand(SKU)

    elif len(sys.argv) == 3:
        if sys.argv[-1] == "received":
            _, data, operation = sys.argv
            db.received(data)

        elif sys.argv[-1] == "get sales":
            _, page_number_str, operation = sys.argv
            page_number = int(page_number_str)
            cursor = list(
                db.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1, }).sort("date", -1))
            length = len(cursor)
            data = []
            start = (int(page_number_str) - 1) * 50
            if cursor:
                for x in range(50):
                    if start > length:
                        break
                    else:
                        data.append(cursor[start])
                        start += 1
            print(json.dumps(data))

        elif sys.argv[-1] == "get orders":
            _, page_number_str, operation = sys.argv
            page_number = int(page_number_str)
            cursor = list(db.place_order_DB.find({},{'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1, 'isReceived': 1}).sort("date", -1))
            length = len(cursor)
            data = []
            start = (int(page_number_str) - 1) * 50
            for x in range(50):
                if start >= length:
                    break
                else:
                    data.append(cursor[start])
                    start += 1
            page_number = int(page_number_str)
            cursor = list(db.received_order_DB.find({},{'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'price': 1}).sort("date", -1))
            length = len(cursor)
            start = (int(page_number_str) - 1) * 50
            for x in range(50):
                if start >= length:
                    break
                else:
                    data.append(cursor[start])
                    start += 1
            print(json.dumps(data))

        elif sys.argv[-1] == "get product":
            _, page_number_str, operation = sys.argv
            page_number = int(page_number_str)
            cursor = list(db.product_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1}))
            length = len(cursor)
            data = []
            start = (int(page_number_str) - 1) * 50
            for x in range(50):
                if start > length:
                    break
                else:
                    try:
                        data.append(cursor[start])
                        start += 1
                    except IndexError:
                        break
                    
            print(json.dumps(data))
                
    elif len(sys.argv) == 4:
        if sys.argv[-1] == "login":
            _, username, password, operation = sys.argv
            db.login(username, password)
            
        elif sys.argv[-1] == "change fiscal year":
            _, date, username, operation = sys.argv
            status = HelperFunctions.status_check(db, username)
            new_date = HelperFunctions.check_fiscal_year(date)
            if new_date != False and status == "Admin":
                datesend = date[5:7]+"/"+date[8:10]
                db.change_fiscal_year(datesend,status)
                print("Success")
            else:
                print("You dont have the rights to change the fiscal year")
                
        elif sys.argv[-1] == "change lifo fifo":
            _, lifo_fifo, username, operation = sys.argv
            status = HelperFunctions.status_check(db, username)
            if lifo_fifo == 'lifo' or lifo_fifo == 'fifo' and status == "Admin":
                db.change_lifo_fifo(lifo_fifo,status)
            else:
                print("You dont have the rights to change to lifo or fifo")
            
    elif len(sys.argv) == 5:
        if sys.argv[-1] == "register":
            _, username, password, status, operation = sys.argv
            db.register(username, password, status)

    elif len(sys.argv) == 7:
        if sys.argv[-1] == "place order":
            _, date, SKU, product_name, quantity, price, operation = sys.argv
            date_checker = HelperFunctions.normal_date_checker(date)
            # SKU_checker = db.SKU_Checker(SKU)
            db.place_order(date, SKU, product_name, quantity, price)

        elif sys.argv[-1] == "add sale":
            _, date, SKU, product_name, quantity, price, operation = sys.argv
            #date_checker = HelperFunctions.normal_date_checker(date)
            # SKU_checker = db.SKU_Checker(SKU)
            # if quantity > 0 and price > 0 and SKU_checker != False and date_checker != False:
            db.add_sale(date, SKU, product_name, quantity, price)
            # else:
            #if quantity <= 0:
            #    print("Please enter correct number of items!")
            #if price <= 0:
            #    print("Please enter correct price!")
            
    else:
        print("Usage: LoginSystem.py <username> <password>")
        sys.exit(1)
        
        

        
        
      
