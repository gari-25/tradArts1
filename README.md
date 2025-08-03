# 🎨 KalaKosh – Preserving the Soul of Indian Art

KalaKosh is a cultural web application designed to digitally preserve, promote, and celebrate traditional Indian art forms through an interactive and visually rich platform.

---

## 📖 Idea in Brief

KalaKosh showcases regional art through state-wise galleries, highlights events and exhibitions, and provides artists with personal dashboards to connect with a wider audience.

---

## ❓ What Real-Life Problem Does It Tackle?

Traditional Indian art forms are underrepresented online, and many artists struggle with visibility and digital outreach. KalaKosh helps preserve these art forms while providing artists a space to be discovered.

---

## 🚀 Features

- 🏠 Artistic homepage with scroll-based reveal animations
- 🖼️ State-wise image galleries of Indian art forms
- 📅 Event listings and user registration
- 👤 Dashboards for artists
- 🔐 Login/Signup functionality with secure authentication
- ✨ Smooth UI transitions using GSAP animations

---

## 🧱 Tech Stack

| Category             | Technologies Used                          |
|----------------------|---------------------------------------------|
| Frontend             | HTML, CSS, JavaScript                      |
| UI Animations        | GSAP (ScrollTrigger for reveal effects)    |
| Backend              | Flask (Python)                             |
| Authentication       | Firebase Admin SDK                         |
| Local Storage        | JSON (users.json)                          |
| Security             | werkzeug.security (password hashing)       |
| Templates            | Jinja2 (via Flask)                         |

---

## 🔐 Firebase Integration

- Firebase Admin SDK is used for:
  - Email/password user creation and login
  - UID management and authentication
  - Custom token generation
- Credentials are loaded via:
  - Environment variable (`FIREBASE_ADMIN_CREDENTIALS`) or
  - Local `serviceAccountKey.json` file
- User details are synced in a local users.json file for reference and role management

