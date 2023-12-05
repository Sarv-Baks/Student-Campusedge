document.addEventListener("DOMContentLoaded", function() {
    // Get login time from server
    fetch('/get_login_time')
        .then(response => response.json())
        .then(data => {
            const loginTimeElement = document.getElementById('loginTime');
            loginTimeElement.textContent = `Logged in at: ${data.loginTime}`;
            
            // Calculate time spent
            const currentTime = new Date().getTime();
            const loginTime = new Date(data.loginTime).getTime();
            let timeSpentInMilliseconds = currentTime - loginTime;
            if (timeSpentInMilliseconds < 0) {
                timeSpentInMilliseconds = 0;
            }
            const seconds = Math.floor(timeSpentInMilliseconds / 1000);
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const remainingSeconds = seconds % 60;
            const timeSpentElement = document.getElementById('timeSpent');
            timeSpentElement.textContent = `Time Spent: ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});