const { spawn } = require('child_process');
const { ipcRenderer } = require('electron');


let abc = 1;
let page = 0;
const pageSize = 50;
let loading = false;
const container = document.getElementById('table-body');

ipcRenderer.on('sale_table_success', (event, data) => {
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
                <td>${item.quantity || 'N/A'}</td>
				<td>${item.price}</td>
				`;
			tbody.appendChild(tr);
		});
		page++;
		loading = false;
	}
});


document.getElementById('next').addEventListener('click', (event) => {
    event.preventDefault();
    const date_input = document.getElementById('date_sale').value;
    const price_input = document.getElementById('price').value;
    const SKU_input = document.getElementById('SKU').value;
    const name_input = document.getElementById('Name').value;
    const amount_input = document.getElementById('Amount').value;
    const message = "add sale";
    ipcRenderer.send('add sale', {date_input, price_input, SKU_input, name_input, amount_input, message});
});

document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('main_container');

    tableBody.addEventListener('scroll', () => {
        const nearBottom = tableBody.scrollHeight - tableBody.scrollTop <= (tableBody.clientHeight + 20);

        if (nearBottom && !loading) {
            loading = true;
            ipcRenderer.send('create-sale-table', { abc });
        }
    });

    // Trigger initial data load
    if (!loading) {
        loading = true;
        ipcRenderer.send('create-sale-table', { abc });
    }
});


