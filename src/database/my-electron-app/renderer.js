const { ipcRenderer } = require('electron');

document.getElementById('loginForm').addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the default form submission
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  ipcRenderer.send('perform-login', { username, password });
});

ipcRenderer.on('login-success', (event, arg) => {
  // Load the dashboard page on successful login
  window.location.href = 'dashboard.html';
});

ipcRenderer.on('login-failure', (event, arg) => {
  const messageDiv = document.getElementById('message');
  messageDiv.innerText = arg; // Display the error message
});

