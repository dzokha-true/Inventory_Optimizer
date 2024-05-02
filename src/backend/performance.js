const { spawn } = require('child_process');
const {ipcRenderer} = require("electron");

document.addEventListener('DOMContentLoaded', () => {
    const our_setting = document.getElementById('settingPopup');
    if(our_setting){
        our_setting.addEventListener('click', (event) => {
            event.preventDefault();
            const start = document.getElementById('startdate').value;
            const end = document.getElementById('enddate').value;
            const message = "change fiscal year";
            var username = localStorage.getItem('username');
            ipcRenderer.send('send date', {end,username,message});
            // or set date in local storage and send them along with other info for function we need
            localStorage.setItem('start', start);
            localStorage.setItem('end', end); 
          });
    }
    const fifo = document.getElementById('fifo');
    fifo.addEventListener('click', (event) => {
        event.preventDefault();
        const status = "fifo";
        ipcRenderer.send('change lifo fifo', {status,username,message});
        localStorage.setItem('lifo-fifo', status); 
    });
    const lifo = document.getElementById('lifo');
    lifo.addEventListener('click', (event) => {
        event.preventDefault();
        const status = "lifo";
        ipcRenderer.send('change lifo fifo', {status,username,message});
        localStorage.setItem('lifo-fifo', status); 
    });
    
});

ipcRenderer.on('performance-success', (event, data) => {
    addHTMLPerformance();
    addHTMLKPI(data);
});

// check KPI column names
function addHTMLKPI(data) {
    var rev = document.getElementById('revenue_dash');
    var gro = document.getElementById('gross_dash');
    var COGS = document.getElementById('cogs_dash');
    var itr = document.getElementById('ITR_dash');
    var profit = document.getElementById('gross_profit_dash');
    var avg_int = document.getElementById('average_inventory_dash');
    var exp_int = document.getElementById('expected_inventory_dash');
    var act_int = document.getElementById('actual_inventory_dash');
    var shrink = document.getElementById('shrinkage_dash');
    var shrink_per = document.getElementById('shrinkage_percent_dash');

    const our_data = JSON.parse(data.dataset);

    rev.innerHTML = "";
    gro.innerHTML = "";
    COGS.innerHTML = "";
    itr.innerHTML = "";
    profit.innerHTML = "";
    avg_int.innerHTML = "";
    exp_int.innerHTML = "";
    act_int.innerHTML = "";
    shrink.innerHTML = "";
    shrink_per.innerHTML = "";

    rev.innerHTML += Math.round(our_data.revenue);
    gro.innerHTML += Math.round(our_data.gross);
    COGS.innerHTML += Math.round(our_data.cogs);
    itr.innerHTML += our_data.ITR.toFixed(3);
    profit.innerHTML += Math.round(our_data.gross_profit);
    avg_int.innerHTML += Math.round(our_data.average_inventory);
    exp_int.innerHTML += Math.round(our_data.expected_inventory);
    act_int.innerHTML += Math.round(our_data.actual_inventory);
    shrink.innerHTML += Math.round(our_data.shrinkage);
    shrink_per.innerHTML = Math.round(our_data.shrinkage_percent);
}

function addHTMLPerformance(){
    // Get the reference to the image element
    var image1 = document.getElementById('PRD');

    // Change the src attribute of the images to reload them
    image1.src = "../public/images/pareto_chart.png";
}

const message = "get_report"; // to be changed later
ipcRenderer.send('get_report', {message});
