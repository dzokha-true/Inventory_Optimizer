const { spawn } = require('child_process');
const { ipcRenderer } = require('electron');


let abc = 1;
let page = 0;
const pageSize = 50;
let loading = false;
const container = document.getElementById('table-body');

ipcRenderer.on('order_table_success', (event, data) => {
	abc ++;
	const our_data = JSON.parse(data.dataset);
	if (loading) {
		const tbody = document.getElementById('table-body');
		our_data.forEach((item) => {
			const tr = document.createElement('tr');
			tr.innerHTML = `
				<td>${item.date}</td>
				<td>${item.SKU}</td>
				<td>${item.product_name}</td>
				<td>${item.cost}</td>
				<td>${item.num || 'N/A'}</td>
				`;
			tbody.appendChild(tr);
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



document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('main_container');
    console.log("DOMContentLoaded - the script is running");

    tableBody.addEventListener('scroll', () => {
        const nearBottom = tableBody.scrollHeight - tableBody.scrollTop <= (tableBody.clientHeight + 20);
        console.log(`Scrolled to: ${tableBody.scrollTop}, Near bottom: ${nearBottom}`);

        if (nearBottom && !loading) {
            console.log('Approaching bottom: Loading more data...');
            loading = true;
            ipcRenderer.send('create-order-table', { abc });
        }
    });

    // Trigger initial data load
    if (!loading) {
        loading = true;
        ipcRenderer.send('create-order-table', { abc });
    }
});

if (!loading) {
    loading = true;
    ipcRenderer.send('create-order-table', { abc });
}


