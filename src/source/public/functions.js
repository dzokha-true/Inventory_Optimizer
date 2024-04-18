const { ipcRenderer } = require('electron');

document.getElementById('loginForm').addEventListener('submit', (event) => {
    event.preventDefault(); 
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    ipcRenderer.send('perform-login', { username, password });
  });
  
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

ipcRenderer.on('login-attempt-exceeded', () => {
    document.getElementById('message').textContent = 'You have exceeded the number of login attempts.';
    document.getElementById('loginButton').disabled = true; 
    window.location.href = '../views/index.html';
    remote.app.emit('main-page');
});

ipcRenderer.on('reset-login', () => {
    document.getElementById('message').textContent = '';
    // Optionally, clear the username and password fields
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    // Enable the login button if it was previously disabled
    document.getElementById('loginButton').disabled = false;
});
