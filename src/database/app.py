from flask import Flask, jsonify
import LoginSystem
import Product
import Sales
import Place_Order
import Received_Order
import Mathematics

app = Flask(__name__)

@app.route('/get/',methods = ['GET'])
def func():
    return jsonify({"num":3})

@app.route('/post/',methods = ['POST'])
def func2():
    return jsonify({"num":3})

@app.route('/put/',methods = ['PUT'])
def func3():
    return jsonify({"num":3})

@app.route('/delete/',methods = ['DELETE'])
def func4():
    return jsonify({"num":3})



if __name__ == "__main__":
    app.run()