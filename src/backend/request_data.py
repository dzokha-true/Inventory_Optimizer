import mainHeader

def request_data(data_type,data):

    status = mainHeader.LoginSystem()
    db_product = mainHeader.Product(status)
    db_transaction = mainHeader.Transaction(status)

    if data_type == 'product_name':
        result = db_product.find({'product_name': data})
    elif data_type == 'SKU':
        result = db_product.find({'SKU': data})
    elif data_type == 'stock':
        result = db_product.find({'stock': data})
    elif data_type == 'transaction_type':
        result = db_transaction.find({'transaction_type': data})
    elif data_type == 'price':
        result = db_transaction.find({'price': data})
    elif data_type == 'date':
        result = db_transaction.find({'date': data})

    return result