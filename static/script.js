// static/script.js

// Function for Signup
async function signup() {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const userType = document.getElementById('user_type') ? document.getElementById('user_type').value : null; // Get user type, check if element exists

    const resultElement = document.getElementById('signup-result');

    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                email: email,
                password: password,
                user_type: userType // Include user_type
            })
        });

        const data = await response.json();
        resultElement.innerText = data.message;

        if (response.ok) {
            resultElement.style.color = 'green';
            window.location.href = '/login'; 
        } else {
            resultElement.style.color = 'red';
        }
    } catch (error) {
        console.error('Error during signup:', error);
        resultElement.innerText = 'An error occurred. Please try again.';
        resultElement.style.color = 'red';
    }
}

// Function for Login
async function login() {
    event.preventDefault(); // Prevent default form submission
    console.log("Login button clicked"); 
    
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const resultElement = document.getElementById('login-result');

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, password: password })
        });

        const data = await response.json();
        resultElement.innerText = data.message;

        if (response.ok) {
            resultElement.style.color = 'green';
            if (data.redirect) {
                window.location.href = data.redirect;
            }
        } else {
            resultElement.style.color = 'red';
        }
    } catch (error) {
        console.error('Login error:', error);
        resultElement.innerText = 'An error occurred. Please try again.';
        resultElement.style.color = 'red';
    }
}