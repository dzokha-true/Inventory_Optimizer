 function isAuthenticated(username,password){
     const validUsername = "Username";
     const validPassword = "Password";

     if (username == validUsername && password == validPassword){
     return true;
     } else {
         return false;
     }
 }

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
