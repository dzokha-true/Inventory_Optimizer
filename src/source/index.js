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

app.on("open-login-page", () => {
	mainWin.loadURL(url.format({
        	pathname: path.join(__dirname, "views/login.html"),
        	protocol: "file",
        	slashes: true
    	}));
});

ipcMain.on('perform-login', (event, { username, password}) => {
	loginAttempts++;
    	operation = 'login';
    	if (loginAttempts >= MAX_LOGIN_ATTEMPTS) {
        	loginAttempts = 0;
		mainWin.loadFile('src/source/views/index.html');
	}
    	const pythonProcess = spawn('python', ['src/database/Main.py', username, password, operation]);
	pythonProcess.stdout.on('data', (data) => {
      		const loginResponse = data.toString().trim(); 
		if (loginResponse === 'Success') { 
			mainWin.loadFile('src/source/views/dashboard.html');	
		} else {
        		event.reply('login-failure', { attemptsLeft: 5 - loginAttempts });
      		}
	});
});

ipcMain.on('perform-register', (event, { username, password, status }) => {
	operation = 'register';
	const pythonProcess = spawn('python', ['src/database/Main.py', username, password, status, operation]);
    	pythonProcess.stdout.on('data', (data) => {
      		const registerResponse = data.toString().trim();
		if (registerResponse === 'Success') { 
	    		mainWin.loadFile('src/source/views/dashboard.html');
      		} else {
          		event.reply('register-failure', {registerResponse});
      		}
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

ipcMain.on('create-sale-table', (event, {abc}) => {
	const pageNumber = abc; // Make sure this is the correct page number
	operation = "create-sale-table";
	const python = spawn('python', ["src/database/Main.py", pageNumber, operation]);
	let dataString = '';
	python.stdout.on('data', (data) => {
    dataString += data.toString();
		event.reply('sale_table_success', {dataset: dataString});
	});
  python.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
});

ipcMain.on('create-order-table', (event, {abc}) => {
	const pageNumber = abc; // Make sure this is the correct page number
	operation = "create-order-table";
	const python = spawn('python', ["src/database/Main.py", pageNumber, operation]);
	let dataString = '';
	python.stdout.on('data', (data) => {
    dataString += data.toString();
		event.reply('order_table_success', {dataset: dataString});
	});
  python.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
});

ipcMain.on('create-product-table', (event, {abc}) => {
	const pageNumber = abc; // Make sure this is the correct page number
	operation = "create-product-table";
	const python = spawn('python', ["src/database/Main.py", pageNumber, operation]);
	let dataString = '';
	python.stdout.on('data', (data) => {
    dataString += data.toString();
		event.reply('product_table_success', {dataset: dataString});
	});
  python.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });

  python.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
});

// for generating dashboard page
ipcMain.on('get_dashboard', (event, {message, message2}) => {
  const operation = message;
  const operation2 = message2;
  // change path to script
  const pythonProcess = spawn('python', ['src/database/Main.py', operation]);
  const pythonProcess2 = spawn('python', ['src/database/Main.py', operation2]);

  pythonProcess.stdout.on('data', (data) => {
  const Response = data.toString().trim();

    let dataString = ''
    dataString += Response;
      
    event.reply('dashboard-success', {dataset: dataString});

  });  
  pythonProcess.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
    event.reply('performance-failure', 'An error occurred during loading report.');
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    event.reply('performance-failure', 'An error occurred during loading report.');
  });

  pythonProcess2.stdout.on('data', (data) => {
    const Response = data.toString().trim();
  
    let dataString = ''
    dataString += Response;

    event.reply('dashboard-success2', {dataset: dataString});
  
  });  
  pythonProcess2.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
    event.reply('performance-failure', 'An error occurred during loading report.');
  });

  pythonProcess2.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    event.reply('performance-failure', 'An error occurred during loading report.');
  });
});

// for generating report for performance page
ipcMain.on('get_report', (event, { message }) => {
    const operation = message;
    // change path to script
    const pythonProcess = spawn('python', ['src/database/Main.py', operation]);

    pythonProcess.stdout.on('data', (data) => {
      const performanceResponse = data.toString().trim();

      let dataString = ''
      dataString += performanceResponse;
        
      event.reply('performance-success', {dataset: dataString});

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

///////// add product from inventory // add field
ipcMain.on('add_product', (event, {field,message}) => {

  const python = spawn('python', ["src/database/Main.py", field, message]);

  python.stdout.on('data', (data) => {
    console.log("Success");
  });
  
  python.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
  });
  
  python.on('close', (code) => {
      console.log(`child process exited with code ${code}`);
  });
});

// for changing fiscal year
ipcMain.on('send date', (event, { end,username,message }) => {
  const operation = message;
  // change path to script
  const pythonProcess = spawn('python', ['src/database/Main.py', end, username,operation]);

  pythonProcess.stdout.on('data', (data) => {
    alert("change fiscal year successfully!");
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

// for changing fifo lifo
ipcMain.on('change lifo fifo', (event, { status,username,message }) => {
  const operation = message;
  // change path to script
  const pythonProcess = spawn('python', ['src/database/Main.py', status, username,operation]);

  pythonProcess.stdout.on('data', (data) => {
    alert("change fifo lifo successfully!");
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
