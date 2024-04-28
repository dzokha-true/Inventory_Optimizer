const { spawn } = require('child_process');
const {ipcRenderer} = require("electron");

// check id later
document.getElementById('settingPopup').addEventListener('click', (event) => {
    event.preventDefault();
    const start = document.getElementById('startdate').value;
    const end = document.getElementById('enddate').value;
    const message = "change_date";
    // discuss with groups
    ipcRenderer.send('send date', {start,end,message});
    // or set date in local storage and send them along with other info for function we need
    localStorage.setItem('start', start);
    localStorage.setItem('end', end); 
  });

  // check id later
document.getElementById('fifolifoPopup').addEventListener('click', (event) => {
    event.preventDefault();
    const fifo = document.getElementById('fifo');
    const lifo = document.getElementById('lifo');
    const message = "fifo_lifo";
    if(lifo.checked == true && fifo.checked == true){
        alert("choose one of two options");
    }else if(lifo.checked == false && fifo.checked == false){
        alert("choose one");
    }else{
        // discuss with groups
        ipcRenderer.send('change fifo lifo', {start,end,message});
        const status = lifo.checked ? "lifo": "fifo" ;
        // or set date in local storage and send them along with other info for function we need
        localStorage.setItem('fifo-lifo', status);
    }
  });

function addHTMLNoti(data) {
    var notibar = document.getElementById('notiPopup');

    // return produt name from back end
    const product = data.response;
    
    notibar.innerHTML += "<div class=\"row single-notification-box unread\"><div class=\"col-11 notification-text\"><p>"
    + "<a href=\"#\" class=\"link name\">"+product+"</a><span class=\"description\">needed reorder</span>"
    + "<a class=\"link\" href=\"order.html\">Go to Orders Page!</a><span class=\"unread-symbol\">•</span> </p>"
    + "<p class=\"time\">1m ago</p></div> </div>";
}

ipcRenderer.on('get noti', (event, data) => {

    const our_data = data.response;
    addHTMLNoti(our_data);
});


