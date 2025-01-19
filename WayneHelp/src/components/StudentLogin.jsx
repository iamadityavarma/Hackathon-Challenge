import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../UserContext";
import "./StudentLogin.css";

const StudentLogin = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { user } = useContext(UserContext);

  const navigate = useNavigate();

  // const handleSignIn = (e) => {
  //   e.preventDefault();

  //   if (user && user.username === username && user.password === password) {
  //     alert("Sign-In Successful!");
  //     navigate("/chat");
  //   } else {
  //     alert("Invalid username or password");
  //   }
  // };

  const handleSignIn = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Login successful");
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);
        window.location.href = "/chat";
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error("Error logging in:", error);
    }
  };

  return (
    <div className="student-login-container">
      <header>
        <h1>Student Login</h1>
      </header>
      <div className="login-box">
        <h2>Welcome to Wayne Help</h2>
        <form onSubmit={handleSignIn}>
          <div className="input-container">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="input-container">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="sign-in-button">
            Sign In
          </button>
        </form>
        <p>
          <a href="/create-account" className="create-account-link">
            Create Account
          </a>
        </p>
      </div>
    </div>
  );
};

export default StudentLogin;
