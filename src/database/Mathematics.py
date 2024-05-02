from datetime import datetime
from Received_Order import Received_Order


class Mathematics(Received_Order):

    def __init__(self):
        super().__init__()

    def gross_profit(self):
        revenue = self.total_revenue_calculator()
        cogs = self.COGS()
        return revenue - cogs

    def gross_margin(self):
        gross_profit = self.gross_profit()
        revenue = self.total_revenue_calculator()
        return gross_profit / revenue * 100

    def average_inventory(self):
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year')
        current_year = datetime.now().year
        fiscal_year_start_date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d')
        fiscal_year_end_date = fiscal_year_start_date.replace(year=fiscal_year_start_date.year + 1)
        if fiscal_year_start_date > datetime.now():
            fiscal_year_start_date = fiscal_year_start_date.replace(year=fiscal_year_start_date.year - 1)
            fiscal_year_end_date = fiscal_year_end_date.replace(year=fiscal_year_end_date.year - 1)
        fiscal_year_start_str = fiscal_year_start_date.strftime('%Y-%m-%d')
        fiscal_year_end_str = fiscal_year_end_date.strftime('%Y-%m-%d')
        cursor = self.place_order_DB.find({})
        initial_inventory = 0
        final_inventory = 0
        for document in cursor:
            if document.get('date', 0) <= fiscal_year_start_str:
                initial_inventory += int(float(document.get("quantity", 0))) * int(float(document.get("price", 0)))
            if document.get('date', 0) >= fiscal_year_end_str:
                final_inventory += int(float(document.get("quantity", 0))) * int(float(document.get("price", 0)))
        return (initial_inventory + final_inventory) / 2

    def inventory_turnover_ratio(self):
        cogs = self.COGS()
        average_inventory = self.average_inventory()
        return cogs / average_inventory if average_inventory else 0

    def COGS(self):
        admin_user = self.login_DB.find_one({'status': 'Admin'})
        date_str = admin_user.get('fiscal_year')
        now = datetime.now()
        current_year = now.year
        date = datetime.strptime(f'{current_year}-{date_str}', '%Y-%m-%d')
        if date > now:
            start = datetime(current_year - 1, date.month, date.day)
            end = datetime(current_year, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')
        else:
            start = datetime(current_year, date.month, date.day)
            end = datetime(current_year + 1, date.month, date.day)
            fiscal_year_start_str = start.strftime('%Y-%m-%d')
            fiscal_year_end_str = end.strftime('%Y-%m-%d')
        if admin_user.get("lifo_fifo") == "fifo":
            cursor = self.received_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'quantity': 1, 'price': 1})
        else:
            cursor = self.received_order_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'quantity': 1, 'price': 1})
        cursor2 = self.sales_DB.find({}, {'_id': 0, 'date': 1, 'SKU': 1, 'quantity': 1, 'price': 1})
        cogs = 0
        for document in cursor2:
            if document.get('date', 0) >= fiscal_year_start_str and document.get('date', 0) <= fiscal_year_end_str:
                num = int(float(document.get("quantity", 0)))
                for entry in cursor:
                    if entry.get("SKU", 0) == document.get("SKU", 0) and num > 0:
                        cogs += int(float(entry.get("price", 0)))
                        num -= 1
        return cogs





