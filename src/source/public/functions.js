const { ipcRenderer } = require('electron');

document.addEventListener('DOMContentLoaded', () => {
    	const loginForm = document.getElementById('loginForm');
    	const registerForm = document.getElementById('registerForm');
	
	if (loginForm) {
        	loginForm.addEventListener('submit', (event) => {
            		event.preventDefault();
            		const username = document.getElementById('username').value;
            		const password = document.getElementById('password').value;
            		ipcRenderer.send('perform-login', { username, password });
        	});
	}

    	if (registerForm) {
        	registerForm.addEventListener('submit', (event) => {
            		event.preventDefault();
            		const username = document.getElementById('username').value;
            		const password = document.getElementById('password').value;
                        const status = document.getElementById('status').value;
            		ipcRenderer.send('perform-register', { username, password, status });
        	});
	}

	const goToLoginButton = document.getElementById('goToLogin');
    	if (goToLoginButton) {
        	goToLoginButton.addEventListener('click', () => {
            		window.location.href = 'login.html';
        	});
    	}

    	const goToRegisterButton = document.getElementById('goToRegister');
    	if (goToRegisterButton) {
        	goToRegisterButton.addEventListener('click', () => {
            		window.location.href = 'register.html';
        	});
    	}

});

ipcRenderer.on('login-failure', (event, data) => {
	document.getElementById('message').textContent = `Login failed. Attempts left: ${data.attemptsLeft}`;
});


ipcRenderer.on('register-failure', (event, data) => {
    	document.getElementById('message_register').textContent = data.registerResponse;
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


