# Importing  modules
from Received_Order import Received_Order


# Define Mathematics class which inherits from Received Order class
class Mathematics(Received_Order):

    # Initialising the Mathematics child class using the parent class' initializer
    def __init__(self):
        super().__init__()

    # Function to calculate and return gross profit by subtracting cost of goods sold (cogs) from total revenue
    def gross_profit(self):
        revenue = self.total_revenue_calculator()
        cogs = self.cogs()
        return revenue - cogs

    # Function to calculate and return gross margin percentage
    def gross_margin(self):
        gross_profit = self.gross_profit()
        revenue = self.total_revenue_calculator()
        return gross_profit / revenue * 100

    # Function to compute the average inventory during the fiscal year by calculating initial and final inventory
    def average_inventory(self):
        fiscal_year_start_str, fiscal_year_end_str, admin_user = self.get_fiscal_year_admin()
        cursor = self.place_order_DB.find({})
        initial_inventory = 0
        final_inventory = 0
        for document in cursor:
            if document.get('date', 0) <= fiscal_year_start_str:
                initial_inventory += int(float(document.get("quantity", 0))) * int(float(document.get("price", 0)))
            if document.get('date', 0) >= fiscal_year_end_str:
                final_inventory += int(float(document.get("quantity", 0))) * int(float(document.get("price", 0)))
        return (initial_inventory + final_inventory) / 2

    # Function to compute inventory turnover ratio
    def inventory_turnover_ratio(self):
        cogs = self.cogs()
        average_inventory = self.average_inventory()
        return float(cogs) / float(average_inventory)

    # Function to calculate cost of goods sold based on either Last-In-First-Out lifo or fifo setting
    def cogs(self):
        fiscal_year_start_str, fiscal_year_end_str, admin_user = self.get_fiscal_year_admin()
        if admin_user.get("lifo_fifo") == "fifo":
            cursor = self.received_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'quantity': 1, 'price': 1})
        else:
            cursor = self.received_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'quantity': 1, 'price': 1})
        cursor2 = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'quantity': 1, 'price': 1})
        cogs = 0
        for document in cursor2:
            if fiscal_year_start_str <= document.get('date', 0) <= fiscal_year_end_str:
                num = int(float(document.get("quantity", 0)))
                for entry in cursor:
                    if entry.get("SKU", 0) == document.get("SKU", 0) and num > 0:
                        cogs += int(float(entry.get("price", 0)))
                        num -= 1
        return cogs
