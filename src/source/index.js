const {app, BrowserWindow, ipcMain, ipcRenderer} = require("electron");
const url = require("url");
const path = require("path");
const { spawn } = require('child_process');

//electron reload
// if(process.env.NODE_ENV !== "production"){
//     require("electron-reload")(__dirname, {
//         electron: path.join(__dirname, "../node_modules", ".bin", "electron")
//     });
// }
// var isDev = process.env.APP_DEV ? (process.env.APP_DEV.trim() == "true") : false;

// if (isDev) {
//     require('electron-reload')(__dirname, {
//         electron: path.join(__dirname, 'node_modules', '.bin', 'electron')
//     });
// }

let mainWin;
let userWin;

function createWindow() {
    mainWin = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        width: 1200,
        height: 600,
        backgroundColor: "#ffffff",
        icon: `file://${__dirname}/public/images/logo.png`
    });

     mainWin.loadURL(url.format({
          pathname: path.join(__dirname, "views/index.html"),
          protocol: "file",
          slashes: true
      }));

    mainWin.on("closed", () =>{
        mainWin = null;
        app.quit();
    });
}

function createuserWindow() {
    userWin = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        },
        width: 1200,
        height: 600,
        backgroundColor: "#ffffff",
        icon: `file://${__dirname}/public/images/logo.png`
    });

    userWin.loadURL(url.format({
         pathname: path.join(__dirname, "views/map.html"),
         protocol: "file",
         slashes: true
     }));

    userWin.on("closed", () =>{
        userWin = null;
        app.quit();
    });
}

app.on("ready", async() => {
    await createWindow();
})

app.on("activate", () => {
    if (mainWin === null) {
        createWindow();
    }
});


app.on("open-login-page", () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/login.html"),
        protocol: "file",
        slashes: true
    }));
});

ipcMain.on('perform-login', (event, { username, password }) => {
    // Here, replace 'path/to/LoginSystem.py' with the actual path to your Python script
    const pythonProcess = spawn('../Inventory_Optimizer/.venv/bin/python', ['src/database/LoginSystem.py', username, password]);

    pythonProcess.stdout.on('data', (data) => {
      const loginResponse = data.toString().trim();
        
      if (loginResponse === 'Success') { // Assuming 'Success' is printed by your Python script
        //console.log("B");
        event.reply('login-success', { username, password });
        // mainWin.close();
        // createuserWindow();
      } else {
        //console.log("C");
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

ipcMain.on('map-page', () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/map.html"),
        protocol: "file",
        slashes: true
    }));
});

ipcMain.on('data-page', () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/data.html"),
        protocol: "file",
        slashes: true
    }));
});

ipcMain.on('dashboard-page', () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/dashboard.html"),
        protocol: "file",
        slashes: true
    }));
});

ipcMain.on('inventory-page', () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/inventory.html"),
        protocol: "file",
        slashes: true
    }));
});


ipcMain.on('order-page', () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/order.html"),
        protocol: "file",
        slashes: true
    }));
});
