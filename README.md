Wayne State Mental Health Chatbot - 2024
A mental health support chatbot designed to assist Wayne State students with their mental well-being and connect them with professional counselors.
Features

🤖 AI-powered mental health chat support

👥 Professional counselor booking system

📅 Availability management for counselors

🔒 Secure user authentication

💬 Real-time chat functionality

📊 Student and professional dashboards

Project Structure
Frontend (WayneHelp)

WayneHelp/

├── public/              # Static files
├── src/                 # Source files
│   ├── components/      # Reusable components
│   ├── pages/          # Page components
│   │   ├── Login/      # Login page
│   │   ├── Register/   # Registration page
│   │   ├── Chat/       # Chatbot interface
│   │   └── Appointments/# Appointment management
│   └── assets/         # Images and styles
├── package.json        # Dependencies
└── vite.config.js      # Vite configuration

## Pages and Features

### Login Page

User authentication
Role-based access (student/professional)
Password recovery option


### Registration Page

User registration form
Role selection
Email verification


### Chatbot Interface

Real-time chat with AI
Mental health support
Crisis resources
Chat history


### Appointment System

View available counselors
Book appointments
Manage bookings
View availability calendar



### Tech Stack
Frontend

React + Vite
Tailwind CSS for styling
React Router for navigation
JWT for authentication

### Backend

Python/Flask
SQLite database
Claude API integration
JWT authentication

### Prerequisites

Node.js 14+ for frontend
Python 3.8+ for backend
npm or yarn
Git
SQLite3

### Installation
Frontend Setup

## Navigate to frontend directory
cd WayneHelp

## Install dependencies
npm install

## Start development server
npm run dev

## Navigate to backend directory
cd ..

## Create and activate virtual environment
python -m venv venv

## Windows
venv\Scripts\activate

## Unix/MacOS
source venv/bin/activate

## Install dependencies
pip install -r requirements.txt

Environment Configuration
Create .env file in root directory:
CopyFLASK_APP=run.py
FLASK_DEBUG=1
JWT_SECRET_KEY=your_jwt_secret
ANTHROPIC_API_KEY=your_anthropic_api_key
Database Setup
bashCopyflask db upgrade
python create_table.py
Running the Application

Start the backend server

bashCopyflask run

Start the frontend development server

bashCopycd WayneHelp
npm run dev

Access the application at http://localhost:5173

API Endpoints
Authentication

POST /auth/register - Register new user
POST /auth/login - User login

Chat

POST /chat/send - Send message to chatbot
GET /chat/history - Get chat history

Appointments

GET /professionals - List all professionals
POST /book_appointment - Book an appointment
GET /appointments - Get user's appointments

Availability

POST /availability/add - Add professional availability
GET /availability - Get professional's availability

Database Schema
Users Table
sqlCopyCREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
Availability Table
sqlCopyCREATE TABLE availability (
    id INTEGER PRIMARY KEY,
    professional_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
);
Appointments Table
sqlCopyCREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    professional_id INTEGER NOT NULL,
    appointment_time TEXT NOT NULL,
    created_at DATETIME
);
Testing
Backend Testing
Use Thunder Client or Postman for API testing:
bashCopy# Example: Test chat endpoint
POST http://localhost:5000/chat/send
Content-Type: application/json
Authorization: Bearer your_jwt_token

{
    "message": "I'm feeling anxious about my exams"
}
Frontend Testing
bashCopycd WayneHelp
npm run test
Troubleshooting

Frontend Issues

bashCopy# Clear npm cache
npm cache clean --force
npm install

## If Vite issues occur
npm run dev -- --force

## Backend Issues

bashCopy# Database reset
flask db stamp head
flask db migrate
flask db upgrade

## Package issues
pip install -r requirements.txt --no-cache-dir
Contributing

## Fork the repository
Create feature branch: git checkout -b feature/AmazingFeature
Commit changes: git commit -m 'Add AmazingFeature'
Push to branch: git push origin feature/AmazingFeature
Open a pull request

## License
This project is licensed under the MIT License.

