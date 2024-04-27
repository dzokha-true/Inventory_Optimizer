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
    var table = document.getElementById('kpi');

    const our_data = JSON.parse(data.dataset);

    table.innerHTML = "";
    
    table.innerHTML += "<li class=\"table-row\">"
     + "<div class=\"col col-1\" data-label=\"gross\">" + our_data.gross + "</div>"
     + "<div class=\"col col-2\" data-label=\"cogs\">" + our_data.cogs + "</div>"
     + "<div class=\"col col-3\" data-label=\"ITR\">" + our_data.ITR + "</div> " + "</li>";
}

function addHTMLPerformance(){
    // Get the reference to the image element
    var image1 = document.getElementById('PRD');

    // Change the src attribute of the images to reload them
    image1.src = "PRD.png";
}

const message = "generate_report"; // to be changed later
ipcRenderer.send('get_report', {message});