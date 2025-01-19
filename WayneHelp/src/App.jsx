import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import LoginPage from "./components/LoginPage";
import StudentLogin from "./components/StudentLogin";
import CreateAccount from "./components/CreateAccount";
import ChatWindow from "./components/ChatWindow";
import AppointmentPage from "./components/AppointmentPage";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/student-login" element={<StudentLogin />} />
          <Route path="/create-account" element={<CreateAccount />} />
          <Route path="/chat" element={<ChatWindow />} />
          <Route path="/appointment" element={<AppointmentPage />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
