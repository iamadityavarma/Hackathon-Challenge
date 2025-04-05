## MindMate – AI-Powered Mental Health Companion

MindMate is a full-stack mental health app that provides AI-powered chat support using the Claude API. The platform includes secure JWT-based authentication, appointment booking, and a clean frontend interface focused on user experience and accessibility.

---

### Features

- AI chat support using Claude API
- Secure user authentication (JWT)
- Appointment booking system
- Clean and accessible UI/UX
- Full-stack architecture using ReactJS, Flask, and SQLite

---

### Tech Stack

| Frontend | Backend | Database | Authentication | AI Integration |
| -------- | ------- | -------- | -------------- | -------------- |
| ReactJS  | Flask   | SQLite   | JWT            | Claude API     |

---

### Project Structure

```
/client        # React frontend
/server        # Flask backend
  ├── routes   # API endpoints
  ├── models   # Database models
  └── utils    # Utility functions (Claude API, JWT, etc.)
```

---

### Getting Started

**1. Clone the Repository**

```bash
git clone https://github.com/Soumya98-dev/MindMate.git
cd MindMate
```

**2. Set Up and Run the Backend (Flask)**

```bash
cd server
pip install -r requirements.txt
python app.py
```

**3. Set Up and Run the Frontend (React)**

```bash
cd client
npm install
npm start
```

---

### API Overview (Optional)

```http
POST /api/auth/login         # Authenticate user
POST /api/chat               # Interact with Claude API
GET /api/appointments        # Retrieve appointment data
```

---

### Inspiration

MindMate was created to explore the intersection of AI and mental health. The goal was to develop an accessible, user-friendly platform that leverages modern tech to support emotional well-being.

---

### Achievements

- Secured 5th place at Wayne State Hackathon 2024

---

### Author

**Soumyadeep Chatterjee**
[GitHub](https://github.com/Soumya98-dev) • [LinkedIn](https://www.linkedin.com/in/deep98)

---

### License

This project is licensed under the MIT License.
