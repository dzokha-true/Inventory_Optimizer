const { spawn } = require('child_process');
const {ipcRenderer} = require("electron");

ipcRenderer.on('dashboard-success', (event, data) => {
    addHTMLPerformance();
    const our_data = JSON.parse(data.dataset);
    for(let i = 0; i < 10; i++){
        adddashboardtable(our_data[i],i+1);
    }
});

ipcRenderer.on('dashboard-success2', (event, data) => {
    addHTMLKPI2(data);
});

function addHTMLKPI2(data) {
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
    var image1 = document.getElementById('trend');

    // Change the src attribute of the images to reload them
    image1.src = "../public/images/pareto_chart.png";
}

// fix and change format to order table
function adddashboardtable(data,i){
    var table = document.getElementById('order_dash');

    table.innerHTML += "<li class=\"table-row\">"
    + "<div class=\"col col-1\" data-label=\"Number\"> <svg class=\"svg-icon productButton\" style=\"width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;\" viewBox=\"0 0 1024 1024\" version=\"1.1\" xmlns=\"http://www.w3.org/2000/svg\">"
    + "<path d=\"M512.197498 752.238526 158.499897 398.540925c-18.73776-18.73776-18.73776-49.092092 0-67.828828s49.092092-18.73776 67.828828 0l285.868773 285.868773 285.868773-285.868773c18.73776-18.73776 49.092092-18.73776 67.828828 0s18.73776 49.092092 0 67.828828L512.197498 752.238526z\"/>"
    + "</svg>" + i + "</div>"
    + "<div class = \"container\"><div class=\"productContent\" id=\"productPopup1\"></div> </div>"
    + "<div class=\"col col-2\" data-label=\"Date\">" + data.date + "</div>"
    + "<div class=\"col col-3\" data-label=\"Arrival\">" + data.arrival + "</div>"
    + "<div class=\"col col-4\" data-label=\"SKU\">" + data.sku + "</div>"
    + "<div class=\"col col-5\" data-label=\"Product\">" + data.product + "</div>"
    + "<div class=\"col col-6\" data-label=\"Quantity\">" + data.quantity + "</div>"
    + "<div class=\"col col-7\" data-label=\"Unit\">" + data.unit + "</div>"
    + "<div class=\"col col-8\" data-label=\"Supplier\">" + data.supplier + "</div> " 
    + "<div class=\"col col-9\" data-label=\"Status\">" + data.status + "</div> "+ "</li>";
}

const message = "generate_dashboard"; // to be changed later
const message2 = "kpi_dash"
ipcRenderer.send('get_dashboard', {message,message2});
