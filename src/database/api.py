from flask import Flask, jsonify
import LoginSystem
import Product
import Sales
import Place_Order
import Received_Order
import Mathematics

app = Flask(__name__)

#from LoginSystem class
# TBD

# from product class
@app.route('/get/all_product',methods = ['POST'])
def get_all_product():
    db = Product()
    return db.get_product_everything()

@app.route('/get/product/name',methods = ['POST'])
def get_product():
    db = Product()
    # product_name = request.json['product_name']
    #need to add name input to query db
    return db.get_product_name()

@app.route('/get/product/SKU',methods = ['POST'])
def get_productSKU():
    db = Product()
    # SKU = request.json['SKU']
    # need to add SKU input to query db
    return db.get_product_SKU()

@app.route('/get/product/class',methods = ['POST'])
def get_productSKUClass():
    db = Product()
    # class = request.json['SKU_class']
    # need to add class to query db
    return db.get_product_SKU_class()

@app.route('/csv/',methods = ['POST'])
def get_csv():
    db = Product()
    # need to check where to locate csv file and what to return
    db.product_to_csv()
    return None

@app.route('/chart/',methods = ['POST'] )
def chart():
    db = Product()
    db.pareto_chart() 
    return None

@app.route('/csvtoproduct/',methods = ['POST'])
def import_csv():
    db = Product()
    jsonfile = db.csv_to_product()
    return jsonfile

@app.route('/add/',methods = ['POST'])
def addproduct():
    db = Product()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.add_product()
    return None

@app.route('/update/',methods = ['POST'])
def updateproduct():
    db = Product()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.update_product()
    return None

@app.route('/delete/',methods = ['DELETE'])
def deleteproduct():
    db = Product()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.delete_product()
    return None


# from Place_Order class
@app.route('/place_order/',methods = ['POST'])
def placeorder():
    db = Place_Order()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.place_order()
    return jsonify({"message":"successful"})

@app.route('/update_order/',methods = ['POST'])
def updateorder():
    db = Place_Order()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.update_order()
    return jsonify({"message":"successful"})

@app.route('/delete_order/',methods = ['DELETE'])
def deleteorder():
    db = Place_Order()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.delete_order()
    return jsonify({"message":"successful"})

@app.route('/ordercsv/',methods = ['POST'])
def ordertocsv():
    db = Place_Order()
    db.place_order_to_csv()
    return None

@app.route('/csvorder/',methods = ['POST'])
def csvtoorder():
    db = Place_Order()
    jsonfile = db.csv_to_place_order()
    return jsonfile

# from Sales class
@app.route('/rev_cal/',methods = ['POST'])
def rev_cal():
    db = Sales()
    revenue = db.revenue_calculator()
    return jsonify({"revenue":revenue})

@app.route('/add_sale/',methods = ['POST'])
def addsale():
    db = Sales()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.add_sale()
    return jsonify({"message":"successful"})

@app.route('/update_sale/',methods = ['POST'])
def updatesale():
    db = Sales()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.update_sale()
    return jsonify({"message":"successful"})

@app.route('/delete_sale/',methods = ['DELETE'])
def deletesale():
    db = Sales()
    # SKU = request.json['SKU']
    # product_name = request.json['product_name']
    # stock = request.json['stock']
    # cost = request.json['cost']
    # inventory_value = request.json['inventory_value']
    # expected_sales = request.json['expected_sales']
    # SKU_class = request.json['SKU_class']

    # need to add more parameter
    db.delete_sale()
    return jsonify({"message":"successful"})

@app.route('/salecsv/',methods = ['POST'])
def saletocsv():
    db = Sales()
    db.sales_to_csv()
    return None

@app.route('/csvsale/',methods = ['POST'])
def csvtosale():
    db = Sales()
    jsonfile = db.csv_to_sales()
    return jsonfile

# from Math class
@app.route('/gross/',methods = ['POST'])
def grossprofit():
    db = Mathematics()
    profit = db.gross_profit()
    return jsonify({"gross_profit":profit})

@app.route('/margin/',methods = ['POST'])
def grossmargin():
    db = Mathematics()
    profit = db.gross_margin()
    return jsonify({"gross_margin":profit})

@app.route('/avg_inv/',methods = ['POST'])
def avg_inv():
    db = Mathematics()
    avg = db.average_inventory()
    return jsonify({"average_inventory":avg})

@app.route('/inv_tov/',methods = ['POST'])
def inv_tov():
    db = Mathematics()
    ratio = db.inventory_turnover_ratio()
    return jsonify({"ratio":ratio})

@app.route('/cogs/',methods = ['POST'])
def cogs_product():
    db = Mathematics()
    cogs = db.COGS()
    return jsonify({"cogs":cogs})

# from Received_Order class
@app.route('/expect_inventory/',methods = ['POST'])
def expect_invent():
    db = Received_Order()
    #cost?
    #num?
    expect = db.expected_inventory(num, cost)
    return jsonify({"expect_invent":expect})

@app.route('/orderreceieve/',methods = ['POST'])
def order():
    db = Received_Order()
    db.order_received()
    return None

@app.route('/actual_inventory/',methods = ['POST'])
def actual_invent():
    db = Received_Order()
    #cost?
    #num?
    actual = db.actual_inventory(num, cost)
    return jsonify({"actual":actual})

@app.route('/shrinkage/',methods = ['POST'])
def shrink():
    db = Received_Order()
    Shrink = db.shrinkage()
    return jsonify({"shrink":Shrink})

@app.route('/shrink_percent/',methods = ['POST'])     
def shrinkpercent():
    db = Received_Order()
    percent = db.shrinkage_percent()
    return jsonify({"percent":percent})
        
@app.route('/receive/ordercsv/',methods = ['POST'])
def reordertocsv():
    db = Received_Order()
    db.place_order_to_csv()
    return None

@app.route('/receive/csvorder/',methods = ['POST'])
def csvtoreorder():
    db = Received_Order()
    jsonfile = db.csv_to_place_order()
    return jsonfile
 
        
        
        
        
        
        


if __name__ == "__main__":
    app.run()