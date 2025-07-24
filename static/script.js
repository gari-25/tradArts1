// Signup
const signupForm = document.getElementById('signup-form');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('signup-username').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;

        const response = await fetch('/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });

        const result = await response.json();
        document.getElementById('signup-result').innerText = result.message;
    });// static/script.js

function signup() {
  const username = document.getElementById("signup-username").value;
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "signup-username": username,
      "signup-email": email,
      "signup-password": password,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("signup-result").innerText = data.message;
      window.location.href = "/login";
    })
    .catch((err) => {
      document.getElementById("signup-result").innerText = "Something went wrong.";
    });
}

function login() {
  console.log("Login button clicked"); 
  
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;

  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("login-result").innerText = data.message;
      if (data.redirect) {
        window.location.href = data.redirect;
      }
    })
    .catch((err) => {
      console.error("Login error:", err);
      document.getElementById("login-result").innerText = "Something went wrong.";
    });
}

}


