const { spawn } = require('child_process');
const { ipcRenderer } = require('electron');


let abc = 1;
let page = 0;
const pageSize = 50;
let loading = false;
const container = document.getElementById('table-body');

document.addEventListener('DOMContentLoaded', function() {
    const tableBody = document.getElementById('main_container');

    ipcRenderer.on('product_table_success', (event, data) => {
        abc ++;
        const our_data = JSON.parse(data.dataset);
        if (loading) {
            const tbody = document.getElementById('table-body');
            our_data.forEach((item) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.SKU}</td>
                    <td>${item.product_name}</td>
                    <td>${item.quantity || 'N/A'}</td>
                    `;
                tbody.appendChild(tr);
            });
            page++;
            loading = false;
        }
    });

    tableBody.addEventListener('scroll', () => {
        const nearBottom = tableBody.scrollHeight - tableBody.scrollTop <= (tableBody.clientHeight + 20);

        if (nearBottom && !loading) {
            loading = true;
            ipcRenderer.send('create-product-table', { abc });
        }
    });

    // Trigger initial data load

});

if (!loading) {
    loading = true;
    ipcRenderer.send('create-product-table', { abc });
}
