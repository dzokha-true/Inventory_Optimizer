const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let loginWindow;
let dashboardWindow;

function createLoginWindow() {
  loginWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // This should be true and use preload scripts in production
    }
  });

  loginWindow.loadFile('index.html');

  loginWindow.on('closed', () => {
    loginWindow = null;
  });
}

function createDashboardWindow() {
  dashboardWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false // Again, consider security implications
    }
  });

  dashboardWindow.loadFile('dashboard.html');

  dashboardWindow.on('closed', () => {
    dashboardWindow = null;
  });
}

app.whenReady().then(createLoginWindow);

ipcMain.on('perform-login', (event, { username, password }) => {
  // Here, replace 'path/to/LoginSystem.py' with the actual path to your Python script
  const pythonProcess = spawn('python', ['Mathematics.py', username, password]);

  pythonProcess.stdout.on('data', (data) => {
    const loginResponse = data.toString().trim();

    if (loginResponse === 'Success') { // Assuming 'Success' is printed by your Python script
      loginWindow.close(); // Close the login window
      createDashboardWindow(); // Create the dashboard window
    } else {
      event.reply('login-failure', 'Login Failed. Please try again.');
    }
  });

  pythonProcess.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
    event.reply('login-failure', 'An error occurred during login.');
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    event.reply('login-failure', 'An error occurred during login.');
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createLoginWindow();
  }
});

