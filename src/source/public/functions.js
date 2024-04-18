// function isAuthenticated(username,password){
//     const validUsername = "Username";
//     const validPassword = "Password";

//     if (username == validUsername && password == validPassword){
//     return true;
//     } else {
//         return false;
//     }
// }

// function runLoginScript(scriptPath="src/database/LoginSystem.py", args) {
//     const python = spawn("../Inventory_Optimizer/.venv/bin/python", [scriptPath, ...args]);

//     python.stdout.on('data', (data) => {
//         console.log(`stdout: ${data}`);
//         const loginResponse = data.toString().trim();
        
//         return loginResponse;
//     });

//     python.stderr.on('data', (data) => {
//         console.error(`stderr: ${data}`);
//     });
//     python.on('close', (code) => {
//         console.log(`child process exited with code ${code}`);
//     });
// }

const { ipcRenderer } = require('electron');
//const { remote } = require('electron');

document.getElementById('loginForm').addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent the default form submission
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    ipcRenderer.send('perform-login', { username, password });
  });
  
ipcRenderer.on('login-success', (event, arg) => {
     // Load the page on successful login
    window.location.href = '../views/map.html';
    remote.app.emit('map-page');
    //alert("valid username or password");
    //  console.log("success");
   });

ipcRenderer.on('login-failure', (event, data) => {
    if (data.attemptsLeft > 0) {
        document.getElementById('message').textContent = `Login failed. Attempts left: ${data.attemptsLeft}`;
    } else {
        document.getElementById('message').textContent = 'You have exceeded the number of login attempts.';
        document.getElementById('loginButton').disabled = true;
    }
});

ipcRenderer.on('login-attempt-exceeded', () => {
    document.getElementById('message').textContent = 'You have exceeded the number of login attempts.';
    document.getElementById('loginButton').disabled = true;
});
