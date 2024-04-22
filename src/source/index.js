const {app, BrowserWindow, ipcMain, ipcRenderer} = require("electron");
const url = require("url");
const path = require("path");
const { spawn } = require('child_process');


let mainWin;
let userWin;
let loginAttempts = 0;
const MAX_LOGIN_ATTEMPTS = 5;

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

function resetLoginAttempts() {
    loginAttempts = 0;
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

// login page
app.on("open-login-page", () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/login.html"),
        protocol: "file",
        slashes: true
    }));
});

// for login performing
ipcMain.on('perform-login', (event, { username, password}) => {
    loginAttempts++;
    operation = 'login';
    if (loginAttempts >= MAX_LOGIN_ATTEMPTS) {
        resetLoginAttempts();
        event.reply('reset-login');
        mainWin.loadFile('src/source/views/index.html');
        return;
    }
    
    const pythonProcess = spawn('python', ['src/database/Mathematics.py', username, password, operation]);

    pythonProcess.stdout.on('data', (data) => {
      const loginResponse = data.toString().trim();
        
      if (loginResponse === 'Success') { 
	event.reply('login-success', { username, password });
      } else {
        event.reply('login-failure', { attemptsLeft: 5 - loginAttempts });
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

  // for performing registration
  ipcMain.on('perform-register', (event, { username, password, status }) => {
    operation = 'register';
    // change path to script for register
    const pythonProcess = spawn('python', ['src/database/Mathematics.py', username, password, status, operation]);

    pythonProcess.stdout.on('data', (data) => {
      const registerResponse = data.toString().trim();

      let dataString = ''
      dataString += registerResponse;
        
      if (registerResponse === 'Success') { 
	    event.reply('register_success', { username, password });
      } else {
          event.reply('register-failure', {response: dataString});
      }

    });  
    pythonProcess.on('error', (error) => {
      console.error(`An error occurred: ${error.message}`);
      event.reply('register-failure', 'An error occurred during register.');
    });
  
    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      event.reply('register-failure', 'An error occurred during register.');
    });
  });

// for generating report for performance page
ipcMain.on('get_report', (event, { message }) => {
    const operation = message;
    // change path to script
    const pythonProcess = spawn('python', ['src/database/Mathematics.py', username, status, operation]);

    pythonProcess.stdout.on('data', (data) => {
      const performanceResponse = data.toString().trim();

      let dataString = ''
      dataString += performanceResponse;
        
      event.reply('performance-success', { username});

    });  
    pythonProcess.on('error', (error) => {
      console.error(`An error occurred: ${error.message}`);
      event.reply('performance-failure', 'An error occurred during loading report.');
    });
  
    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      event.reply('performance-failure', 'An error occurred during loading report.');
    });
  });

//renderer for each page
ipcMain.on('main-page', () => {
	mainWin.loadURL(url.format({
		pathname: path.join(__dirname, "views/index.html"),
		protocol: "file",
		slashes: true
	}));
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

ipcMain.on('dashboard-page', (event, message) => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/dashboard.html"),
        protocol: "file",
        slashes: true
    }));
    
    const operation = message;
    // change path to script
    const pythonProcess = spawn('python', ['src/database/Mathematics.py', username, status, operation]);

    pythonProcess.stdout.on('data', (data) => {
      const performanceResponse = data.toString().trim();

      let dataString = ''
      dataString += performanceResponse;
        
      event.reply('performance-success', { username});

    });  
    pythonProcess.on('error', (error) => {
      console.error(`An error occurred: ${error.message}`);
      event.reply('dashboard-failure', 'An error occurred during loading dashboard.');
    });
  
    pythonProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
      event.reply('dashboard-failure', 'An error occurred during loading dashboard.');
    });
});

ipcMain.on('inventory-page', () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/inventory.html"),
        protocol: "file",
        slashes: true
    }));
});

///////// create table
ipcMain.on('create-table', (event, {message}) => {

    const python = spawn('python', ["src/database/Product.py", message]);

    let dataString = '';
    python.stdout.on('data', (data) => {
        dataString += data.toString();
        event.reply('table_success', {dataset: dataString});
        //console.log(dataString);
    });
    
    python.stdout.on('end', () => {
        //const dataconvert = JSON.parse(dataString);
        // app.get('/data', (req, res) => {
        //     res.json(dataconvert); // send data to front-end
        // });
    });
    
    python.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });
    
    python.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
  });

ipcMain.on('order-page', () => {
    mainWin.loadURL(url.format({
        pathname: path.join(__dirname, "views/order.html"),
        protocol: "file",
        slashes: true
    }));
});

app.on('window-all-closed', () => app.quit());
app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
});