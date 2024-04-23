const { ipcRenderer } = require('electron');

// document.getElementById('loginForm').addEventListener('submit', (event) => {
//     event.preventDefault();
//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;

//     ipcRenderer.send('perform-login', { username, password });
//   });
  
ipcRenderer.on('login-success', (event, arg) => {
    window.location.href = '../views/map.html';
    remote.app.emit('map-page');
   });

ipcRenderer.on('login-failure', (event, data) => {
    if (data.attemptsLeft > 0) {
        document.getElementById('message').textContent = `Login failed. Attempts left: ${data.attemptsLeft}`;
    } else {
        document.getElementById('message').textContent = 'You have exceeded the number of login attempts.';
    }
});

 const box = $(".single-notification-box");
 const markAllAsRead = $("#markAllAsRead");
 const unreadNotificationNumber = $(".unread-notifications-number");

 markAllAsRead.click(function(e){

     console.log("click !");

     if(box.hasClass("unread")){
         box.removeClass("unread");
         box.addClass("read");
         unreadNotificationNumber.text("0");
     }
 });

// function runPythonScript(scriptPath: string = "../LoginSystem.py", username, password) {
//     const python = spawn('python', [scriptPath, ...args]);

//     python.stdout.on('data', (data) => {
//         console.log(stdout: ${data});
//     });

//     python.stderr.on('data', (data) => {
//         console.error(stderr: ${data});
//     });

//     python.on('close', (code) => {
//         console.log(child process exited with code ${code});
//     });
// }

ipcRenderer.on('login-attempt-exceeded', () => {
    document.getElementById('message').textContent = 'You have exceeded the number of login attempts.';
    window.location.href = '../views/index.html';
    remote.app.emit('main-page');
});

ipcRenderer.on('reset-login', (event,arg) => {
    document.getElementById('message').textContent = '';
    // Optionally, clear the username and password fields
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    // Enable the login button if it was previously disabled
    document.getElementById('loginButton').disabled = false;
});

// document.getElementById('registerForm').addEventListener('submit', (event) => {
//     event.preventDefault();
//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;
//     const status = document.getElementById('status').value;

//     ipcRenderer.send('perform-register', { username, password, status });
//   });

ipcRenderer.on('register_success', (event,data) => {
    window.location.href = '../views/index.html';
    remote.app.emit('main-page');
});

ipcRenderer.on('register-failure', (event, data) => {
    const our_data = data.response;
    document.getElementById('message_register').textContent = our_data;
});

ipcRenderer.on('reset-register', () => {
    document.getElementById('message').textContent = '';
    // Optionally, clear the username and password fields
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('status').value = '';
    // Enable the login button if it was previously disabled
    document.getElementById('loginButton').disabled = false;
});