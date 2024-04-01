import csv
import PyMongoManager

Stock_db = PyMongoManager.DataBasemanager()
#Order_db = ....

# fill in the name of csv
# format: date, SKU, name, sale, quantity price
with open('fridge.csv', newline='') as csvfile:
    myreader = csv.reader(csvfile)
    for row in myreader:
        Stock_db.add_item(row[0],row[1],row[2],row[3],row[4],row[5])


# add information to second database TBD


#close file
csvfile.close()