// global variable declaration for each function

// from login class 

// from product class
const display_all_product = () =>{
    fetch('http://localhost:5000/get/all_product',{
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
    })
    .then(resp => resp.json())
    .then(data =>console.log(data))
    .catch(error => console.log(error))
}

const display_product_name = (name) =>{
    fetch('http://localhost:5000/get/product/name',{
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
    })
    .then(resp => resp.json())
    .then(data => console.log(data))
    .catch(error => console.log(error))
}

const display_product_sku = (sku) =>{
    fetch('http://localhost:5000/get/product/SKU',{
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
    })
    .then(resp => resp.json())
    .then(data =>console.log(data))
    .catch(error => console.log(error))
}

const display_product_class = (Class_sku) =>{
    fetch('http://localhost:5000/get/product/SKU',{
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
    })
    .then(resp => resp.json())
    .then(data =>console.log(data))
    .catch(error => console.log(error))
}

// from sales class

// from received order

// from place order

// from math