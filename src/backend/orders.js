const { spawn } = require('child_process');
const { ipcRenderer } = require('electron');


let abc = 1;
let page = 0;
const pageSize = 50;
let loading = false;
const container = document.getElementById('table-body');

document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('main_container');

    ipcRenderer.on('order_table_success', (event, data) => {
        abc ++;
        const our_data = JSON.parse(data.dataset);
        if (loading) {
            const tbody = document.getElementById('table-body');
            our_data.forEach((item) => {
                const tr = document.createElement('tr');
                if (item.isReceived == false) {
                    tr.innerHTML = `
                    <td>${item.date}</td>
                    <td>${item.SKU}</td>
                    <td>${item.product_name}</td>
                    <td>${item.price}</td>
                    <td>${item.quantity}</td>
                    <td><button id = "button" class="received-btn" data-item='${JSON.stringify(item)}'>Received?</button></td>
                    `;
                    tbody.appendChild(tr);
                }else{
                    tr.innerHTML = `
                    <td>${item.date}</td>
                    <td>${item.SKU}</td>
                    <td>${item.product_name}</td>
                    <td>${item.price}</td>
                    <td>N/A</td>
                    <td>Received</td>
                    `;
                    tbody.appendChild(tr);
                }
            });
            page++;
            loading = false;
        }
    });

    // adding a listener event to the add_product button
document.getElementById('next').addEventListener('click', (event) => {
    event.preventDefault();
    const date_ordered_input = document.getElementById('Date_order').value;
    const price_input = document.getElementById('Price').value;
    const SKU_input = document.getElementById('SKU').value;
    const name_input = document.getElementById('Name').value;
    const amount_input = document.getElementById('Amount').value;
    const message = "place order";
    ipcRenderer.send('place order', {date_ordered_input, SKU_input, name_input, amount_input, price_input, message});

});


    container.addEventListener('click', function(e) {
		if (e.target.classList.contains('received-btn')) {
			const itemData = JSON.parse(e.target.getAttribute('data-item'));
            ipcRenderer.send('processitem', {itemData});
		}
	});

    tableBody.addEventListener('scroll', () => {
        const nearBottom = tableBody.scrollHeight - tableBody.scrollTop <= (tableBody.clientHeight + 20);
        if (nearBottom && !loading) {
            loading = true;
            ipcRenderer.send('create-order-table', { abc });
        }
    });



});
if (!loading) {
    loading = true;
    ipcRenderer.send('create-order-table', { abc });
}

