const { spawn } = require('child_process');
const {ipcRenderer} = require("electron");

document.getElementById('addbutton').addEventListener('click', (event) => {
    event.preventDefault();
    const message = "generate_report"; // to be changed later
    ipcRenderer.send('get_report', {message});
  });

ipcRenderer.on('performance-success', (event, data) => {
    const our_data = data.response;
    addHTMLPerformance();
    // load pdf function??
});

function addHTMLPerformance(){
    var picture = document.getElementById('display_area_performance');

    // change the name of report picture
    picture.innerHTML += "<img src=\"img1.jpg\" alt=\"PRD\" width=\"500\" height=\"600\">"
    + "<img src=\"img2.jpg\" alt=\"KPI\" width=\"500\" height=\"600\">"
    + "<img src=\"img3.jpg\" alt=\"Net Sales\" width=\"500\" height=\"600\">";
}