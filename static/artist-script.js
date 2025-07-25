// static/artist-script.js

// REGISTER FORM SUBMIT
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const res = await fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    alert(data.message);
    if (res.ok) window.location.href = '/artist-login';
  });
}

// LOGIN FORM SUBMIT
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUser').value;
    const password = document.getElementById('loginPass').value;

    const res = await fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    alert(data.message);
    if (res.ok) window.location.href = '/artist-dashboard';
  });
}

// ART UPLOAD FORM
const artForm = document.getElementById('artForm');
if (artForm) {
  artForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('artTitle').value;
    const description = document.getElementById('artDesc').value;
    const image_url = document.getElementById('artImageUrl').value;

    const res = await fetch('/upload_art', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, image_url })
    });

    const data = await res.json();
    alert(data.message);
  });
}

// EVENT CREATION FORM
const eventForm = document.getElementById('eventForm');
if (eventForm) {
  eventForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('eventName').value;
    const description = document.getElementById('eventDesc').value;
    const location = document.getElementById('eventLoc').value;
    const date = document.getElementById('eventDate').value;

    const res = await fetch('/create_event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description, location, date })
    });

    const data = await res.json();
    alert(data.message);
  });
}

// DASHBOARD FETCH
const artworksContainer = document.getElementById('artworks');
const eventsContainer = document.getElementById('events');

if (artworksContainer || eventsContainer) {
  fetch('/dashboard_data')
    .then(res => res.json())
    .then(data => {
      if (artworksContainer) {
        artworksContainer.innerHTML = data.artworks.map(art => `
          <div>
            <h4>${art.title}</h4>
            <img src="${art.image_url}" alt="${art.title}">
            <p>${art.description}</p>
          </div>
        `).join('');
      }
      if (eventsContainer) {
        eventsContainer.innerHTML = data.events.map(ev => `
          <div>
            <h4>${ev.name}</h4>
            <p>${ev.description}</p>
            <p>${ev.location} | ${ev.date}</p>
          </div>
        `).join('');
      }
    });
}
