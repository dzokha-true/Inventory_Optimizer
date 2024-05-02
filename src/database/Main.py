# Import modules
import sys
from Mathematics import Mathematics
import json
import HelperFunctions
import updated_checkForReorder


# Function to get statistics of the company
def get_stat(database):
    cogs = database.cogs()
    gross = database.gross_margin()
    average_inventory = database.average_inventory()
    gross_profit = database.gross_profit()
    ITR = database.inventory_turnover_ratio()
    expected_inv = database.expected_inventory()
    actual_inv = database.actual_inventory()
    shrinkage = database.shrinkage()
    revenue = database.total_revenue_calculator()
    shrinkage_perc = database.shrinkage_percent()
    calculation = {"revenue": revenue, "gross": gross, "cogs": cogs, "ITR": ITR, "gross_profit": gross_profit,
                   "average_inventory": average_inventory, "expected_inventory": expected_inv,
                   "actual_inventory": actual_inv, "shrinkage": shrinkage, "shrinkage_percent": shrinkage_perc}
    return calculation


# Main Driver Function
if __name__ == "__main__":
    # Initialize the object
    db = Mathematics()

    # Checks if there is only 1 argument in command line
    if len(sys.argv) == 2:

        # Function to get the report for the performance  page
        if sys.argv[-1] == "get_report":
            _, operation = sys.argv
            data = get_stat(db)
            db.pareto_chart()
            print(json.dumps(data))

        # Function to generate the dashboard page
        elif sys.argv[-1] == "generate_dashboard":
            _, operation = sys.argv
            page_number = 1
            cursor = orders = list(db.place_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1,
                                                               'product_name': 1, 'quantity': 1, 'price': 1,
                                                               'isReceived': 1}).sort("date", -1))
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

        # Function to get the kpi of the company
        elif sys.argv[-1] == "kpi_dash":
            _, operation = sys.argv
            data = get_stat(db)
            print(json.dumps(data))

        # Function to check if there is need for reorder
        elif sys.argv[-1] == "noti":
            _, operation = sys.argv
            cursor = db.product_DB.find({}, {'_id': 0, 'SKU': 1, 'product_name': 1, 'quantity': 1, 'price': 1})
            for document in cursor:
                SKU = document.get("SKU")
                updated_checkForReorder.checkForReorder(SKU)

    # Check if there is 2 arguments in command line
    elif len(sys.argv) == 3:

        # Function to mark the item as received
        if sys.argv[-1] == "received":
            _, data, operation = sys.argv
            db.received(data)

        # Function to show a table of sales implementing infinite scroll
        elif sys.argv[-1] == "get sales":
            _, page_number_str, operation = sys.argv
            page_number = int(page_number_str)
            cursor = list(db.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1,
                                                'price': 1, }).sort("date", -1))
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

        # Function to show a table of orders implementing infinite scroll with both order placed and order received
        elif sys.argv[-1] == "get orders":
            _, page_number_str, operation = sys.argv
            page_number = int(page_number_str)
            cursor = list(db.place_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1, 'quantity': 1,
                                                      'price': 1, 'isReceived': 1}).sort("date", -1))
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
            cursor = list(
                db.received_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'product_name': 1,
                                               'price': 1}).sort("date", -1))
            length = len(cursor)
            start = (int(page_number_str) - 1) * 50
            for x in range(50):
                if start >= length:
                    break
                else:
                    data.append(cursor[start])
                    start += 1
            print(json.dumps(data))

        # Function to show a table of products implementing infinite scroll
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

    # Check if there are 3 arguments in command line
    elif len(sys.argv) == 4:

        # Login the user
        if sys.argv[-1] == "login":
            _, username, password, operation = sys.argv
            db.login(username, password)

        # Change the fiscal year for everyone
        elif sys.argv[-1] == "change fiscal year":
            _, date, username, operation = sys.argv
            status = HelperFunctions.status_check(db, username)
            new_date = HelperFunctions.check_fiscal_year(date)
            if new_date is not False and status == "Admin":
                fiscal_year = date[5:7] + "-" + date[8:10]
                db.change_fiscal_year(fiscal_year, status)
                print("Success")
            else:
                print("You dont have the rights to change the fiscal year")

        # Change the lifo or fifo calculation method for everyone
        elif sys.argv[-1] == "change lifo fifo":
            _, lifo_fifo, username, operation = sys.argv
            status = HelperFunctions.status_check(db, username)
            if (lifo_fifo == 'lifo' or lifo_fifo == 'fifo') and status == "Admin":
                db.change_lifo_fifo(lifo_fifo, status)
                print("Success")
            else:
                print("You dont have the rights to change to lifo or fifo")

    # Check if there is 4 arguments in command line
    elif len(sys.argv) == 5:

        # Register the user
        if sys.argv[-1] == "register":
            _, username, password, status, operation = sys.argv
            db.register(username, password, status)

    # Check if there is 6 arguments in command line
    elif len(sys.argv) == 7:

        # Adds an order to the orders_placed database in MongoDB
        if sys.argv[-1] == "place order":
            _, date, SKU, product_name, quantity, price, operation = sys.argv
            date_checker = HelperFunctions.normal_date_checker(date)
            db.place_order(date, SKU, product_name, quantity, price)

        # Adds a sale to the sales database in MongoDB
        elif sys.argv[-1] == "add sale":
            _, date, SKU, product_name, quantity, price, operation = sys.argv
            db.add_sale(date, SKU, product_name, quantity, price)

    # Catch the exceptions and errors
    else:
        print("Usage: LoginSystem.py <username> <password>")
        sys.exit(1)
