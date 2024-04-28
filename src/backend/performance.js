const { spawn } = require('child_process');
const {ipcRenderer} = require("electron");

document.getElementById('addbutton').addEventListener('click', (event) => {
    event.preventDefault();
    const message = "generate_report"; // to be changed later
    ipcRenderer.send('get_report', {message});
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

    rev.innerHTML += our_data.revenue;
    gro.innerHTML += our_data.gross;
    COGS.innerHTML += our_data.cogs;
    itr.innerHTML += our_data.ITR;
    profit.innerHTML += our_data.gross_profit;
    avg_int.innerHTML += our_data.average_inventory;
    exp_int.innerHTML += our_data.expected_inventory;
    act_int.innerHTML += our_data.actual_inventory;
    shrink.innerHTML += our_data.shrinkage;
    shrink_per.innerHTML = our_data.shrinkage_percent;
}

function addHTMLPerformance(){
    // Get the reference to the image element
    var image1 = document.getElementById('PRD');

    // Change the src attribute of the images to reload them
    image1.src = "PRD.png";
}

const message = "generate_report"; // to be changed later
ipcRenderer.send('get_report', {message});