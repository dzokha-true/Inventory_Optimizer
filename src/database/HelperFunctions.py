from datetime import datetime
from datetime import date
import re

# Checks if a format of the fiscal year entered by the user is correct
# If it is valid, it returns the date in datetime obkect, else returns false
def check_fiscal_year(date):
    date_format = "%m-%d"
    try:
        temp = datetime.strptime(date, date_format)
        return temp
    except ValueError:
        print("Invalid format. Please ensure the date is in MM-DD format!")
        return False

# Checks what is the status of the user and returns the corresponding status
def status_check(object, username):
    user = object.login_DB.find_one({'username': username})
    status = user.get('status')
    if status == "ReadWrite":
        return "ReadWrite"
    elif status == "Admin":
        return "Admin"
    else:
        return "Read"

# Checks if the SKU is in a correct format and returns false or true depending if it is correct
def SKU_Checker(SKU):
    if re.match('^[A-Z]{3}-[0-9]{3}-[A-Z]{1}-[0-9]{1}$', SKU):
        print("Invalid format. Please ensure the SKU is in AAA-111-A-1 format!")
        return False
    else:
        return True

# Checks if the date inputed is in correct format and returns the date if it true, else returns false
def normal_date_checker(date_input):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_input):
        print("Invalid format. Please ensure the date is in YYYY-MM-DD format.")
        return False
    else:
        try:
            year, month, day = map(int, date_input.split('-'))
            my_date = date(year, month, day)
            return date_input
        except ValueError:
            print("Invalid date. Please make sure the date is correct format (YYYY-MM-DD).")
            return False
